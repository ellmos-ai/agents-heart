---
name: agents-heart
version: 0.2.0
description: "Provider-neutral agent role contract enforcement, assignment correlation receipts, and fail-closed worker profile deletion for Python orchestrators."
---

# agents-heart Skill

Use `agents-heart` when building or auditing orchestrator control layers in Python (`>=3.11`) that require:
1. **Role Contract Authorization** (`authorize_role`)
2. **Assignment Lifecycle Correlation** (`begin_assignment`, `finish_assignment`)
3. **Fail-Closed Worker Profile Retirement** (`delete_worker_profile` / `archive_then_remove_profile`)

## Installation

```bash
pip install -e .
```

## Canonical API

### 1. Authorize Role (`authorize_role`)
Validates `role_id` against `ROLE_CONTRACTS` (`hintergrund_worker`, `task_worker`, `boss_routing`, `expert_role`) and `mode` (`"safe"` or `"full"`), ensuring `task.claim` and `task.execute` rights. Raises `AssignmentDenied` fail-closed on any mismatch.

```python
from agents_heart import AssignmentDenied, authorize_role

contract = authorize_role("task_worker", mode="full")
```

### 2. Correlate Assignments (`begin_assignment` / `finish_assignment`)
Creates an immutable `Assignment` dataclass with UUIDs and UTC timestamps, recording `assignment.started` and `assignment.ended` receipts (`status` in `{"completed", "released", "error", "interrupted"}`).

```python
from agents_heart import begin_assignment, finish_assignment

events = []
assignment = begin_assignment(
    role_id="task_worker",
    mode="full",
    agent_instance_id="worker-01",
    backend_id="local",
    model_id="default",
    slot_id="slot-01",
    task_id="TASK-1",
    event_recorder=events.append,
)
finish_assignment(assignment=assignment, status="completed", event_recorder=events.append)
```

### 3. Safe Worker Profile Deletion (`delete_worker_profile`)
Enforces four guards before removal:
1. Exact `profile_id` and `profile["id"]` match (`ProfileDeletionRejected("profile_identity_invalid" | "profile_identity_mismatch")`).
2. `assert_inactive(profile)` callable proof (`"execution_proof_required"`).
3. All `terminal_records(profile)` have `record.get("phase") == "terminal"` (`"terminal_receipts_unconfirmed"`).
4. `archive(profile_id, records)` completes before `remove()` is called (`"deletion_port_unavailable"` if callables missing).

## Module Boundaries
- **Network:** `none` (zero network I/O)
- **Data:** `user-local`
- **Dependencies:** Zero runtime dependencies (Python stdlib only, PEP 561 typed via `py.typed`)
