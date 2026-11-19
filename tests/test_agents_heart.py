from dataclasses import FrozenInstanceError

import pytest

from agents_heart import (
    AssignmentDenied,
    ProfileDeletionRejected,
    archive_then_remove_profile,
    authorize_role,
    begin_assignment,
    delete_worker_profile,
    finish_assignment,
)


def test_authorize_role_success():
    for role_id in ["hintergrund_worker", "task_worker", "boss_routing", "expert_role"]:
        for mode in ["safe", "full"]:
            contract = authorize_role(role_id, mode)
            assert contract.role_id == role_id
            assert "task.claim" in contract.rights
            assert "task.execute" in contract.rights


def test_authorize_role_unknown_role():
    with pytest.raises(AssignmentDenied, match="unbekannte Rolle"):
        authorize_role("non_existent_role", mode="full")

    with pytest.raises(AssignmentDenied, match="unbekannte Rolle"):
        authorize_role("", mode="full")


def test_authorize_role_invalid_mode():
    with pytest.raises(AssignmentDenied, match="unbekannter Ausführungsmodus"):
        authorize_role("task_worker", mode="unrestricted")


def test_begin_and_finish_assignment_flow():
    events = []
    assignment = begin_assignment(
        role_id="hintergrund_worker",
        mode="full",
        agent_instance_id="inst-1",
        backend_id="ollama",
        model_id="qwen3",
        slot_id="buddha_always_on",
        task_id=101,
        session_id="session-xyz",
        initiated_by="coordinator-9",
        event_recorder=events.append,
    )
    assert assignment.session_id == "session-xyz"
    assert assignment.initiated_by == "coordinator-9"

    finish_assignment(
        assignment=assignment,
        status="completed",
        event_recorder=events.append,
        result="ok",
        reason="all steps verified",
    )
    assert len(events) == 2
    assert events[0]["event"] == "assignment.started"
    assert events[0]["status"] == "started"
    assert events[1]["event"] == "assignment.ended"
    assert events[1]["status"] == "completed"
    assert events[1]["result"] == "ok"
    assert events[1]["reason"] == "all steps verified"
    assert "ended_at" in events[1]
    assert events[0]["assignment_id"] == events[1]["assignment_id"]


def test_begin_assignment_validates_required_fields():
    events = []
    with pytest.raises(ValueError, match="Besetzungsfeld agent_instance_id fehlt"):
        begin_assignment(
            role_id="task_worker",
            mode="safe",
            agent_instance_id="",
            backend_id="ollama",
            model_id="qwen3",
            slot_id="slot-1",
            task_id=10,
            event_recorder=events.append,
        )

    with pytest.raises(ValueError, match="Besetzungsfeld backend_id fehlt"):
        begin_assignment(
            role_id="task_worker",
            mode="safe",
            agent_instance_id="inst-1",
            backend_id="",
            model_id="qwen3",
            slot_id="slot-1",
            task_id=10,
            event_recorder=events.append,
        )

    with pytest.raises(ValueError, match="Besetzungsfeld model_id fehlt"):
        begin_assignment(
            role_id="task_worker",
            mode="safe",
            agent_instance_id="inst-1",
            backend_id="ollama",
            model_id="   ",
            slot_id="slot-1",
            task_id=10,
            event_recorder=events.append,
        )

    with pytest.raises(ValueError, match="Besetzungsfeld slot_id fehlt"):
        begin_assignment(
            role_id="task_worker",
            mode="safe",
            agent_instance_id="inst-1",
            backend_id="ollama",
            model_id="qwen3",
            slot_id="",
            task_id=10,
            event_recorder=events.append,
        )


def test_finish_assignment_validates_status():
    events = []
    assignment = begin_assignment(
        role_id="task_worker",
        mode="safe",
        agent_instance_id="inst-1",
        backend_id="ollama",
        model_id="qwen3",
        slot_id="slot-1",
        task_id=10,
        event_recorder=events.append,
    )

    with pytest.raises(ValueError, match="ungültiger Status"):
        finish_assignment(
            assignment=assignment,
            status="invalid_status",
            event_recorder=events.append,
        )

    for valid_status in ["completed", "released", "error", "interrupted"]:
        finish_assignment(
            assignment=assignment,
            status=valid_status,
            event_recorder=events.append,
        )
        assert events[-1]["status"] == valid_status


def test_delete_worker_profile_success():
    archived = []
    removed = []
    profile = {"id": "worker-1"}
    ok = delete_worker_profile(
        "worker-1",
        profile,
        assert_inactive=lambda p: None,
        terminal_records=lambda p: [{"id": "run-1", "phase": "terminal"}],
        archive=lambda pid, recs: archived.append((pid, recs)),
        remove=lambda: (removed.append(True) or True),
    )
    assert ok is True
    assert len(archived) == 1
    assert removed == [True]

    # Verify alias behaves identically
    ok_alias = archive_then_remove_profile(
        "worker-1",
        profile,
        assert_inactive=lambda p: None,
        terminal_records=lambda p: [{"id": "run-2", "phase": "terminal"}],
        archive=lambda pid, recs: archived.append((pid, recs)),
        remove=lambda: True,
    )
    assert ok_alias is True


def test_delete_worker_profile_rejection_cases():
    profile = {"id": "worker-1"}

    # Invalid profile_id
    with pytest.raises(ProfileDeletionRejected) as exc:
        delete_worker_profile(
            "",
            profile,
            assert_inactive=lambda p: None,
            terminal_records=lambda p: [],
            archive=lambda pid, r: None,
            remove=lambda: True,
        )
    assert exc.value.code == "profile_identity_invalid"

    # Profile identity mismatch
    with pytest.raises(ProfileDeletionRejected) as exc:
        delete_worker_profile(
            "worker-2",
            profile,
            assert_inactive=lambda p: None,
            terminal_records=lambda p: [],
            archive=lambda pid, r: None,
            remove=lambda: True,
        )
    assert exc.value.code == "profile_identity_mismatch"

    # Execution proof not callable
    with pytest.raises(ProfileDeletionRejected) as exc:
        delete_worker_profile(
            "worker-1",
            profile,
            assert_inactive="not_callable",  # type: ignore[arg-type]
            terminal_records=lambda p: [],
            archive=lambda pid, r: None,
            remove=lambda: True,
        )
    assert exc.value.code == "execution_proof_required"

    # Missing ports
    with pytest.raises(ProfileDeletionRejected) as exc:
        delete_worker_profile(
            "worker-1",
            profile,
            assert_inactive=lambda p: None,
            terminal_records="not_callable",  # type: ignore[arg-type]
            archive=lambda pid, r: None,
            remove=lambda: True,
        )
    assert exc.value.code == "deletion_port_unavailable"

    # Non-terminal records
    with pytest.raises(ProfileDeletionRejected) as exc:
        delete_worker_profile(
            "worker-1",
            profile,
            assert_inactive=lambda p: None,
            terminal_records=lambda p: [{"id": "run-3", "phase": "active"}],
            archive=lambda pid, r: None,
            remove=lambda: True,
        )
    assert exc.value.code == "terminal_receipts_unconfirmed"


def test_role_contract_and_assignment_are_frozen():
    contract = authorize_role("task_worker", mode="safe")
    with pytest.raises(FrozenInstanceError):
        contract.role_id = "other"  # type: ignore[misc]

    events: list[dict[str, object]] = []
    assignment = begin_assignment(
        role_id="task_worker",
        mode="safe",
        agent_instance_id="inst-immutable",
        backend_id="local",
        model_id="default",
        slot_id="slot-01",
        task_id="T-1",
        event_recorder=events.append,
    )
    with pytest.raises(FrozenInstanceError):
        assignment.status = "mutated"  # type: ignore[attr-defined]


def test_delete_worker_profile_inactivity_failure_prevents_archive_and_remove():
    archived: list[str] = []
    removed: list[bool] = []
    profile = {"id": "worker-active"}

    def fail_inactive(_profile):
        raise ProfileDeletionRejected("worker_still_active")

    with pytest.raises(ProfileDeletionRejected) as exc:
        delete_worker_profile(
            "worker-active",
            profile,
            assert_inactive=fail_inactive,
            terminal_records=lambda p: [{"id": "run-1", "phase": "terminal"}],
            archive=lambda pid, recs: archived.append(pid),
            remove=lambda: (removed.append(True) or True),
        )
    assert exc.value.code == "worker_still_active"
    assert archived == []
    assert removed == []
