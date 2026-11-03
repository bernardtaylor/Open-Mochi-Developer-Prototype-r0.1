"""Run the exact parser compiled into ESP32 firmware as a host-native binary.
This checks that simulator and firmware agree on command acceptance.
No ESP32 hardware or network access required.
"""
import random
import shutil
import subprocess
from pathlib import Path
import pytest
from gateway.protocol import validate, ProtocolError

ROOT = Path(__file__).resolve().parents[1]

@pytest.fixture(scope="module")
def native_validator(tmp_path_factory):
    compiler = shutil.which("g++") or shutil.which("clang++")
    if not compiler:
        pytest.skip("No C++ compiler installed; install g++ for cross-language conformance")
    binary = tmp_path_factory.mktemp("cpp") / "protocol-validator"
    subprocess.run([compiler, "-std=c++11", "-Wall", "-Wextra", "-Werror",
                    "-I", str(ROOT / "firmware/include"),
                    str(ROOT / "tools/protocol_validator.cpp"), "-o", str(binary)],
                   check=True, capture_output=True, text=True)
    return binary

SAMPLES = ["I", "Q", "E:neutral", "E:talking", "V:42.5", "V:250", "V:250.00000",
           "V:0", "V:.5", "V:1.", "V:0000000", "S:1", "P:0",
           "", " ", "Q ", "i", "E:invalid", "E:happy ", "V:1e2", "V:+1", "V:-1",
           "V:250.01", "V:251", "V:.", "V:0..1", "V:nan", "V:99999999999999",
           "S:0", "P:2", "V:1/2", "E:happy\\n", "E:123456789012345678901"]

def test_native_vs_python_parser(native_validator):
    rng = random.Random(20261102)
    alphabet = "QIEVSP:0123456789.abcdef -+\\n"
    samples = SAMPLES + ["".join(rng.choice(alphabet) for _ in range(rng.randint(0, 24))) for _ in range(180)]
    for item in samples:
        if "\\x00" in item: continue
        try:
            validate(item)
            py_valid = True
        except ProtocolError:
            py_valid = False
        cpp = subprocess.run([str(native_validator), item], capture_output=True, text=True)
        assert cpp.returncode in (0, 2), cpp.stderr
        assert (cpp.returncode == 0) == py_valid, f"Mismatch for {item!r}"


def test_version_query_does_not_change_state():
    from gateway.protocol import State, execute
    state = State(expression="happy", speed_kmh=3.5)
    assert execute(state, "I") == "ID:0.2,sim"
    assert state.expression == "happy" and state.speed_kmh == 3.5
