# Community launch and contributions

## Objective

Build a **legally redistributable, repeatable Open Mochi reference device and protocol** while conducting a separate, evidence-led compatibility investigation for genuine Dasai Mochi V3 hardware. Public success is measured by *independent reproduction*, not stars/followers or a speculative feature list.

## Publishing the code (repo owner; external step)

1. Review every source file, repository name, logo and reference before publication. No extracted factory assets, credentials, serial numbers, unique pairing IDs or copyrighted artwork.
2. Create a GitHub public repository (suggested name `open-mochi-prototype`, or pick a distinct name to avoid implying official Dasai affiliation).
3. From this directory, run:

   ```bash
   git init
   git add .
   git commit -m "Initial experimental Open Mochi r0.1 reference"
   gh auth login
   gh repo create open-mochi-prototype --public --source=. --remote=origin --push
   ```

   `gh` is the optional GitHub CLI. Alternatively create a repository on GitHub and push to its configured origin. Publication requires action in **your own account**; this package has not created an online repository.
4. Enable issues and discussions; add issue labels `good first issue`, `help wanted`, `hardware verification`, `Momentum`, `BLE`, `documentation`, `security`, `V3 research`.
5. Enable branch protection, require pull-request review and Python CI, and prohibit committing binaries/credentials. Use release tags such as `v0.1.0-dev`; attach build logs and clearly state untested boards.
6. Set `Security Policy` to link `SECURITY.md`; configure a private vulnerability reporting method. Add a contributor licence policy if distribution terms change.

## Contributor on-ramps

| Type of contributor | First useful contribution |
| --- | --- |
| No hardware | Run simulator; submit a playtest report or UI bug |
| ESP32 hobbyist | Build the exact reference wiring; submit log/firmware version/video of function |
| Flipper + Momentum owner | Validate `flipper/mochi_control.js` serial menu and pinout |
| Factory V3 owner | Submit **redacted, non-destructive** PCB photos and markings, USB enumeration results |
| Mobile developer | Propose/implement native BLE adapter with permission and background-operation tests |
| Audio/AI developer | Define privacy-first audio tests; separate audio transport from control messages |
| Hardware/PCB engineer | Design keyed, protected add-on interface and measured power budget |
| Security tester | Add pairing, input fuzz tests, protocol negotiation, safe firmware rollback |

## Launch waves / decision gates

**Wave 0: 5–10 software-only testers.** Goal: someone unfamiliar with the project gets the simulator running from README on Windows, macOS and Linux. Collect setup blockers before asking people to buy parts.

**Wave 1: 3–5 independent ESP32 builders.** Gate: at least two different people confirm a reproducible *same-board* wiring/build, GPIO pin map, BLE and serial smoke tests. Maintain a per-board hardware matrix; do not generalise from one ESP32 to every ESP board.

**Wave 2: Flipper + Momentum testers.** Gate: verified UART script behavior with specific Momentum build and with official Flipper JS runtime. Report conflicts with Expansion Module service, pin naming and timing.

**Wave 3: genuine Mochi V3 owners.** Gate: identifiable processor/display/flash/USB data path with at least two independently reviewed board photos. Attempt firmware writes **only after** a documented recovery plan exists. Never distribute factory firmware images.

**Wave 4: standalone voice / app.** Gate: secure connection, permission handling, speech privacy, battery measurements, accessibility and multi-device PTT opt-in. Real-time voice and cloud AI are not release-0 features.

## Rules for requests and pull requests

- One change per PR, linked to an issue, with tests and documented board model.
- Label all claims `Verified on hardware`, `Verified in emulator`, or `Unverified hypothesis`.
- Repro steps, exact release/build, expected vs actual result. No screenshots showing secrets.
- No proprietary firmware dumps or original copyrighted animation/audio assets in public issues.
- Radio features must respect local regulations; don't accept contributions that enable unauthorised access or interference.
- Keep hardware abstractions independent of branded boards, with one documented configuration per board.
- Human review of electrical/safety changes before merging.

## What constitutes a successful community project?

- A newcomer can assemble and flash the **same documented reference kit** without direct help from the maintainer.
- The library's controls work through both an ESP32 and a simulator and produce identical observable results.
- Flipper is **optional**; the device is not disabled when a Flipper is absent.
- A V3 conversion is advertised only after independent electrical/firmware validation.
- All firmware/assets and instructions distributed in the public repo have redistribution rights.

## r0.2 launch discipline

Use `docs/ISSUE_BACKLOG.md` as initial issue seeds and `docs/RELEASE_CHECKLIST.md` for release gates. Request that each tester labels evidence as simulator, native C++ parser, on-target compiled, hardware verified, or independently reproduced. A board should not be marked supported because a forum post claims it works.
