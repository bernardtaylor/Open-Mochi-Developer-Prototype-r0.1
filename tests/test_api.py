import asyncio
from httpx import ASGITransport, AsyncClient
from gateway.app import create_app
from gateway.bridge import SimulatorBridge


def test_api():
    asyncio.run(_check())


async def _check():
    app = create_app(SimulatorBridge())
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        state = await client.get("/api/state")
        assert state.status_code == 200
        assert state.json()["state"]["expression"] == "neutral"
        result = await client.post("/api/command", json={"command": "E:happy"})
        assert result.status_code == 200
        assert result.json()["reply"] == "OK:E:happy"
        state = await client.get("/api/state")
        assert state.json()["state"]["expression"] == "happy"
        ai = await client.post("/api/assistant", json={"text":"hello"})
        assert ai.status_code == 501
        invalid = await client.post("/api/command", json={"command": "V:-99"})
        assert invalid.status_code == 422
