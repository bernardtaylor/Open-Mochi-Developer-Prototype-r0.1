# RFC-0001: Open Mochi Local-First Community Hub
Status: **Proposed / architectural research only** · 2026-11-03 · documentation version 0.2.1

## Decision
Develop Open Mochi as an independent, local-first animated companion ecosystem. Treat compatibility with the proprietary Dasai Mochi V3 hardware as an adapter research track, not the core dependency. Continue using MOCHI/1 only for reference low-bandwidth device commands until a versioned transport-neutral next protocol is implemented and tested.

## Product surfaces
- **Device:** low-power expression renderer with offline animations and optional motion, button, sound; ESP32-S3 voice reference and economical keychain-class reference should not be forced into one PCB. Keep factory V3 status unverified.
- **Phone app:** native Android/iOS BLE central, offline-first SQLite storage, optional live GPS/speed, event rules, character/gallery preview, BLE provisioning, device keys, optional internet account, friends and AI. Prefer Flutter for one UI codebase with native service plugins for BLE and location, not a browser-only PWA.
- **Local Hub (optional):** Raspberry Pi/PC/Home Assistant + Mosquitto bridge. Local MQTT for rules and IoT integrations; only explicitly permitted actions from trusted integrations.
- **Community Cloud (optional):** identity, social permissions, device registration, animation metadata/packs, moderation, remote events, backups and remote voice/AI gateway. Never required to display a local expression.
- **Developer SDK:** open capability manifest, device simulator, reference adapters and signed/validated animation packs.

## Connectivity tiers
1. No network: built-in expressions, local button/IMU events, cached packs, no speech-to-cloud.
2. Phone nearby/no internet: BLE commands, phone GPS-derived *local speed/drive state*, local phone STT/TTS when available, cached user rules; no global friend messages.
3. Local LAN hub: device-to-device events and home integrations through authenticated MQTT; device can connect through phone or a Wi-Fi bridge; no public cloud dependency.
4. Internet: cross-user greetings, presence, moderated community content, optional AI and voice calls. Use explicit opt-in, account auth, and revocable sharing.

## Architecture and transport boundaries
```
Device (display + local rule engine) <--BLE GATT--> Native Phone App
    | optional UART/Wi-Fi bridge                 |-- SQLite cache + mobile GPS
    |                                            |-- HTTPS/WS cloud client (opt-in)
    +--- optional LAN MQTT adapter ---> Local Hub (Mosquitto / Home Assistant)
                                                  |
Optional community backend: Auth + ownership + event router + content catalog + AI gateway
                                                  |
Optional LiveKit/WebRTC voice rooms (separate media path; phone audio initially)
```
- Preserve MOCHI/1 as a small ASCII command implementation without adding user identity, secrets, live GPS, audio or cloud data.
- Design **new proposed** openmochi.event.v1 for app/hub/cloud *above* the legacy MOCHI/1 adapter: `event_id`, `schema`, `source_device`, `kind`, `time`, `ttl_ms`, `capabilities`, `payload`. Carry routing, ownership and authentication outside the device command grammar. No implementation exists yet.
- Prioritise commands `animation.set`, `sound.play`, `mode.set`, `presence.update`, `battery.status`, `button.ptt`. Audio/media over WebRTC or a dedicated codec/transceiver, **not** existing 20-byte BLE writes.
- Trust boundaries: authenticated accounts; factory device reset/reclaim; short-lived session credentials; per-device key material; scoped invite-only community channels; signed or allowlisted content; sender block/report; opt-in location sharing; no retention of raw GPS by default.
- Do not expose the current loopback-only FastAPI developer gateway to public networks. Build and security-review a separate service.

## IoT interoperability
- **Home Assistant + ESPHome/Mosquitto**: preferred local bridge for existing compatible devices. Require explicit connector permissions; a generic IoT device cannot be controlled merely because it is on a network.
- **ESP RainMaker Neo**: alternative ESP32 device provisioning, fleet and app SDK built on user-owned AWS account; evaluate SDK licensing/costs before adoption.
- **ThingsBoard CE**: alternative device management/multitenancy; likely excessive for first 100 users.
- **Matter/Thread**: optional future bridge for appropriate standard device types. Character animations and social presence need custom application APIs; ESP32-S3 alone lacks 802.15.4 Thread radio.
- **Supabase/Postgres + Realtime**: possible first community backend; adopt fine-grained row-level authorization, not default public channels.
- **Cloudflare Durable Objects/WebSockets**: another realtime coordination path; avoid lock-in until the product/tenant model is validated.
- **LiveKit**: optional self-hosted/managed voice/agent path after user accounts and reliable native background audio work.
- **EMQX**: do not assume current broker release is freely redistributable in a hosted commercial platform: 5.9+ uses BSL 1.1; prefer Mosquitto in open reference stack.

## Consumer device editions
| Edition | Hardware intent | Primary use |
| --- | --- | --- |
| Keychain | minimal BLE SoC, tiny display, battery, button; phone handles GPS/voice/cloud | ambient reactions + shared greetings |
| Car companion | ESP32-S3 + colour screen/IMU + sound; optional microphone and car-safe mount | drive-mode reactions + assistant via phone |
| Desk/Home | ESP32-S3 Wi-Fi + screen/audio; optional Home Assistant/MQTT | animations + home automations |
| Factory V3 | unknown MCU and peripheral interfaces | independent reverse engineering track |
| Flipper/Momentum | existing user-owned Flipper via UART/BLE adapter | optional expansion/tool, not core dependency |

## Phone app and UX
- Onboarding without registration: pair over BLE, confirm physical button/proximity, name device, choose character, demonstrate offline animation.
- User may optionally create account to back up custom packs, invite friends or use hosted AI/PTT.
- Save default reactions and small animation packs locally; sync later and handle explicit merge conflicts.
- Driving profile: non-distracting dimming, silence and motion rules; no text interaction required while driving.
- iOS: Core Bluetooth background modes/state restoration and location background sessions require measured device testing; not equivalent to an always-on daemon. Android: foreground service/Companion Device Manager and user-visible permissions require proper implementation. PWA Web Bluetooth is not a reliable cross-platform BLE foundation.
- Voice: phone microphone and speaker first, device output hardware later; no indefinite passive microphone capture.
- Keychain: no continuous cloud socket or GPS radio assumed; phone-mediated events and periodic low-duty-cycle BLE.

## Community packs and extensibility
- Published pack manifest: `pack_id`, `version`, `author`, `license`, `min_protocol`, `capabilities`, `assets`, `limits`, `hashes`; sandbox content and bound animation frame rate/duration/volume.
- User-created artwork/audio must be original or appropriately licensed; do not redistribute Dasai factory assets.
- Moderation, takedown, abuse reporting, privacy controls, device revocation and abuse-resistant invitations are mandatory before public social features.
- Test SDK against simulated devices, not solely genuine factory Mochi hardware.

## Phased delivery and measurable gates
- **M0** Existing v0.2.0 baseline: simulator + MOCHI/1 parser, source for ESP32 and Flipper. Hardware/BLE security not validated.
- **M1** Two independently validated ESP32 reference builds, verified pinout/audio/display, 20 manual reconnect cycles, no unexpected writes; publish exact test logs.
- **M2** Android and iOS native BLE clients: pair/reclaim, animations, local speed, SQLite cache; demonstrate no-account/no-internet operation and document locked-phone limits on both OSes.
- **M3** Local hub adapter: Mosquitto + Home Assistant integration for at least 2 real supported IoT events, ACL tests and disconnected reconnection tests.
- **M4** Opt-in multi-user beta: device ownership/transfer, invited pairs, remote hello, consent controls, block/report, abuse tests, latency observation.
- **M5** Animation pack author tooling and content distribution with integrity validation and licence metadata; 2 independent community-created packs.
- **M6** Optional text AI, then voice/LiveKit/PTT after security and background audio validation. Avoid promising always-on voice for tiny battery-powered keychains.
- **M7** Product hardware: enclosure, battery, thermal, RF, USB, supportability and factory V3 adapter feasibility; regulatory sign-off before consumer sales.

## Product success metrics (proposed targets, not demonstrated)
- First animation without account/internet; onboarding in a few minutes on a known phone/board combination.
- Local action-to-expression latency and reconnect behaviour recorded at 50th/95th percentile, not asserted until measured.
- 2 independent community builders can reproduce the same board/firmware/version tests.
- A user can revoke sharing/delete cloud data, unpair/reclaim hardware, and stay functional offline.
- No unauthenticated remote display/audio injection, no default exact GPS sharing, no automatic recording.

## Commercial and legal gate
UK consumer connectable product security requirements effective 29 April 2024; review PSTI applicability, statements of compliance, support period, vulnerability reports, UKCA/CE/radio/WEEE/battery standards and appropriate safety evaluations before selling kits/devices. GPS and voice data can be personal information under UK GDPR; handle per-purpose permissions and retention. A keychain marketed for children triggers more stringent safeguards.

## Sources (research, not warranties)
- https://docs.flutter.dev/app-architecture/design-patterns/offline-first
- https://developer.android.com/develop/connectivity/bluetooth/ble/background
- https://developer.apple.com/library/archive/documentation/NetworkingInternetWeb/Conceptual/CoreBluetooth_concepts/CoreBluetoothBackgroundProcessingForIOSApps/PerformingTasksWhileYourAppIsInTheBackground.html
- https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API
- https://esphome.io/components/bluetooth_proxy/
- https://www.mosquitto.org/
- https://docs.neo.rainmaker.espressif.com/docs/phone-apps/home-app/
- https://thingsboard.io/docs/concepts/multi-tenancy/
- https://docs.livekit.io/intro/about/
- https://supabase.com/docs/guides/realtime/architecture
- https://github.com/emqx/emqx
- https://www.gov.uk/guidance/regulations-consumer-connectable-product-security
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/online-tracking/guidance-for-consumer-internet-of-things-products-and-services/what-information-do-iot-products-use/

## Open decisions
- Confirm reference phone app toolchain (Flutter recommended).
- Confirm market order: keychain vs car vs desk.
- Decide community backend after no-account local prototype evidence.
- Define app/firmware capability manifest and protocol v2 without breaking current MOCHI/1 clients.
- Prototype factory V3 only after MCU/display/USB identification.
