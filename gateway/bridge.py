"""Transport adapters: simulation, USB/UART, or BLE.

A transport is selected explicitly at startup. No auto-scanning, port claiming,
network broadcasting, or cloud access happens in the default configuration.
"""
import asyncio
import time
from abc import ABC, abstractmethod
from .protocol import State, execute, validate

SERVICE_UUID = "8ef6c3e0-6d43-4a81-891e-e9e380720001"
WRITE_UUID = "8ef6c3e0-6d43-4a81-891e-e9e380720002"
NOTIFY_UUID = "8ef6c3e0-6d43-4a81-891e-e9e380720003"


class Bridge(ABC):
    @abstractmethod
    async def send(self, command: str) -> str:
        ...

    async def close(self):
        pass


class SimulatorBridge(Bridge):
    def __init__(self):
        self.state = State()

    async def send(self, command: str) -> str:
        return execute(self.state, command)


class SerialBridge(Bridge):
    def __init__(self, port: str):
        try:
            import serial
        except ImportError as exc:
            raise RuntimeError("Install pyserial: pip install -e '.[serial]'") from exc
        self.serial = serial.Serial(port, 115200, timeout=0.15)
        self.lock = asyncio.Lock()

    def _blocking_send(self, command: str):
        # Ignore USB boot logs and enforce an overall deadline. Each readline()
        # must be bounded by the underlying serial timeout too.
        deadline = time.monotonic() + 3.0
        self.serial.reset_input_buffer()
        self.serial.write((command + "\n").encode("ascii"))
        self.serial.flush()
        while time.monotonic() < deadline:
            line = self.serial.readline().decode("ascii", errors="replace").strip()
            if line.startswith(("OK:", "ERR:", "ST:", "ID:")):
                return line
        raise TimeoutError("No MOCHI/1 response received within 3 seconds")

    async def send(self, command: str) -> str:
        validate(command)
        async with self.lock:
            return await asyncio.to_thread(self._blocking_send, command)

    async def close(self):
        self.serial.close()


class BleBridge(Bridge):
    def __init__(self, address: str | None = None):
        self.address = address
        self.client = None
        self.last_reply = None
        self.reply_event = asyncio.Event()
        self.lock = asyncio.Lock()

    async def connect(self):
        try:
            from bleak import BleakClient, BleakScanner
        except ImportError as exc:
            raise RuntimeError("Install bleak: pip install -e '.[ble]'") from exc
        device = self.address or await BleakScanner.find_device_by_name("OpenMochi-r0", timeout=8)
        if not device:
            raise RuntimeError("OpenMochi-r0 BLE peripheral not found")
        self.client = BleakClient(device)
        await self.client.connect()

        def reply_handler(_characteristic, value):
            self.last_reply = bytearray(value).decode("ascii", errors="replace")
            self.reply_event.set()

        await self.client.start_notify(NOTIFY_UUID, reply_handler)

    async def send(self, command: str) -> str:
        validate(command)
        async with self.lock:
            if self.client is None or not self.client.is_connected:
                await self.connect()
            self.last_reply = None
            self.reply_event.clear()
            await self.client.write_gatt_char(WRITE_UUID, command.encode("ascii"), response=True)
            await asyncio.wait_for(self.reply_event.wait(), timeout=3)
            return self.last_reply or "ERR:NO_REPLY"

    async def close(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()
