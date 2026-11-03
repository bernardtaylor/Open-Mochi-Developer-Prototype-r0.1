# Release and public-test gate

## Before pushing public source

- [ ] Inspect files for private data, API keys, copyrighted/closed firmware and non-distributable assets.
- [ ] Select a non-confusing project name and explicitly disclaim manufacturer affiliation.
- [ ] Publish README, MIT licence for original code, code of conduct, contribution and security policies.
- [ ] Run Python unit tests; require a C++ compiler so parser cross-language test does not skip.
- [ ] Run `node --check` on scripts; clearly state that this is not a Momentum runtime test.
- [ ] Verify loopback-only gateway and prohibit public network exposure in docs.
- [ ] Check default branch protection and CI status before accepting pull requests.

## Before publishing a flashed firmware binary or 'compatible board' claim

- [ ] PlatformIO compilation succeeded on an explicitly named target toolchain.
- [ ] Firmware runs on the exact specified board revision; boot/flash/recovery tested.
- [ ] Verified board wiring, voltages, peripheral power, and no unsafe pin conflicts.
- [ ] UART and BLE service exercised, malformed inputs handled, 10 reconnects successful.
- [ ] Display/audio if enabled physically tested, with measured current draw where possible.
- [ ] Two independent builders complete the same procedure.
- [ ] Known BLE security limitations plainly documented; public unattended use prohibited.

## Before calling a genuine factory V3 retrofit 'compatible'

- [ ] Controller/flash, display bus and battery protections positively identified.
- [ ] Non-destructive backup and recovery plan exists.
- [ ] Tested against a reversible adapter or spare board, not only an owner's primary device.
- [ ] No proprietary assets or binaries redistributed without appropriate rights.
