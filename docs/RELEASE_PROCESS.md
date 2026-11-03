# Prompt-to-GitHub release policy

**Canonical repository:** https://github.com/bernardtaylor/Open-Mochi-Developer-Prototype-r0.1

Open Mochi has three independent version numbers:

- **Project release:** `VERSION` and `[project].version` in `pyproject.toml`, e.g. `0.2.0`. Follow SemVer (`MAJOR.MINOR.PATCH`). Before `1.0.0`, incompatible experimental changes may increment MINOR.
- **Protocol:** `MOCHI/1` and advertised `ID:0.2,...`. Change only when wire-format/behaviour compatibility changes, never just because README/code changed.
- **Hardware revision:** separate board identifier/revision in documentation. A Python release is not evidence of physical compatibility.

## When a prompt creates a change

1. Audit current repository state and review the request; do not overwrite or replace community commits.
2. Implement a focused change. Avoid copying private data, credentials, GPS histories, personal identifiers, proprietary firmware or restricted assets into this public repository.
3. Test what is testable. Record commands and results; keep hardware validation explicitly pending unless physically demonstrated.
4. Bump project version: PATCH for fixes/docs, MINOR for new compatible features, and MAJOR for stable breaking changes. Pre-1.0 breaking changes use MINOR and a clear migration note. Pure discussion, research or prompt rewrites without repository changes **do not** require a new version.
5. Update `VERSION`, `pyproject.toml`, `README.md` version/status/quickstart when affected, and `CHANGELOG.md` with traceable changes and known limits. Update protocol, wiring, BOM, test matrix and security documentation if affected.
6. Commit to a descriptive branch and open a PR for code or hardware changes; perform review and verify checks before merging. Do not silently merge unverified firmware changes. Keep each change traceable to a commit/PR.
7. Prefer an annotated `vX.Y.Z` tag and GitHub release for validated releases, where GitHub tooling permits; document if tagging is not supported. Never describe a ZIP as a validated hardware release.
8. In each chat response, include repository link, resulting version, commit/PR, tests and limits. Publishing is performed during an active session with GitHub access; chats do **not** run autonomously in the background.

## Release acceptance gates

- Python test suite passes, and embedded protocol C++ checks run where toolchains are available.
- Hardware firmware PlatformIO build is verified on supported CI or listed as outstanding.
- Hardware claim needs a test report: board revision, pins/voltages, firmware hashes, logs, reproducible steps and recovery procedure.
- No unauthenticated radio or remote access is described as secure.
- Do not include private or proprietary material in public issues or source.
