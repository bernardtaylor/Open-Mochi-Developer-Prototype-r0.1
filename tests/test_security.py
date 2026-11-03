import asyncio
from httpx import ASGITransport, AsyncClient
from gateway.app import create_app
from gateway.bridge import SimulatorBridge


def test_localhost_security():
    asyncio.run(_run())


async def _run():
    app = create_app(SimulatorBridge())
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        blocked = await client.post("/api/command", json={"command": "E:happy"},
                                    headers={"Origin": "https://untrusted.example"})
        assert blocked.status_code == 403
        good = await client.post("/api/command", json={"command": "I"},
                                 headers={"Origin": "http://testserver"})
        assert good.status_code == 200
        assert good.json()["reply"] == "ID:0.2,sim"
        state = await client.get("/api/state")
        assert state.json()["state"]["expression"] == "neutral"
        invalid_host = await client.get("/api/state", headers={"Host": "outside.example"})
        assert invalid_host.status_code == 400
