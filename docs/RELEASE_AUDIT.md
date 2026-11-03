# r0.2 engineering audit — corrections and evidence

## Why the revision exists

r0.1 validated the local simulator/API but did not prove that the ESP32 firmware would compile or that Flipper Momentum could communicate with physical hardware. This revision concentrates on verifiable software equivalence and community testing boundaries.

| Issue in r0.1 | Corrective work in r0.2 | Evidence / remaining risk |
| --- | --- | --- |
| ESP32 used `strtof` with acceptance of exponents or signs, but Python rejected them | Added C++11 pure parser consumed by firmware; host conformance test | Native C++ and Python grammar compared; firmware not flashed |
| No protocol identity check | Added read-only `I` command and ID reply | Python tests and source inspection; physical replies unverified |
| Serial loop could wait through many long serial timeouts | Added fixed 3s deadline with short serial reads | Code-level fix; needs physical serial testing |
| Local web dashboard accepted cross-origin WebSocket connection | Added Origin/Host checks, plus Origin check on unsafe HTTP methods | Local ASGI security tests; not a public authentication mechanism |
| GPS values could flood the command bridge | Rate-limited change transmissions to at most 1Hz | Source-level fix; browser/device GPS not independently verified |
| Only one community test route | Added board porting, V3 discovery, evidence matrix and backlog | Documents; community reproduction pending |
| Hardware status could be mistaken for verified | Strengthened first-run and release gates | **No actual ESP32/Flipper/Mochi device has been tested in this environment** |

## Verification tiers

1. **Source reviewed:** design or code examined, no code execution.
2. **Tested in simulator:** Python API and browser command behaviour, not radio or electronics.
3. **Compiled host-native:** C++ parser compiled on PC; not full embedded firmware.
4. **Compiled for target:** PlatformIO reports a successful ESP32-S3 build (not achieved in this environment).
5. **Verified on hardware:** precise board revision, firmware hash and evidence from a physical tester.
6. **Reproduced independently:** at least two builders follow the same instructions and obtain comparable results.

## Out of scope for r0.2

- Production secure BLE authentication/bonding or encrypted audio.
- Streaming internet push-to-talk, voice capture and text-to-speech through Mochi.
- Factory Dasai Mochi V3 bootloader, firmware, display or USB data compatibility.
- Native iOS/Android BLE clients or background operation.
- Reliable protocol multiplexing of simultaneous serial and BLE command origins.
- A battery-powered assembly and all associated electrical safety testing.

Open a dedicated issue for each missing feature rather than representing an aspirational diagram as completed work.
