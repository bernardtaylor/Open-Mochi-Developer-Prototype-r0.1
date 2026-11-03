# Prompt-to-GitHub release policy

Canonical repository: https://github.com/bernardtaylor/Open-Mochi-Developer-Prototype-r0.1

## Versioning
- Project version: `VERSION` and `pyproject.toml`, using SemVer.
- Protocol version: `MOCHI/1` and `ID:0.2,...`, updated only when wire compatibility changes.
- Hardware revisions: tracked separately and never implied by software release numbers.

## Workflow for each change made in an active chat
1. Read the latest repository contents and preserve independent community work.
2. Implement the requested changes with focused tests.
3. Bump project version when source or documentation changes warrant it; pure discussion does not create a release.
4. Update `VERSION`, `pyproject.toml`, `CHANGELOG.md`, `README.md`, and affected protocol/wiring/test documents.
5. Commit source changes with an informative message, preferably on a branch with a PR; review and test before merging unverified hardware code.
6. Document actual test results, external dependencies, known limitations and hardware safety.
7. Publish version tags and releases once verification gates pass.
8. Report GitHub commit/PR URLs and the exact published version in the chat.

There is **no unattended background publishing**. Each change must be published in an active session with GitHub access. Do not upload proprietary factory firmware, assets, credentials, private GPS data, personal identifiers or unsafe unverified hardware instructions.

## Release gates
- Automated simulator and Python checks pass.
- Cross-language protocol tests pass if the C++ toolchain is available.
- ESP32 PlatformIO firmware build is verified before declaring binary releases.
- Physical compatibility requires explicit board, revision, wiring and evidence.
- Flipper/Momentum runtime support and factory Mochi V3 modification remain unverified until tested.
