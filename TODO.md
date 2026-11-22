# TODO — agents-heart

Provider-neutrales Control-Modul (`modul:agents-heart`, v0.2.0) für Worker-Rollenverträge, Besetzungs-Autorisierung und Profil-Lebenszyklus.

## STATUS

| Category | Status | Notes |
|----------|--------|-------|
| .gitignore | :green_circle: | Alle Mindesteinträge für Release-Hygiene, Multi-Host- & Lock-Schutz vorhanden |
| README.md | :green_circle: | Vollständige englische Dokumentation mit zweisprachiger README_de.md |
| LICENSE | :green_circle: | MIT-Lizenzdatei vorhanden |
| Database Files | :green_circle: | 0 .db-Dateien im Repository |
| Environment Files | :green_circle: | 0 .env-Dateien im Repository |
| Secrets | :green_circle: | 0 Tokens, Passwörter oder private Schlüssel |
| Personal Paths | :green_circle: | 0 hartcodierte persönliche Dateipfade |
| Private Data (PII) | :green_circle: | 0 PII-Muster in getrackten Dateien |
| BACH Internals | :green_circle: | 0 BACH-interne Dokumente oder Pfade |
| TODO.md | :green_circle: | Standardisierte Statustabelle und Roadmap codifiziert |
| **Overall** | **CLEAN** | 10/10 Final Gate Check PASS, 100% Metadaten- und Vertragspariät |

**Audit-Datum:** 2026-11-19
**Gate Check Exit Code:** `0`

---

## Erledigte Aufgaben

- [x] **Rollen-Vertragsprüfung (`authorize_role`):** Fail-closed Prüfung der Rechteverträge (`hintergrund_worker`, `task_worker`, `boss_routing`, `expert_role`) mit `task.claim` und `task.execute`.
- [x] **Besetzungs-Startnachweis (`begin_assignment`):** Generierung unveränderlicher `Assignment`-Instanzen mit korrelierter UUID, Zeitstempel (UTC) und `assignment.started`-Ereignis.
- [x] **Besetzungs-Endnachweis (`finish_assignment`):** Aufzeichnung korrelierter `assignment.ended`-Ereignisse mit Terminal-Status (`completed`, `released`, `error`, `interrupted`).
- [x] **Sicheres Profil-Löschen (`delete_worker_profile`):** Vierstufiger Schutz gegen unvollständige Profil-Entfernung (Identitätsprüfung, Inaktivitäts-Assertion, Bestätigung von Terminal-Belegen `phase == 'terminal'`, Archivierungs-Handoff).
- [x] **PEP 561 Typisierungsunterstützung:** Typisierungsmarker `py.typed` hinterlegt und in `package-data` verankert.
- [x] **Testsuite-Härtung:** Umfassende Unit- und Vertragstests für alle Validierungs- und Fehlerpfade (`pytest` mit nativer `pythonpath`-Auflösung).
- [x] **Release-Gate-Standardisierung:** Bereitstellung von `LICENSE`, `.gitignore`, `TODO.md`, `README.md` und `README_de.md` für 10/10 Final Gate Check.
- [x] **Pfad-A-Hygiene, CI & Governance:** Cross-OS CI-Matrix, Dependabot, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CONTRIBUTING.md`, LLM-Einstiegspunkte (`SKILL.md`, `llms.txt`, `llm.txt`) und `ruff`-Bereinigung.

---

## Roadmap & Offene Punkte

- [ ] **Erweiterte Rollen-Definitionen:** Deklaratives Laden benutzerdefinierter Rollenverträge aus externen JSON/YAML-Konfigurationen bei Bedarf.
- [ ] **Ereignis-Audit-Filter:** Optionale Schema-Validierung für übergebene `event_recorder`-Payloads.
- [ ] **Leistungsmetriken im Endbeleg:** Aufzeichnung von Token-Verbrauch oder Laufzeitdauer in optionalen Belegfeldern.
