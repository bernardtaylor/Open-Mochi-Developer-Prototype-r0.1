# Open Mochi · developer prototype v0.2.1

> **Community engineering reference, not a firmware update for a factory Dasai Mochi V3.** Independent experimental project. Not affiliated with Dasai or Flipper Devices. No original factory firmware, artwork or sound assets are included.

A reproducible path toward a modular animated companion that can interact with Flipper Zero (including Momentum Firmware) and, later, phone-based GPS/AI/PTT systems. **This release implements only local expressions, simple sound effects, serial/BLE commands and a browser test harness.** Release v0.2.0 adds an embedded/desktop protocol conformance validator, an `I` identity command, a bounded serial reply timeout, basic localhost host/origin guards, and expanded tests.

## Source of truth and update process

**Canonical GitHub repository:** [bernardtaylor/Open-Mochi-Developer-Prototype-r0.1](https://github.com/bernardtaylor/Open-Mochi-Developer-Prototype-r0.1). Despite the historical repository name, releases are versioned by `VERSION` and `pyproject.toml`, not by renaming the repository.

New code/docs changes requested in ChatGPT should be published with a version bump when appropriate, updated README and changelog, tests and a traceable commit or pull request. This requires an active connected GitHub session; no unattended background sync is implied. See [docs/RELEASE_PROCESS.md](docs/RELEASE_PROCESS.md). The protocol version (`MOCHI/1`) and hardware revisions are separate from the software release version.

## Proposed next product direction (RFC — not implemented)

[**RFC-0001: Local-first community IoT hub, mobile app, AI and device editions**](docs/RFC-0001-LOCAL-FIRST-COMMUNITY-HUB.md) describes a proposed BLE-first companion experience with optional Home Assistant/MQTT and cloud/social extensions. It is research and roadmap documentation, not support for a working cloud app. v0.2.1 is a **documentation-only** release; the firmware and simulator capabilities remain those of v0.2.0.

## Demonstrated / not demonstrated

| Capability | Status |
| --- | --- |
| Desktop simulation, REST API, dashboard | Implemented; local automated tests |
| Protocol parsing & simulator state changes | Implemented; tested against C++ firmware parser |
| ESP32-S3 240×240 ST7789 cartoon face | Source supplied; **hardware build not verified** |
| MAX98357A I²S synthesised sound effects | Source supplied; **hardware build not verified** |
| ESP32-S3 UART / USB serial commands | Source supplied; hardware not verified |
| BLE GATT control (not audio) | Source supplied; hardware not verified, **no BLE authentication** |
| Flipper Momentum JS UART script | Source supplied; **not tested against user's installed Momentum build** |
| Browser geolocation speed to controller | Implemented in dashboard; requires usable GPS speed and browser permission |
| Native Android/iOS app, hands-free audio, cloud AI, remote PTT | **Not implemented** |
| Local Ollama text response and browser speech | Opt-in integration; **requires running Ollama/model, not tested here** |
| Dasai V3 factory board detection, flashing, peripheral support | **Not implemented** |

## Quickest way to play-test: no hardware

1. Install **Python 3.10+**.
2. From repository root:

   ```bash
   python -m venv .venv
   # On Windows PowerShell: .venv\\Scripts\\Activate.ps1
   # On Linux/macOS: source .venv/bin/activate
   python -m pip install -e ".[test]"
   python -m pytest -q
   python -m gateway.app --mode sim
   ```

3. Open **http://127.0.0.1:8765** on **that same computer**.
4. Try **Identify protocol**, **Happy**, **Sound 1**, manual speed **42 km/h**, **Hold PTT**, and **Q**.
5. In the console, confirm `ID:0.2,sim` and replies `OK:E:happy`, `OK:S`, `OK:V`, `OK:P`, `ST:happy,42.0`.

This tests protocol + UI. It does **not** prove your original Mochi hardware is controllable. No hardware, account, API key, cloud subscription or GPS is required for this mode.

### Testing the REST API without opening a browser

```bash
curl -X POST http://127.0.0.1:8765/api/command \
  -H 'Content-Type: application/json' -d '{"command":"E:happy"}'
curl http://127.0.0.1:8765/api/state
```

**Windows PowerShell** (avoids `curl` alias differences):

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8765/api/command -ContentType application/json -Body '{"command":"E:happy"}'
```

## Audit notes for r0.2

- [docs/RELEASE_AUDIT.md](docs/RELEASE_AUDIT.md) — findings, corrections, and real test boundaries.
- [docs/ISSUE_BACKLOG.md](docs/ISSUE_BACKLOG.md) — prioritised community GitHub issues.
- [docs/BOARD_PORTING.md](docs/BOARD_PORTING.md) — how to add a supported controller without breaking the protocol.
- [docs/V3_DISCOVERY.md](docs/V3_DISCOVERY.md) — safe, non-destructive factory Mochi hardware research.
- [docs/RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md) — explicit gates for publishing firmware binaries.

The C++ protocol parser in `firmware/include/mochi_protocol.h` is used by the ESP32 application and can be compiled natively by a host compiler for automated conformance against Python. The Python tests skip that cross-language check if no C++ compiler is installed; CI must use one. Hardware is **not** verified by compiling the parser on a PC.

## Stage 1 hardware: independent ESP32-S3

Reference target is an Espressif **ESP32-S3 DevKitC-1**, external **240×240 ST7789 SPI display**, optional **MAX98357A I²S amplifier and suitable speaker**, and optional Flipper serial control.

- Wiring and power rules: [docs/WIRING.md](docs/WIRING.md)
- Firmware build: [firmware/README.md](firmware/README.md)
- BLE / USB / UART protocol: [docs/PROTOCOL.md](docs/PROTOCOL.md)
- Suggested BOM: [docs/BOM.md](docs/BOM.md)

Run PlatformIO:

```bash
cd firmware
pio run
pio run -t upload
pio device monitor -b 115200
```

**Do not flash this firmware to the original Mochi V3 or Flipper Zero.** It is intended for the independent ESP32-S3 development board. Display/audio can be disabled in `firmware/include/config.h` for a USB/BLE/UART-only smoke test. The source has not been compiled or flashed against physical hardware in this environment; expect board-specific tweaks and report them.

## Stage 2 gateway: connect development hardware

From repo root, after flashing the reference ESP32:

```bash
python -m pip install -e ".[serial]"
python -m gateway.app --mode serial --serial COM5
# Linux example: --serial /dev/ttyACM0
```

Or BLE (using a desktop BLE adapter):

```bash
python -m pip install -e ".[ble]"
python -m gateway.app --mode ble
```

The web UI stays at `http://127.0.0.1:8765` on that computer. Serial-port names, BLE permission and BLE device names vary. The gateway has basic error handling, but no robust reconnection strategy yet. Close serial monitors before taking a serial port with the gateway.

**Mobile browser caveat:** The dashboard is a local developer tool, not a cross-platform native app. A phone can't ordinarily reach a computer's `127.0.0.1`. Its GPS requires HTTPS or a secure-origin exception. Android/iPhone native BLE development is a separate deliverable; do not assume Safari supports Web Bluetooth.

## Optional local AI text demonstration

The gateway includes an **opt-in local Ollama text adapter** (no microphone or hardware speech output). Install and run Ollama separately, download a model with `ollama pull MODEL_NAME`, then run:

```bash
python -m gateway.app --mode sim --ollama-model MODEL_NAME
```

Ask a question in the dashboard. The model runs on **your computer**; the browser may read the response aloud. The firmware receives only a `talking` expression, never the text or an audio stream. The model cannot send arbitrary device commands. Ollama usage requires its own installed binary/model and sufficient local CPU/GPU resources. The official `/api/generate` format uses `stream:false`. <https://docs.ollama.com/api>

**No local AI was actually run in this environment.** Default behaviour when omitted is HTTP 501 (disabled).

## Stage 3 Flipper Zero running Momentum

The [Flipper JavaScript script](flipper/mochi_control.js) is a sample controller for **the independent ESP32 board**, not a Mochi V3 USB interface. It sends ASCII commands over **Flipper USART GPIO**, with correct TX/RX crossover and a common GND. Verify 3.3 V levels; never join independent power rails. The script's current API has been based on official Flipper JS serial/UI examples, but must be tested on the specific Momentum release.

See [docs/WIRING.md](docs/WIRING.md) and [docs/TEST_PLAN.md](docs/TEST_PLAN.md).

## Project boundaries and trust model

- **No internet service** is used by this release. No model API keys or audio recordings are stored.
- Gateway binds to loopback only, has no authentication, and **must not be publicly exposed**.
- **Prototype BLE is unauthenticated**. It can cause display/sound changes; test only in controlled environments. Do not use while driving or transmit secrets.
- Do not connect to original Mochi PCB until rails, logic levels, display bus, charging system and safe recovery have been verified.
- All custom example expressions are original geometric drawings. No extracted Dasai firmware/artwork is included.
- Momentum source is GPL-3.0; this repo's MIT examples **do not include or vendor Momentum code**. Respect licences before copying third-party sources.

## Join the community / what we need most

Read [docs/COMMUNITY.md](docs/COMMUNITY.md), then reproduce the simulator tests, report your board model/OS, or contribute an independently verified pinout, driver, test case or accessible build guide. We particularly need **non-destructive photographs and identified component markings** from genuine Mochi V3 hardware (without serial numbers or personally identifying details), and **verified Flipper/Momentum interoperability reports**.

**Release status: experimental developer r0.2. Not a certified product, not a production security architecture, and not endorsed by any hardware manufacturer.**
