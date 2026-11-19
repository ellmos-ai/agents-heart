<p align="center">
  <img src="assets/banner.svg" alt="agents-heart banner" width="100%">
</p>

# agents-heart (Deutsche Dokumentation)

[![Version](https://img.shields.io/badge/Version-0.2.0-blue)](pyproject.toml)
[![Python](https://img.shields.io/badge/Python-3.11%20|%203.12%20|%203.13-blue)](pyproject.toml)
[![Lizenz: MIT](https://img.shields.io/badge/Lizenz-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/pytest-23%20bestanden-brightgreen)](tests/)
[![Geprüft](https://img.shields.io/badge/geprüft-2026--11--19-informational)](CHANGELOG.md)

**Sprache / Language:** [English](README.md) | **Deutsch**

Provider-neutrales Control-Modul (`modul:agents-heart`, v0.2.0) für Worker-Rollenverträge, Besetzungs-Autorisierung und Profil-Lebenszyklus.

## Überblick

`agents-heart` fungiert als fail-closed Steuerungsschicht zwischen Orchestratoren und Laufzeitumgebungen. Das Modul trifft keine eigenmächtigen Modell- oder Backend-Entscheidungen, sondern kapselt drei wesentliche Kontrollfunktionen:

1. **Rollen-Autorisierung (`authorize_role`)**: Prüft fail-closed, ob ein geplanter Ausführungspfad die erforderlichen Rechte (`task.claim`, `task.execute`) besitzt.
2. **Besetzungs-Korrelation (`begin_assignment`, `finish_assignment`)**: Vergibt unveränderliche `Assignment`-Identitäten und zeichnet korrelierbare Start- und Endbelege auf (`assignment.started`, `assignment.ended`).
3. **Sicheres Profil-Löschen (`delete_worker_profile`)**: Garantiert Inaktivität, verifiziert das Erreichen des Terminal-Status (`phase == "terminal"`) aller archivierten Läufe und führt die geordnete Bereinigung durch.

## Installation

```bash
pip install -e .
```

Inklusive Entwicklungs- und Testwerkzeugen (`pytest`, `ruff`):

```bash
pip install -e ".[dev]"
```

### Installation & Integration mit deinem LLM

Lies [llms.txt](llms.txt) und [SKILL.md](SKILL.md) für kompakte API-Verträge und fail-closed Nutzungsregeln:

> *Prompt:* „Lies `llms.txt` und `SKILL.md` in `agents-heart`, installiere das Paket mit `pip install -e .` und integriere `authorize_role`, `begin_assignment`, `finish_assignment` sowie `delete_worker_profile`, ohne fail-closed Prüfungen zu umgehen.“

## Schnittstellen & Verwendung

### Rollen-Autorisierung

```python
from agents_heart import authorize_role, AssignmentDenied

# Rechtevertrag vor Ausführung prüfen
contract = authorize_role("task_worker", mode="full")
assert "task.claim" in contract.rights
assert "task.execute" in contract.rights

# Nicht autorisierte Rollen lösen AssignmentDenied aus
try:
    authorize_role("unbekannte_rolle", mode="full")
except AssignmentDenied as fehler:
    print(f"Abgelehnt: {fehler}")
```

### Besetzungs-Nachweise

```python
from agents_heart import begin_assignment, finish_assignment

ereignisse = []

# Startnachweis aufzeichnen
besetzung = begin_assignment(
    role_id="task_worker",
    mode="full",
    agent_instance_id="instanz-42",
    backend_id="lokaler_executor",
    model_id="gemini-flash",
    slot_id="worker_slot_01",
    task_id="TASK-1001",
    event_recorder=ereignisse.append,
)

# ... Task-Durchführung ...

# Endnachweis aufzeichnen
finish_assignment(
    assignment=besetzung,
    status="completed",
    event_recorder=ereignisse.append,
    result="erfolgreich",
)

assert len(ereignisse) == 2
assert ereignisse[0]["assignment_id"] == ereignisse[1]["assignment_id"]
```

### Sichere Worker-Profilbereinigung

```python
from agents_heart import delete_worker_profile

profil = {"id": "worker-alpha"}

erfolg = delete_worker_profile(
    "worker-alpha",
    profil,
    assert_inactive=lambda p: None,
    terminal_records=lambda p: [{"id": "lauf-99", "phase": "terminal"}],
    archive=lambda pid, belege: print(f"{len(belege)} Läufe für {pid} archiviert"),
    remove=lambda: True,
)
assert erfolg is True
```

## Modulgrenzen

- **Netzwerk:** Keine Netzwerkzugriffe (`boundaries.network: "none"`).
- **Daten:** Benutzerlokal (`boundaries.data: "user-local"`).
- **Plattformen:** Windows, macOS, Linux.
- **Oberfläche:** Python-Bibliothek (`entrypoints.library: "agents_heart"`).

## Tests & Linting

Führe Linter sowie Unit- und Vertragstests mit `ruff` und `pytest` aus:

```bash
ruff check .
pytest -ra -v
```

## Governance & LLM-Einstiege

- [SKILL.md](SKILL.md) — Agenten-Skill-Spezifikation
- [llms.txt](llms.txt) — Kompakter LLM-Kontexteinstieg ([llm.txt](llm.txt))
- [CONTRIBUTING.md](CONTRIBUTING.md) — Entwicklungs- und Qualitätsregeln
- [SECURITY.md](SECURITY.md) — Sicherheitsgarantien und vertrauliche Meldung
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — Verhaltenskodex
- [CHANGELOG.md](CHANGELOG.md) — Versionshistorie

## Lizenz

MIT-Lizenz. Siehe [LICENSE](LICENSE).
