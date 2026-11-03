# Runtime architecture and software scope

```text
                Phone or PC (r0.2 = PC browser only)
                GPS input / commands / optional local AI text
                              |
                   localhost Python gateway
                        |             |
                    simulator      serial / BLE
                                        |
                     ESP32-S3 reference board (NOT factory V3)
                     |  ST7789  |  I2S MAX98357A  |  UART
                                                   |
                                          Flipper Zero / Momentum
```

`MOCHI/1` carries only bounded ASCII control messages. The source supports **no direct audio streaming**, GPS coordinates, NFC traffic, device authentication or remote PTT service. Smartphone GPS and voice interactions are future development deliverables; the current browser can use geolocation only where the browser/security context allows it.

Data plane separation for a later version:
- **Control plane:** versioned UART/BLE messages, event types, animation/telemetry updates, secure pairing, reply correlation.
- **Audio plane:** smartphone audio or an explicitly designed wireless audio transport with codec/latency/buffering tests.
- **Internet plane:** phone or gateway-mediated authenticated service; no public Wi-Fi listener on the reference firmware.

Avoid making Flipper a mandatory component. The hardware abstraction should allow native ESP32 control as well as optional Flipper expansion.
