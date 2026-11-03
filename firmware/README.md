# ESP32-S3 reference firmware

This is for a generic **ESP32-S3 DevKitC-1**, **not** the factory Dasai Mochi V3. Its ST7789 display and MAX98357A amplifier are external modules. Do not attempt to wire any original Mochi peripheral until the PCB has been identified.

Use `platformio run` to build; `platformio run -t upload` to flash; `platformio device monitor` for USB serial. The `platformio.ini` pins target the reference board, not the XIAO or Atom series.

If you only own an ESP32-S3 and no display/audio hardware, set `MOCHI_USE_ST7789` and `MOCHI_USE_I2S_SPEAKER` to `0` in `include/config.h` before building. Serial/BLE commands will still work. A blank screen or silent speaker with those settings is expected.

**BLE:** Advertises `OpenMochi-r0` with service and characteristic UUIDs in `config.h`. Each WRITE is exactly one ASCII command of at most 20 bytes; the NOTIFY characteristic publishes a short result. UART/USB commands must end in `\n`.

**IMPORTANT:** r0 BLE has no authentication or bond enforcement. Use only on the bench, do not transmit private information, and do not install publicly accessible unattended systems. A production build needs authenticated pairing/authorization and robust reconnect handling.

**Audio:** `S:1`, `S:2`, `S:3` emit simple synthesised tones via I²S. No microphone capture, recorded voice, speech synthesis, or Bluetooth voice streaming is implemented.


**Protocol parser:** `include/mochi_protocol.h` is a C++11 header used in `main.cpp`; `tests/test_conformance.py` compiles that same header on a PC and compares its accepted commands against the Python simulator. This catches input-grammar drift but is not a complete firmware build test.

**Firmware build boundary:** The reference `platformio.ini` is pinned to the PlatformIO Espressif32 6.12.0 Arduino toolchain, not the newest Espressif/Arduino release. A different Arduino core may require BLE or I²S API changes. Record exact compiler/build output when reporting problems.
