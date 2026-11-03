# MOCHI/1 protocol · revision 0.2

A tiny ASCII control protocol, independent of carrier transport. Deliberately excludes audio, identity, geolocation coordinates and cloud secrets. The same syntax works in the Python simulator, firmware BLE write characteristic, USB serial and Flipper UART.

## Transport

- **UART/USB:** 115200, 8-N-1, one message per line ending with `\n`. Maximum **20 printable ASCII bytes excluding newline**.
- **BLE GATT:** one command per characteristic write, **20-byte maximum**. Do not append newline. Only control data, not audio. Test with a normal central: the GATT server is `OpenMochi-r0` (name retained for pre-1.0 discovery compatibility).
- **Event/status:** ASCII notifications on the separate characteristic, and responses over the UART origin channel.

| Field | UUID |
| --- | --- |
| Service | `8ef6c3e0-6d43-4a81-891e-e9e380720001` |
| Write (central → Mochi) | `8ef6c3e0-6d43-4a81-891e-e9e380720002` |
| Notify/read | `8ef6c3e0-6d43-4a81-891e-e9e380720003` |

## Commands

| Message | Description | Typical response |
| --- | --- | --- |
| `E:happy` | Set one of `neutral`, `happy`, `surprised`, `sleepy`, `listening`, `talking`, `sad` | `OK:E:happy` |
| `V:42.5` | Update speed in **km/h**, range 0..250 | `OK:V` |
| `S:1` | Play local tone preset 1, 2 or 3 | `OK:S` |
| `P:1` | PTT button pressed / 0 released (**event only, no audio**) | `OK:P` |
| `Q` | Query device state | `ST:happy,42.5` |
| `I` | Identify protocol implementation | `ID:0.2,sim` or `ID:0.2,esp32s3` |

Outputs: `OK:*` means accepted, `ERR:*` means rejected, `ST:<expression>,<speed>` is a state reply. Responses do not include user identifiers. Invalid messages should be rejected with no state mutation. Maximum payload sizes are intended to work without BLE fragmentation at the minimum ATT MTU.

## Design caveats and future version

- Asynchronous telemetry, correlation IDs, signed commands, replay control, capability negotiation and retransmission are **not** in revision 0.2.
- The same BLE event characteristic broadcasts replies from all origins; multi-controller sessions could receive each other's acknowledgements. Restrict to one controller for r0.
- Desktop Python and ESP32 share the same admissible speed grammar (nonnegative decimal, no sign/exponent, 0..250); `firmware/include/mochi_protocol.h` is compiled natively and checked against Python in `tests/test_conformance.py`. On-device behavior still requires hardware verification.
- For protocol version 1: add `HELLO`, feature flags, unique device identifier, protocol negotiation, framed binary messages, CRC/sequence numbers for serial transports, secure BLE pairing, event subscription and stable OTA rollback.
- For voice: use a **separate** transport (phone audio, WebRTC, or audio-capable dedicated Wi-Fi path). Do not try to squeeze live audio through these GATT writes.

## Strict syntax and reproducibility

- Command payload is 1–20 printable ASCII bytes. `I`, `Q` are standalone.
- Speed accepts `V:0`, `V:42.5`, `V:.5`, `V:250.000`; refuses exponents (`V:1e2`), signs (`V:+1`), whitespace and values above 250.
- `Q` and `I` are read-only; invalid commands must not mutate state.
- The C++ parser and Python validator agree in host-native tests. Serial framing and BLE delivery have **not** undergone physical hardware validation.
- `ID:0.2,...` is informational identification only, not secure authentication or a robust version-negotiation handshake.
- The UART and BLE protocols are *control only*. Live audio, credentials, GPS coordinates and user data must never be sent with MOCHI/1.
