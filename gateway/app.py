"""Local developer dashboard and command relay.

Run: python -m gateway.app --mode sim
HTTP is bound to 127.0.0.1 by default. Do not expose this unauthenticated
prototype on the public internet or a shared network.
"""
import argparse
import asyncio
import json
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from urllib.parse import urlsplit
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .bridge import SimulatorBridge, SerialBridge, BleBridge
from .protocol import State, ProtocolError, execute, validate
from .assistant import LocalAssistant

ROOT = Path(__file__).resolve().parent.parent


class CommandRequest(BaseModel):
    command: str


class AssistantRequest(BaseModel):
    text: str


def create_app(bridge=None, assistant=None) -> FastAPI:
    adapter = bridge or SimulatorBridge()
    @asynccontextmanager
    async def lifespan(_app):
        try:
            yield
        finally:
            await adapter.close()

    app = FastAPI(title="Open Mochi prototype gateway", version="0.2.0", lifespan=lifespan)
    # Loopback development only; reject DNS-rebinding hostnames and cross-origin
    # browser writes. This is a safety barrier, NOT production authentication.
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "testserver"])

    @app.middleware("http")
    async def same_origin_writes(request: Request, call_next):
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            origin = request.headers.get("origin")
            if origin:
                parsed = urlsplit(origin)
                if parsed.scheme not in ("http", "https") or parsed.netloc.lower() != request.headers.get("host", "").lower():
                    return JSONResponse(status_code=403, content={"detail": "Cross-origin request denied"})
        return await call_next(request)

    app.state.adapter = adapter
    app.state.mirror = State()
    app.state.clients = set()
    app.state.lock = asyncio.Lock()
    app.state.assistant = assistant

    @app.get("/api/state")
    async def get_state():
        return {"state": app.state.mirror.public(), "backend": adapter.__class__.__name__}

    @app.post("/api/command")
    async def command(request: CommandRequest):
        try:
            cmd = validate(request.command)
        except ProtocolError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        try:
            async with app.state.lock:
                reply = await adapter.send(cmd)
                if reply.startswith("OK:"):
                    execute(app.state.mirror, cmd)
                result = {"command": cmd, "reply": reply, "state": app.state.mirror.public()}
        except (TimeoutError, ConnectionError, OSError, RuntimeError, asyncio.TimeoutError) as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
        if reply.startswith("ERR:"):
            return JSONResponse(status_code=422, content=result)
        stale = []
        for client in list(app.state.clients):
            try:
                await client.send_json(result)
            except Exception:
                stale.append(client)
        for client in stale:
            app.state.clients.discard(client)
        return result

    @app.post("/api/assistant")
    async def assistant_message(request: AssistantRequest):
        if app.state.assistant is None:
            raise HTTPException(status_code=501, detail="Local AI is disabled; launch with --ollama-model MODEL")
        if not 1 <= len(request.text.strip()) <= 300:
            raise HTTPException(status_code=422, detail="text must be 1..300 characters")
        try:
            response = await asyncio.to_thread(app.state.assistant.respond, request.text)
        except (ValueError, OSError, TimeoutError) as exc:
            raise HTTPException(status_code=502, detail=f"Local AI unavailable: {type(exc).__name__}") from exc
        return {"response": response, "where_audio_plays": "browser_only"}

    @app.websocket("/api/events")
    async def events(websocket: WebSocket):
        origin = websocket.headers.get("origin")
        host = websocket.headers.get("host", "")
        if host.split(":")[0].lower() not in ("127.0.0.1", "localhost", "testserver"):
            await websocket.close(code=1008)
            return
        if origin:
            parsed = urlsplit(origin)
            if parsed.scheme not in ("http", "https") or parsed.netloc.lower() != host.lower():
                await websocket.close(code=1008)
                return
        await websocket.accept()
        app.state.clients.add(websocket)
        try:
            await websocket.send_json({"state": app.state.mirror.public(), "reply": "CONNECTED"})
            while True:
                # Browsers send keepalives; no command input is accepted via WS.
                await websocket.receive_text()
        except WebSocketDisconnect:
            pass
        finally:
            app.state.clients.discard(websocket)

    app.mount("/", StaticFiles(directory=str(ROOT / "web"), html=True), name="dashboard")
    return app


app = create_app()


def main():
    parser = argparse.ArgumentParser(description="Open Mochi developer gateway")
    parser.add_argument("--mode", choices=["sim", "serial", "ble"], default="sim")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--serial", dest="serial_port", help="USB/UART device path (COMx, /dev/ttyACM0)")
    parser.add_argument("--ble-address", help="Optional BLE device identifier/address")
    parser.add_argument("--ollama-model", help="Enable an explicitly selected locally installed Ollama model")
    args = parser.parse_args()
    if args.mode == "serial" and not args.serial_port:
        parser.error("--mode serial requires --serial PORT")
    bridge = (SimulatorBridge() if args.mode == "sim" else
              SerialBridge(args.serial_port) if args.mode == "serial" else
              BleBridge(args.ble_address))
    import uvicorn
    assistant = LocalAssistant(args.ollama_model) if args.ollama_model else None
    uvicorn.run(create_app(bridge, assistant=assistant), host="127.0.0.1", port=args.port, log_level="info")


if __name__ == "__main__":
    main()
