# Security Policy / Sicherheitsrichtlinie

[English](#english) | [Deutsch](#deutsch)

---

## English

### Supported Versions
Security fixes target the latest `0.2.x` release line on `main`.

### Security Model & Boundaries
- **Network:** `none` — `agents-heart` performs zero network I/O and no external telemetry.
- **Data:** `user-local` — all assignment receipts and role validations run purely in-memory via caller-supplied callbacks.
- **Fail-Closed Guarantees:**
  - `authorize_role` rejects unknown roles, unknown modes (`safe`/`full` only), and incomplete permission sets via `AssignmentDenied`.
  - `delete_worker_profile` rejects invalid/mismatched identities, missing execution proofs, unavailable callbacks, or non-terminal archived records (`phase != "terminal"`) via `ProfileDeletionRejected` before archiving or deleting.

### Reporting a Vulnerability
Please **do not** disclose security vulnerabilities in public issues.
Report issues privately via:
- GitHub Private Vulnerability Reporting (Security Advisories) on `ellmos-ai/agents-heart`
- Email: `security@ellmos.ai` or `security@open-bricks.org`

Target initial response time: within **48 hours**.

---

## Deutsch

### Unterstützte Versionen
Sicherheitskorrekturen richten sich an die aktuelle `0.2.x`-Linie auf `main`.

### Sicherheitsmodell & Grenzen
- **Netzwerk:** `none` — `agents-heart` führt keinerlei Netzwerk-I/O oder externe Telemetrie aus.
- **Daten:** `user-local` — sämtliche Besetzungsnachweise und Rollenprüfungen laufen rein im Speicher über übergebene Callbacks.
- **Fail-Closed-Garantien:**
  - `authorize_role` lehnt unbekannte Rollen, unbekannte Modi (nur `safe`/`full`) und unvollständige Rechteverträge mit `AssignmentDenied` ab.
  - `delete_worker_profile` lehnt ungültige/abweichende Identitäten, fehlende Ausführungsnachweise, fehlende Port-Callbacks oder nicht-terminale Datensätze (`phase != "terminal"`) mit `ProfileDeletionRejected` ab, bevor archiviert oder gelöscht wird.

### Sicherheitslücken melden
Bitte Sicherheitslücken **nicht** in öffentlichen Issues melden, sondern vertraulich über:
- GitHub Private Vulnerability Reporting (Security Advisories) in `ellmos-ai/agents-heart`
- E-Mail: `security@ellmos.ai` oder `security@open-bricks.org`

Angestrebte Erstreaktionszeit: innerhalb von **48 Stunden**.
