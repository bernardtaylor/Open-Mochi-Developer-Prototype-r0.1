# Suggested bench prototype parts (UK planning ranges)

These are **illustrative allowances**, not current offers or verified prices. Buy only after checking the exact connector layout and board revisions. You already own the Flipper Zero and factory Mochi V3; neither should be altered for the software simulator.

| Component | Quantity | Rough allowance | Notes |
| --- | ---: | ---: | --- |
| ESP32-S3 DevKitC-1 reference board | 1 | £8–£20 | Prefer board with USB and sufficient flash; verify pin accessibility |
| 240×240 ST7789 SPI TFT breakout | 1 | £5–£13 | Must match voltage and SPI wiring; not the original Mochi OLED |
| MAX98357A I²S amplifier | 1 | £3–£8 | Optional, for synthesised sounds |
| Suitable small speaker | 1 | £3–£9 | Match amplifier rating/impedance |
| Female/male jumper cables + breadboard | 1 set | £5–£12 | For non-permanent testing |
| USB data cable | 1 | £0–£5 | May already be owned |
| **Additional outlay** | | **~£24–£67** | Excludes tools, tax/shipping variations and future battery work |

Avoid adding microphone, GPS, LiPo/charger, NFC or sub-GHz radio until the command and sound/display path passes its acceptance tests. Those are later optional extensions.

## Planned follow-on hardware, **not implemented in r0**

- I²S or PDM microphone with verified ESP32-S3 support.
- Battery/charger protection and measured sleep current.
- Keyed expansion connector with a published electrical specification.
- Compact revision 1 PCB, physical controls, enclosure and strain relief.
- Optional Flipper expansion connector with appropriate mechanical fit.
- Original Mochi V3 display/audio adapter **only after verified pinout and protocol discovery**.
