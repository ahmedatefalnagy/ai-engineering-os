"""Unit tests for Phase 2: Workflow Engine, Task Dependencies, and Approvals."""

from pathlib import Path

import pytest

from sifr.adapters.persistence.workflow_sqlite_adapter import SQLiteWorkflowRepositoryAdapter
from sifr.application.workflow_engine import (
    ApprovalRequiredError,
    TaskDependencyError,
    WorkflowEngine,
)
from sifr.domain.workflow_models import ApprovalStatus, TaskStatus


def test_task_lifecycle_and_dependencies(tmp_path: Path) -> None:
    db_file = tmp_path / "workflow_test.db"
    adapter = SQLiteWorkflowRepositoryAdapter(db_file)
    engine = WorkflowEngine(task_repo=adapter, approval_repo=adapter)

    # 1. Create Task A
    task_a = engine.create_task(
        title="Setup DB Schema",
        description="Initialize PostgreSQL tables",
        project_id="proj_1",
    )
    assert task_a.status == TaskStatus.PENDING

    # 2. Create Task B depending on Task A
    task_b = engine.create_task(
        title="Seed DB Data",
        description="Insert sample records",
        project_id="proj_1",
        dependencies=[task_a.task_id],
    )

    # 3. Attempt to start Task B before Task A finishes -> Must Fail with TaskDependencyError
    with pytest.raises(TaskDependencyError):
        engine.start_task(task_b.task_id)

    # 4. Start & Complete Task A
    engine.start_task(task_a.task_id)
    engine.complete_task(task_a.task_id)

    # 5. Now starting Task B must succeed
    started_b = engine.start_task(task_b.task_id)
    assert started_b.status == TaskStatus.IN_PROGRESS


def test_human_approval_gate(tmp_path: Path) -> None:
    db_file = tmp_path / "approval_test.db"
    adapter = SQLiteWorkflowRepositoryAdapter(db_file)
    engine = WorkflowEngine(task_repo=adapter, approval_repo=adapter)

    # Task requiring approval (e.g., prod deployment or destructive migration)
    task_crit = engine.create_task(
        title="Drop Old Partition",
        description="Destructive table cleanup",
        project_id="proj_1",
        requires_approval=True,
    )

    # Starting must halt and raise ApprovalRequiredError
    with pytest.raises(ApprovalRequiredError):
        engine.start_task(
            task_crit.task_crit_id if hasattr(task_crit, "task_crit_id") else task_crit.task_id
        )

    # Verify pending approvals
    pending = adapter.get_pending_approvals_for_task(task_crit.task_id)
    assert len(pending) == 1
    req = pending[0]
    assert req.status == ApprovalStatus.PENDING

    # Approve request
    engine.decide_approval(
        request_id=req.request_id,
        approved=True,
        decided_by="admin_ahmed",
        reason="Verified backup snapshot",
    )

    # Task status back to PENDING and approval flag resolved
    updated_task = adapter.get_task_by_id(task_crit.task_id)
    assert updated_task is not None
    assert updated_task.requires_approval is False

    # Now task can start
    started = engine.start_task(task_crit.task_id)
    assert started.status == TaskStatus.IN_PROGRESS
