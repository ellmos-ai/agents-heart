<p align="center">
  <img src="assets/banner.svg" alt="agents-heart banner" width="100%">
</p>

# agents-heart

[![Version](https://img.shields.io/badge/version-0.2.0-blue)](pyproject.toml)
[![Python](https://img.shields.io/badge/python-3.11%20|%203.12%20|%203.13-blue)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/pytest-23%20passed-brightgreen)](tests/)
[![Verified](https://img.shields.io/badge/verified-2026--11--19-informational)](CHANGELOG.md)

**Language / Sprache:** **English** | [Deutsch](README_de.md)

Provider-neutral control library (`modul:agents-heart`, v0.2.0) for agent role contract enforcement, assignment correlation, and worker profile lifecycle management.

## Overview

`agents-heart` acts as a fail-closed control layer between orchestrators and execution runtimes. It does not decide model selection or backend providers directly. Instead, it:
1. **Enforces role contracts (`authorize_role`)**: Verifies that an execution path holds required permissions (`task.claim`, `task.execute`) before work begins.
2. **Correlates assignments (`begin_assignment`, `finish_assignment`)**: Issues unique, immutable `Assignment` identifiers and emits matching start and end receipts (`assignment.started`, `assignment.ended`).
3. **Guards worker profile retirement (`delete_worker_profile`)**: Ensures worker inactivity, verifies all runs have reached terminal status (`phase == "terminal"`), archives records, and triggers safe removal.

## Installation

```bash
pip install -e .
```

With development tools (`pytest`, `ruff`):

```bash
pip install -e ".[dev]"
```

### Install & Integrate with Your LLM

Read [llms.txt](llms.txt) and [SKILL.md](SKILL.md) for concise API contracts and fail-closed usage patterns:

> *Prompt:* "Read `llms.txt` and `SKILL.md` in `agents-heart`, install the package with `pip install -e .`, and integrate `authorize_role`, `begin_assignment`, `finish_assignment`, and `delete_worker_profile` without bypassing fail-closed checks."

## Usage

### Role Authorization

```python
from agents_heart import authorize_role, AssignmentDenied

# Validate contract permissions fail-closed
contract = authorize_role("task_worker", mode="full")
assert "task.claim" in contract.rights
assert "task.execute" in contract.rights

# Unauthorized roles raise AssignmentDenied
try:
    authorize_role("unknown_role", mode="full")
except AssignmentDenied as err:
    print(f"Denied: {err}")
```

### Assignment Correlation

```python
from agents_heart import begin_assignment, finish_assignment

events = []

# Record start receipt
assignment = begin_assignment(
    role_id="task_worker",
    mode="full",
    agent_instance_id="instance-42",
    backend_id="local_runner",
    model_id="gemini-flash",
    slot_id="worker_slot_01",
    task_id="TASK-1001",
    event_recorder=events.append,
)

# Perform actual execution...

# Record termination receipt
finish_assignment(
    assignment=assignment,
    status="completed",
    event_recorder=events.append,
    result="success",
)

assert len(events) == 2
assert events[0]["assignment_id"] == events[1]["assignment_id"]
```

### Worker Profile Deletion

```python
from agents_heart import delete_worker_profile

profile = {"id": "worker-alpha"}

success = delete_worker_profile(
    "worker-alpha",
    profile,
    assert_inactive=lambda p: None,
    terminal_records=lambda p: [{"id": "run-99", "phase": "terminal"}],
    archive=lambda pid, recs: print(f"Archived {len(recs)} runs for {pid}"),
    remove=lambda: True,
)
assert success is True
```

## Module Boundaries

- **Network:** None (`boundaries.network: "none"`)
- **Data:** User-local (`boundaries.data: "user-local"`)
- **Platforms:** Windows, macOS, Linux
- **Surfaces:** Python library (`entrypoints.library: "agents_heart"`)

## Testing & Linting

Run linting and unit/contract tests via `ruff` and `pytest`:

```bash
ruff check .
pytest -ra -v
```

## Governance & LLM Entrypoints

- [SKILL.md](SKILL.md) — Agent skill reference
- [llms.txt](llms.txt) — Concise LLM context entrypoint ([llm.txt](llm.txt))
- [CONTRIBUTING.md](CONTRIBUTING.md) — Development and quality gates
- [SECURITY.md](SECURITY.md) — Security guarantees and private reporting
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — Community standards
- [CHANGELOG.md](CHANGELOG.md) — Version history

## Documentation in German

A German companion guide is available at [README_de.md](README_de.md).

## License

MIT License. See [LICENSE](LICENSE) for details.
