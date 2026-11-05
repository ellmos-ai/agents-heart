# Changelog

## [0.2.0] - 2026-10-31 / 2026-11-05
### Added
- Standalone package layout (`src/agents_heart/__init__.py`, `pyproject.toml`, `ellmos-module.v2.json`).
- `delete_worker_profile` and `ProfileDeletionRejected` moved into `agents-heart` (Task #2103).
- Release readiness: MIT `LICENSE`, standardized `TODO.md` with status matrix, `.gitignore` release-gate hardening (10/10 PASS).
- PEP 561 typing marker `py.typed` and package data declaration.
- Bilingual documentation: comprehensive English `README.md` and German `README_de.md`.
- Expanded test suite (16 tests) with comprehensive validation logic and contract tests in `tests/test_metadata.py`.
