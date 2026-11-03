"""MOCHI/1: deliberately small line/characteristic control protocol.

This module is also the software simulator's authoritative state machine.
No GPS coordinates, voice streams, private messages, or remote commands are permitted.
"""
from dataclasses import dataclass, asdict
from decimal import Decimal, InvalidOperation

FACES = ("neutral", "happy", "surprised", "sleepy", "listening", "talking", "sad")
MAX_LENGTH = 20


class ProtocolError(ValueError):
    pass


@dataclass
class State:
    expression: str = "neutral"
    speed_kmh: float = 0.0
    ptt: bool = False
    last_sound: int | None = None

    def public(self) -> dict:
        return asdict(self)


def validate(raw: str) -> str:
    if not isinstance(raw, str) or not (1 <= len(raw) <= MAX_LENGTH):
        raise ProtocolError("command must be 1..20 ASCII characters")
    try:
        raw.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ProtocolError("ASCII required") from exc
    if any(ord(c) < 32 or ord(c) > 126 for c in raw):
        raise ProtocolError("control or non-printable character")
    if raw in ("Q", "I"):
        return raw
    if raw.startswith("E:") and raw[2:] in FACES:
        return raw
    if raw.startswith("V:"):
        number = raw[2:]
        if not number or any(c not in "0123456789." for c in number):
            raise ProtocolError("speed must be decimal km/h")
        try:
            value = Decimal(number)
        except InvalidOperation as exc:
            raise ProtocolError("invalid speed") from exc
        if not (0 <= value <= 250):
            raise ProtocolError("speed outside 0..250 km/h")
        return raw
    if raw in ("S:1", "S:2", "S:3", "P:0", "P:1"):
        return raw
    raise ProtocolError("unknown command")


def execute(state: State, command: str) -> str:
    command = validate(command)
    if command == "Q":
        return f"ST:{state.expression},{state.speed_kmh:.1f}"
    if command == "I":
        return "ID:0.2,sim"
    kind, arg = command.split(":", 1)
    if kind == "E":
        state.expression = arg
        return f"OK:E:{arg}"
    if kind == "V":
        state.speed_kmh = float(arg)
        return "OK:V"
    if kind == "S":
        state.last_sound = int(arg)
        return "OK:S"
    if kind == "P":
        state.ptt = arg == "1"
        return "OK:P"
    raise ProtocolError("unreachable")
