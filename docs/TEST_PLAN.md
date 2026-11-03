# Reproducible play-testing and acceptance criteria

## Wave 0 · Anyone (software only)

Run `python -m pytest -q` and `python -m gateway.app --mode sim` (root `README.md`). The following should work:

| Test ID | Action | Pass criteria |
| --- | --- | --- |
| SIM-00 | Click **Identify protocol** | Reply starts `ID:0.2,sim`; state unchanged |
| SIM-01 | Click Happy | Face changes, console displays `OK:E:happy` |
| SIM-02 | Send `V:42.5` | UI shows 42.5 km/h, response `OK:V` |
| SIM-03 | Play `S:1` | Console shows `OK:S`; simulator does **not** play external audio |
| SIM-04 | Hold/release PTT button | Commands `P:1`, then `P:0`; **no voice transmission** |
| SIM-05 | Query `Q` | Reply `ST:<expression>,<speed>` |
| SIM-06 | Send `V:-12` or `E:bad` | HTTP 422, state remains unchanged |
| SIM-07 | Refresh browser | State is still held in server memory |
| SIM-08 | Restart server | State returns to neutral/0; persistence intentionally absent |

## Wave 1 · ESP32-S3 hardware developer

1. Disable display and I²S flags; compile/flash reference board.
2. Use USB serial at 115200, send `Q\n` and `E:happy\n`. Record hardware model and firmware version.
3. Connect known ST7789 display after power/pin validation; verify 7 expressions.
4. Connect compatible MAX98357A and speaker, test 3 tone patterns at modest level.
5. Connect BLE using a supported central and test writes + notifications without UART concurrently.
6. Repeat rapid changes (100 commands) and note malformed responses, freezes and reset reasons.
7. Disconnect and reconnect BLE ten times. Expected after each: service discoverable and controls functioning.

**First hardware acceptance gate:** one verified board revision compiles, passes all modes and produces reproducible assembly steps. This environment has not performed those physical tests.

## Wave 2 · Existing Flipper Zero + Momentum

1. Verify Flipper firmware release, script APIs and USART selection.
2. Connect only GND/TX/RX with both devices powered separately.
3. Start `flipper/mochi_control.js` under Apps → Scripts.
4. Observe menu input, `OK`/`ST` UART replies, screen/sound response on ESP32.
5. Test stopping script, unplugging cable and re-running without reset or port conflict.
6. Capture **only protocol logs** (no credentials, pairing data or account details).

## Wave 3 · Native mobile, future release

Test iOS/Android BLE permission and foreground operation, Bluetooth reconnection, secure pairing, phone GPS speed accuracy, background execution/OS throttling, audio echo/latency, offline modes, optional cloud account and PTT consent. **No claims of pass in r0.**

## Report a failure

Include exact board revision/flash size, OS, PlatformIO/Arduino version, firmware commit hash, source pinmap, expected/actual behaviour, reproducible steps and redacted UART logs. For Flipper, include Momentum release/build and whether USART is free. Use the GitHub issue templates. Never post home addresses, live location coordinates, Wi-Fi passwords, tokens or unique serial numbers.

## Cross-language conformance (new in r0.2)

Run `python -m pytest -q` with `g++` (or `clang++`) installed. The suite compiles the *actual header consumed by ESP32 firmware* into a host binary and compares valid/invalid command outcomes against the Python validator over example inputs and deterministic random inputs. A missing compiler **skips** that test, which is not acceptable for CI or a public release gate.

Run `node --check web/app.js` and `node --check flipper/mochi_control.js` to detect JavaScript syntax errors. **Node syntax validation does not prove compatibility with the Flipper mJS runtime or Momentum firmware.**

## Physical hardware evidence required

For every board claiming support, record the exact board/module revision, GPIO wiring, firmware commit, PlatformIO build logs, first boot `I` reply, `Q` reply, working display and sound results, BLE 10-cycle reconnect test and UART/Flipper replies. Do not mark any board as verified based only on running the simulator or native C++ parser.
