# -*- coding: utf-8 -*-
import pytest
from agents_heart import (
    AssignmentDenied,
    ProfileDeletionRejected,
    authorize_role,
    begin_assignment,
    delete_worker_profile,
    finish_assignment,
)


def test_begin_and_finish_assignment():
    events = []
    assignment = begin_assignment(
        role_id="hintergrund_worker",
        mode="full",
        agent_instance_id="inst-1",
        backend_id="ollama",
        model_id="qwen3",
        slot_id="buddha_always_on",
        task_id=101,
        event_recorder=events.append,
    )
    finish_assignment(
        assignment=assignment,
        status="completed",
        event_recorder=events.append,
        result="ok",
    )
    assert len(events) == 2
    assert events[0]["event"] == "assignment.started"
    assert events[1]["event"] == "assignment.ended"
    assert events[0]["assignment_id"] == events[1]["assignment_id"]


def test_delete_worker_profile_enforces_inactivity_and_terminal_receipts():
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

    with pytest.raises(ProfileDeletionRejected) as exc:
        delete_worker_profile(
            "worker-1",
            profile,
            assert_inactive=lambda p: None,
            terminal_records=lambda p: [{"id": "run-2", "phase": "running"}],
            archive=lambda pid, recs: None,
            remove=lambda: True,
        )
    assert exc.value.code == "terminal_receipts_unconfirmed"
