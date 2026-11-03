# Community play-test: exact reproduction steps

## Software-only (Windows, Linux or macOS)

1. Install Python 3.10 or newer and extract this ZIP.
2. Open a terminal in the extracted directory (the directory containing `pyproject.toml`).
3. Create a virtual environment, activate it, and run `python -m pip install -e '.[test]'`.
4. Run `python -m pytest -q`. With a C++ compiler installed, the cross-language parser test must **not** skip.
5. Run `python -m gateway.app --mode sim` in a terminal; open `http://127.0.0.1:8765` on that same machine.
6. In a second terminal, run `python tools/playtest.py --output my-report.json`.
7. Confirm **12/12** commands passed and inspect browser expressions manually.
8. Stop the gateway with Ctrl+C; report the exact command, OS/Python version and redacted error log if anything fails.

Windows PowerShell activation: `.venv\\Scripts\\Activate.ps1` (if your execution policy permits it). Linux/macOS activation: `source .venv/bin/activate`.

## ESP32 electrical bench (new contribution, not yet verified)

1. Confirm your board is a supported or proposed reference ESP32-S3 DevKitC-1 revision and inspect its schematic.
2. Disable display/audio flags in `firmware/include/config.h` for initial USB/BLE-only smoke test.
3. Install PlatformIO, run `cd firmware && pio run`, and capture toolchain and build results.
4. Flash **only** to your ESP32 reference board, not Flipper or factory Mochi.
5. Send `I` followed by newline over USB serial and expect `ID:0.2,esp32s3`; send `Q` and expect neutral speed state.
6. Wire display/amplifier incrementally using `docs/WIRING.md`, checking voltage requirements before power.
7. Test serial, sound, expression changes, 10 BLE reconnections and malformed commands.
8. Record results in a GitHub hardware report, including commit hash and exact board revision.

## Flipper + Momentum bench (new contribution, not yet verified)

1. Record Momentum release/build and back up existing Flipper configuration.
2. Wire the Flipper USART to the **external ESP32 reference board only**, with 3.3V TX/RX crossover and common ground.
3. Use separate power sources and never connect independent power rails.
4. Run `flipper/mochi_control.js` using Apps → Scripts; verify `Identify`, `Status`, expressions and sound.
5. Report successful commands, timeouts and module conflicts. The presence of a USB-C connector on both devices is not evidence of a shared control protocol.

## Privacy and evidence

Keep the gateway on loopback only. Submit redacted text logs; no MACs, exact GPS coordinates, passwords, pairing secrets or unique device serial numbers. Do not upload factory firmware.
