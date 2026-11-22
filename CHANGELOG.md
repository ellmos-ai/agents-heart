# Changelog

## [Unreleased]
### Added
- Cross-OS CI matrix workflow (`.github/workflows/ci.yml`: Ubuntu/Windows/macOS on Python 3.11–3.13 with `workflow_dispatch` and `contents: read` permissions), Dependabot configuration (`.github/dependabot.yml`), and bilingual issue templates (`.github/ISSUE_TEMPLATE/`).
- Bilingual governance documentation (`CODE_OF_CONDUCT.md`, `SECURITY.md`, `CONTRIBUTING.md`) and LLM entrypoints (`SKILL.md`, `llms.txt`, `llm.txt`).
- Expanded PEP 621 metadata (`keywords`, `[project.urls]`, `[project.optional-dependencies].dev`), hardened `[tool.pytest.ini_options]` without relative `--basetemp`, and standardized `[tool.ruff.lint]` rules in `pyproject.toml`.
- Additional unit and metadata contract tests in `tests/test_agents_heart.py` and `tests/test_metadata.py`.

### Changed
- Cleaned `src/agents_heart/__init__.py` and test imports/type annotations (`UTC`, `dict[str, Any]`) to satisfy `ruff check .` with zero warnings.
- Hardened `.gitignore` with agent directory, lock-cache, marketing-log, and debug artifact patterns.
- Synchronized `README.md` and `README_de.md` with badges, language switchers, installation/testing sections, and governance/LLM references while keeping version `0.2.0` unchanged.

## [0.2.0] - 2026-10-31 / 2026-11-05
### Added
- Standalone package layout (`src/agents_heart/__init__.py`, `pyproject.toml`, `ellmos-module.v2.json`).
- `delete_worker_profile` and `ProfileDeletionRejected` moved into `agents-heart` (Task #2103).
- Release readiness: MIT `LICENSE`, standardized `TODO.md` with status matrix, `.gitignore` release-gate hardening (10/10 PASS).
- PEP 561 typing marker `py.typed` and package data declaration.
- Bilingual documentation: comprehensive English `README.md` and German `README_de.md`.
- Expanded test suite (16 tests) with comprehensive validation logic and contract tests in `tests/test_metadata.py`.
