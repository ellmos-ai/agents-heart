# agents-heart

Provider-neutrales Control-Modul (`modul:agents-heart`, v0.2.0) für:

1. **Rollen-Autorisierung (`authorize_role`)**: Fail-closed Prüfung von `RoleContract`-Rechten (`task.claim`, `task.execute`).
2. **Besetzungs-Korrelation (`begin_assignment`, `finish_assignment`)**: Korrelierte Start-/End-Ereignisse (`assignment.started`, `assignment.ended`) mit unveränderlicher `Assignment`-Identität.
3. **Sicheres Entfernen inaktiver Worker-Profile (`delete_worker_profile`)**: Fail-closed Prüfung der Inaktivität, Verifikation abgeschlossener Läufe (`phase == "terminal"`), Archivierung und anschließende Entfernung.
