"""SQLite implementation for Phase 2: Tasks and Approvals."""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path

from sifr.domain.workflow_models import (
    ApprovalRequest,
    ApprovalStatus,
    Task,
    TaskStatus,
)
from sifr.ports.workflow_contracts import ApprovalRepositoryPort, TaskRepositoryPort


class SQLiteWorkflowRepositoryAdapter(TaskRepositoryPort, ApprovalRepositoryPort):
    """Handles task and approval persistence inside SQLite."""

    def __init__(self, db_path: Path | str = ":memory:") -> None:
        self.db_path = str(db_path)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    assigned_agent TEXT,
                    status TEXT NOT NULL,
                    dependencies_json TEXT NOT NULL,
                    requires_approval INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    completed_at TEXT,
                    metadata_json TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS approvals (
                    request_id TEXT PRIMARY KEY,
                    task_id TEXT NOT NULL,
                    action_description TEXT NOT NULL,
                    status TEXT NOT NULL,
                    decided_by TEXT,
                    decision_reason TEXT,
                    created_at TEXT NOT NULL,
                    decided_at TEXT
                )
            """)
            conn.commit()

    def save_task(self, task: Task) -> None:
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO tasks (
                    task_id, project_id, title, description, assigned_agent,
                    status, dependencies_json, requires_approval, created_at,
                    completed_at, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(task_id) DO UPDATE SET
                    status=excluded.status,
                    assigned_agent=excluded.assigned_agent,
                    requires_approval=excluded.requires_approval,
                    completed_at=excluded.completed_at,
                    metadata_json=excluded.metadata_json
            """,
                (
                    task.task_id,
                    task.project_id,
                    task.title,
                    task.description,
                    task.assigned_agent,
                    task.status.value,
                    json.dumps(task.dependencies),
                    1 if task.requires_approval else 0,
                    task.created_at.isoformat(),
                    task.completed_at.isoformat() if task.completed_at else None,
                    json.dumps(task.metadata),
                ),
            )
            conn.commit()

    def get_task_by_id(self, task_id: str) -> Task | None:
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,)).fetchone()
            if not row:
                return None
            return self._row_to_task(row)

    def list_tasks_for_project(self, project_id: str) -> Sequence[Task]:
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM tasks WHERE project_id = ? ORDER BY created_at ASC", (project_id,)
            )
            return [self._row_to_task(row) for row in cursor.fetchall()]

    def save_approval_request(self, approval: ApprovalRequest) -> None:
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO approvals (
                    request_id, task_id, action_description, status,
                    decided_by, decision_reason, created_at, decided_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(request_id) DO UPDATE SET
                    status=excluded.status,
                    decided_by=excluded.decided_by,
                    decision_reason=excluded.decision_reason,
                    decided_at=excluded.decided_at
            """,
                (
                    approval.request_id,
                    approval.task_id,
                    approval.action_description,
                    approval.status.value,
                    approval.decided_by,
                    approval.decision_reason,
                    approval.created_at.isoformat(),
                    approval.decided_at.isoformat() if approval.decided_at else None,
                ),
            )
            conn.commit()

    def get_approval_by_id(self, request_id: str) -> ApprovalRequest | None:
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM approvals WHERE request_id = ?", (request_id,)
            ).fetchone()
            if not row:
                return None
            return self._row_to_approval(row)

    def get_pending_approvals_for_task(self, task_id: str) -> Sequence[ApprovalRequest]:
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM approvals WHERE task_id = ? AND status = ?",
                (task_id, ApprovalStatus.PENDING.value),
            )
            return [self._row_to_approval(row) for row in cursor.fetchall()]

    def _row_to_task(self, row: sqlite3.Row) -> Task:
        return Task(
            task_id=row["task_id"],
            project_id=row["project_id"],
            title=row["title"],
            description=row["description"],
            assigned_agent=row["assigned_agent"],
            status=TaskStatus(row["status"]),
            dependencies=json.loads(row["dependencies_json"]),
            requires_approval=bool(row["requires_approval"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            completed_at=datetime.fromisoformat(row["completed_at"])
            if row["completed_at"]
            else None,
            metadata=json.loads(row["metadata_json"]),
        )

    def _row_to_approval(self, row: sqlite3.Row) -> ApprovalRequest:
        return ApprovalRequest(
            request_id=row["request_id"],
            task_id=row["task_id"],
            action_description=row["action_description"],
            status=ApprovalStatus(row["status"]),
            decided_by=row["decided_by"],
            decision_reason=row["decision_reason"],
            created_at=datetime.fromisoformat(row["created_at"]),
            decided_at=datetime.fromisoformat(row["decided_at"]) if row["decided_at"] else None,
        )
