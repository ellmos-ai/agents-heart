# Contributing to agents-heart / Mitwirken an agents-heart

[English](#english) | [Deutsch](#deutsch)

---

## English

Thank you for contributing to `agents-heart`!

### Development Setup
1. Clone the repository into your local development workspace (`<LOCAL_DEV_REPOS>/agents-heart`).
2. Install in editable mode with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Create a dedicated feature branch (never commit directly to `main`).

### Quality & Contract Gates
Before opening a pull request, verify all checks locally:
```bash
git diff --check
ruff check .
python -m compileall -q src tests
pytest -ra -v
```

### Core Design Rules
- Keep `agents-heart` **provider-neutral** and **network-free** (`boundaries.network = "none"`).
- Preserve **fail-closed** semantics in `authorize_role`, `begin_assignment`, `finish_assignment`, and `delete_worker_profile`.
- Maintain bilingual documentation parity (`README.md` and `README_de.md`) and update `CHANGELOG.md` under `## [Unreleased]`.
- Never commit personal paths, hostnames, secrets, or lock files.

---

## Deutsch

Vielen Dank für deinen Beitrag zu `agents-heart`!

### Entwicklungsumgebung einrichten
1. Klone das Repository in deinen lokalen Entwicklungsordner (`<LOCAL_DEV_REPOS>/agents-heart`).
2. Installiere das Paket editierbar inklusive Dev-Abhängigkeiten:
   ```bash
   pip install -e ".[dev]"
   ```
3. Erstelle einen dedizierten Feature-Branch (niemals direkt auf `main` committen).

### Qualitäts- und Vertragstests
Prüfe vor einem Pull Request alle Gates lokal:
```bash
git diff --check
ruff check .
python -m compileall -q src tests
pytest -ra -v
```

### Zentrale Designregeln
- Halte `agents-heart` **anbieterneutral** und **netzwerkfrei** (`boundaries.network = "none"`).
- Bewahre die **fail-closed**-Semantik in `authorize_role`, `begin_assignment`, `finish_assignment` und `delete_worker_profile`.
- Pflege die zweisprachige Dokumentation (`README.md` und `README_de.md`) paritätisch und ergänze Änderungen in `CHANGELOG.md` unter `## [Unreleased]`.
- Committe niemals persönliche Dateipfade, Hostnamen, Zugangsdaten oder Lock-Dateien.
