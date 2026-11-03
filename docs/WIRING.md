# Reference hardware wiring (not Dasai V3)

**Target:** ESP32-S3 DevKitC-1 + external ST7789 240×240 SPI TFT + optional MAX98357A I²S amplifier/speaker. **All pin mappings are configurable in `firmware/include/config.h`.** ESP32-S3 board pin availability differs by manufacturer and module. This mapping must be reviewed against the exact board before applying power.

## Reference ESP32-S3 pins

| Function | DevKitC-1 GPIO | Peripheral connection |
| --- | ---: | --- |
| TFT SCLK | GPIO12 | ST7789 SCL/SCK |
| TFT MOSI | GPIO11 | ST7789 SDA/DIN |
| TFT CS | GPIO10 | ST7789 CS |
| TFT D/C | GPIO9 | ST7789 DC |
| TFT RESET | GPIO14 | ST7789 RST |
| I²S BCLK | GPIO4 | MAX98357A BCLK |
| I²S LRCK/WS | GPIO5 | MAX98357A LRC/WS |
| I²S DATA OUT | GPIO6 | MAX98357A DIN |
| UART RX (ESP) | GPIO17 | Flipper TX (USART pin 13) |
| UART TX (ESP) | GPIO18 | Flipper RX (USART pin 14) |
| Ground | GND | Common ground on every accessory |

**Flipper reference USART pin assignments** are in Flipper's official expansion-module documentation. The `serial.setup("usart",115200)` call opens that port. Do not confuse Flipper's physical pin numbering with its STM32 GPIO port numbering. <https://developer.flipper.net/flipperzero/doxygen/expansion_protocol.html>

## Power and signals

1. All ESP32 and Flipper **UART logic levels are 3.3 V**. Never connect 5 V logic outputs directly.
2. **Cross RX/TX**; Flipper TX → ESP RX, ESP TX → Flipper RX, and GND ↔ GND.
3. **Do not join 3.3 V/5 V/VBUS rails of two separately powered devices.** Only join ground and verified logic signals where safe.
4. Power the reference ESP32 by its own USB port during development. Power the TFT and amplifier **only according to their exact modules' documentation**. Different ST7789 boards have 3.3 V-only logic or onboard regulators. Never assume a breakout is 5 V tolerant.
5. MAX98357A must have a suitable speaker; do **not** connect a speaker directly to an ESP32 GPIO. Start with low software volume; speaker impedance/rating must be compatible with the amplifier.
6. A LiPo battery needs appropriate charging, cutoff, protection and mechanical retention. **Revision 0 uses USB power**, not an improvised LiPo wiring modification.
7. The factory Dasai V3 PCB is **not** electrically characterised. Do not apply this table to its ports, battery or peripherals.

## USB-C

Flipper Zero and Dasai both have USB-C connectors, but no verified Dasai USB host/device data interface or application protocol. A C-to-C cable is not an adapter for UART, and USB-C connectors do not guarantee an operational data path. Do not connect the two devices directly to attempt firmware flashing.

## Without an external display/speaker

Set `MOCHI_USE_ST7789` and/or `MOCHI_USE_I2S_SPEAKER` to `0` in `config.h` to run BLE/UART/USB only. This is the **preferred first electrical smoke test** on unfamiliar ESP32 boards.
