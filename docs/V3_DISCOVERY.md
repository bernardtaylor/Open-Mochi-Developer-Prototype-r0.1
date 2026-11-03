# Factory Dasai Mochi V3 — non-destructive research only

**No factory board support is included.** A photograph is evidence of component markings, not proof of software reflashability.

## Contributor observation record

- Device edition / retail model and approximate acquisition year (avoid serial number).
- High-resolution images of PCB front and back, obscuring serials and QR IDs.
- Main IC markings and labelled display/sensor/audio devices.
- USB-C port data wiring observation, without applying external voltage to unknown pads.
- USB enumeration under Windows/Linux/macOS with a known data cable, if any.
- Read-only UART logs or debug interface identifications from a qualified electronics tester.
- PCB power rails and pin levels only when safely measured by someone competent.
- Factory firmware recovery options established before any erase/write experiment.

Do **not** submit firmware dumps, private pairing identifiers, proprietary animation assets, potentially dangerous battery alterations, or potentially copyrighted binaries. Do not assume UART pins based on a connector's position or bridge power rails between Flipper and Mochi.

## Decision gate

- **Direct firmware route:** bootloader/interface and recovery demonstrated on original board.
- **Secondary controller route:** a verified peripheral or control bus with usable protocol exists.
- **Replacement route:** screen, audio and power interfaces confirmed compatible with a replacement controller.
- **Fallback:** independent Open Mochi Maker reference device remains supported regardless of V3 findings.
