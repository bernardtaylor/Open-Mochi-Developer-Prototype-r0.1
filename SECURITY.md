# Security policy and release status

**This is a developer prototype, not a secure internet-connected device.** The gateway accepts commands without authentication, but only binds to `127.0.0.1` by default. Never reverse-proxy or tunnel it onto a public address. The firmware's BLE service is also **unauthenticated**: anyone within BLE range who discovers it may send expressions/sounds. Do not transmit sensitive data or use it around untrusted people. ESP32-S3 Bluetooth features remain subject to hardware/software constraints.

Before any internet-connected public release, implement: authenticated BLE pairing/authorisation, replay protection, access-control states, secure provisioning, encrypted cloud transport, safe audio-consent UX, signed versioned firmware updates with rollback, secrets storage, rate limits and abuse controls.

Reports of potential security issues should go privately to the repository maintainers via GitHub's private vulnerability reporting after the repository is created. Avoid publishing real keys, device identifiers, user locations or full dumps. Until that method is configured, keep the prototype local and do not disclose unpatched issues through public demonstration endpoints.

Never connect Flipper GPIO to unidentified factory Mochi power rails. Avoid using radios outside applicable law or interfering with devices/networks you don't own or administer.
