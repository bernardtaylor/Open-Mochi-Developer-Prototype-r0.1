import pytest
from gateway.protocol import State, ProtocolError, execute, validate, FACES


def test_valid_faces():
    for face in FACES:
        assert validate(f"E:{face}") == f"E:{face}"


def test_state_transitions():
    state = State()
    assert execute(state, "E:happy") == "OK:E:happy"
    assert execute(state, "V:42.5") == "OK:V"
    assert execute(state, "P:1") == "OK:P"
    assert execute(state, "S:2") == "OK:S"
    assert state.expression == "happy"
    assert state.speed_kmh == 42.5
    assert state.ptt is True
    assert state.last_sound == 2
    assert execute(state, "Q") == "ST:happy,42.5"


@pytest.mark.parametrize("command", ["", "E:invalid", "V:-1", "V:251", "V:nan", "V:1e2", "V:2.3.4", "P:2", "S:4", "DROP TABLE", "E:" + "x"*30, "E:happy\n", "E:🥳"])
def test_reject_invalid(command):
    with pytest.raises(ProtocolError):
        validate(command)
