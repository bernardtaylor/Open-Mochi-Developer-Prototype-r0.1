# Changelog

## 0.2.0 — 2026-11-02 (developer preview)

- Created a shared host-compilable C++11 MOCHI/1 command parser and tested it against the Python simulator.
- Rejected noncanonical speed forms consistently (exponents/signs/whitespace).
- Added the read-only `I` protocol identity command (`ID:0.2,sim` / `ID:0.2,esp32s3`).
- Bounded the desktop serial command response loop to a three-second deadline.
- Added Host and Origin checks on the loopback developer gateway; still not suitable for public network exposure.
- Rate-limited GPS speed updates through the browser control page.
- Added cross-language conformance/security tests, community issue backlog, board porting, V3 discovery and release gates.
- Confirmed Python test suite, JavaScript syntax and local API play-test in the development environment.
- Added explicit VERSION file and documented prompt-to-GitHub release/versioning policy, canonical repository and README maintenance rules.

**Not completed:** Full ESP32 PlatformIO build/flash, BLE bench testing, Flipper/Momentum runtime test, physical V3 inspection, voice streaming, AI microphone integration or native mobile applications.

## 0.1.0 — initial experimental developer reference

- Python simulator/command gateway, browser dashboard, UART/BLE reference firmware source, Flipper script, tests and community docs.