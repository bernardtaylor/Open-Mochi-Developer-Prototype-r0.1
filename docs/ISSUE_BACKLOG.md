# Prioritised public issue backlog (paste each row into a separate GitHub issue)

| Issue title | Priority | Type | Acceptance criterion |
| --- | --- | --- | --- |
| Confirm ESP32-S3 DevKitC-1 PlatformIO build | P0 | hardware/build | Exact board variant and compiler output attached; `I`/`Q` replies captured |
| Validate ST7789 physical wiring and seven expressions | P0 | hardware | Clear connection diagram and seven photographed states |
| Validate MAX98357A tones and safe sound levels | P0 | audio | Three tones play; wiring/power recorded, no overheating |
| Test official Flipper + Momentum serial script interoperability | P0 | Flipper | Document build, RX/TX, `I`/`Q`/expression replies, no stalled port |
| BLE 10-cycle connect/disconnect bench test | P0 | BLE | Every cycle reliably accepts command and reports notification |
| ESP32 queue saturation and malformed-frame response | P1 | firmware | Bounded response/timeouts under 100 rapid commands |
| Implement authenticated BLE pairing | P1 | security | Unpaired central cannot change expressions/sound; regression tests |
| Implement transport sequence/correlation ID | P1 | protocol | Reply tied to command under concurrent UART/BLE connections |
| Windows/macOS/Linux installation validation | P1 | docs | Two independent testers on each supported platform |
| Verify genuine V3 board MCU/display/USB without firmware writes | P1 | V3 research | Two reviewed redacted board photo reports |
| Android BLE reference client and foreground GPS | P2 | mobile | Documented permission, reconnect and speed updates |
| iOS BLE reference client and background constraints | P2 | mobile | Device-tested behaviour and failure conditions recorded |
| Microphone + speech output reference adapter | P2 | audio | Full duplex/half duplex test, measured latency and power |
| Internet PTT with authenticated users | P3 | service | Explicit opt-in, encrypted transport, no audio retention by default |
| Modular keyed accessory connector and board manifest | P3 | hardware | Electrical spec, reference schematic, two compatible modules |

Use labels: `good-first-issue`, `help-wanted`, `hardware-validation`, `Flipper-Momentum`, `protocol`, `security`, `V3-research`, `documentation`.
