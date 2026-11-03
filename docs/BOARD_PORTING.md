# Adding a new ESP32 / RP2350 / M5Stack reference board

The protocol is **board-independent**; electrical pinouts and drivers are not. A patch for one controller must not silently change the target for every contributor.

1. Create a separate PlatformIO environment or build profile for the specific commercially identifiable board **and hardware revision**.
2. Record MCU, Arduino/ESP-IDF core, flash/PSRAM, display controller, audio DAC/codec, GPIO mapping, radio/BLE availability, USB behavior and power circuit.
3. Do not copy `firmware/include/config.h` pin settings to a different PCB without checking schematic and strapping pins. Never join independent power rails.
4. Implement the character display and optional audio as platform-specific adapters; keep the `MOCHI/1` parser independent from display, sound or BLE code.
5. Reuse the fixed control grammar, including `I` and `Q`; if functionality is absent, report it through future capability negotiation rather than silently pretending support.
6. Add automated tests for parser or gateway changes, and submit first-boot serial logs, BLE service discovery and physical photos with serials redacted.
7. Register verified board and test results in `docs/HARDWARE_MATRIX.csv`. State clearly whether hardware evidence is available.
8. For community support, propose only boards with a stable toolchain, documented flash recovery procedure and accessible connectors.

**Factory Mochi exception:** A factory V3 adapter is not a generic ESP32 board. Treat its original MCU, flash and display as unknown until separately documented. Never run our ESP32 binary on it.
