# Contributing

Thank you for testing an experimental project. Start with `README.md` and `docs/TEST_PLAN.md`.

1. Open an issue describing the feature or reproduction failure before a major redesign.
2. Include exact board / operating-system / Momentum version, circuit or wiring and revision.
3. Run `python -m pytest -q`; add a unit test for protocol or gateway changes.
4. Do not submit proprietary Mochi firmware, copyrighted character assets, private BLE addresses, coordinates, passwords or raw device dumps containing identifiers.
5. State **which capabilities were physically tested** and which remain hypothetical.
6. Make small pull requests with rationale, safety considerations and documentation updates.

External hardware is never assumed to be electrically compatible based on connector shape or marketing names. Community communication and safety policy are in `docs/COMMUNITY.md` and `SECURITY.md`.
