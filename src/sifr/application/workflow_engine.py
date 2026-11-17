"""Workflow Engine and Approval Use Cases."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime

from sifr.application.logging import AuditLogger
from sifr.domain.errors import SifrError
from sifr.domain.workflow_models import (
    ApprovalRequest,
    ApprovalStatus,
    Task,
    TaskStatus,
)
from sifr.ports.workflow_contracts import ApprovalRepositoryPort, TaskRepositoryPort


class TaskDependencyError(SifrError):
    def __init__(self, message: str) -> None:
        super().__init__(f"Task dependency unresolved: {message}", exit_code=10)


class ApprovalRequiredError(SifrError):
    def __init__(self, task_id: str) -> None:
        super().__init__(f"Task '{task_id}' is halted awaiting human approval", exit_code=11)


class WorkflowEngine:
    """Manages task lifecycle, DAG dependencies, and human approval gates."""

    def __init__(
        self,
        task_repo: TaskRepositoryPort,
        approval_repo: ApprovalRepositoryPort,
        audit_logger: AuditLogger | None = None,
    ) -> None:
        self.task_repo = task_repo
        self.approval_repo = approval_repo
        self.audit = audit_logger or AuditLogger()

    def create_task(
        self,
        title: str,
        description: str,
        project_id: str,
        assigned_agent: str | None = None,
        dependencies: list[str] | None = None,
        requires_approval: bool = False,
    ) -> Task:
        task = Task(
            title=title,
            description=description,
            project_id=project_id,
            assigned_agent=assigned_agent,
            dependencies=dependencies or [],
            requires_approval=requires_approval,
            status=TaskStatus.PENDING,
        )
        self.task_repo.save_task(task)
        self.audit.log_event(
            "task_created",
            {
                "task_id": task.task_id,
                "project_id": task.project_id,
                "title": task.title,
                "requires_approval": requires_approval,
            },
        )
        return task

    def start_task(self, task_id: str) -> Task:
        task = self.task_repo.get_task_by_id(task_id)
        if not task:
            raise SifrError(f"Task '{task_id}' not found", exit_code=12)

        # Check dependencies
        for dep_id in task.dependencies:
            dep_task = self.task_repo.get_task_by_id(dep_id)
            if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                raise TaskDependencyError(f"Dependency '{dep_id}' is not completed")

        # Check approval gate
        if task.requires_approval:
            approvals = self.approval_repo.get_pending_approvals_for_task(task_id)
            if not approvals:
                # Create approval request if none exists
                req = ApprovalRequest(
                    task_id=task_id,
                    action_description=f"Approve execution of task '{task.title}'",
                )
                self.approval_repo.save_approval_request(req)
                self.audit.log_event(
                    "approval_requested", {"task_id": task_id, "req_id": req.request_id}
                )

            # Update status to awaiting approval
            halted_task = Task(
                title=task.title,
                description=task.description,
                project_id=task.project_id,
                task_id=task.task_id,
                assigned_agent=task.assigned_agent,
                status=TaskStatus.AWAITING_APPROVAL,
                dependencies=task.dependencies,
                requires_approval=task.requires_approval,
                created_at=task.created_at,
                metadata=task.metadata,
            )
            self.task_repo.save_task(halted_task)
            raise ApprovalRequiredError(task_id)

        in_progress_task = Task(
            title=task.title,
            description=task.description,
            project_id=task.project_id,
            task_id=task.task_id,
            assigned_agent=task.assigned_agent,
            status=TaskStatus.IN_PROGRESS,
            dependencies=task.dependencies,
            requires_approval=task.requires_approval,
            created_at=task.created_at,
            metadata=task.metadata,
        )
        self.task_repo.save_task(in_progress_task)
        self.audit.log_event("task_started", {"task_id": task_id})
        return in_progress_task

    def complete_task(self, task_id: str) -> Task:
        task = self.task_repo.get_task_by_id(task_id)
        if not task:
            raise SifrError(f"Task '{task_id}' not found", exit_code=12)

        completed_task = Task(
            title=task.title,
            description=task.description,
            project_id=task.project_id,
            task_id=task.task_id,
            assigned_agent=task.assigned_agent,
            status=TaskStatus.COMPLETED,
            dependencies=task.dependencies,
            requires_approval=task.requires_approval,
            created_at=task.created_at,
            completed_at=datetime.now(UTC),
            metadata=task.metadata,
        )
        self.task_repo.save_task(completed_task)
        self.audit.log_event("task_completed", {"task_id": task_id})
        return completed_task

    def decide_approval(
        self,
        request_id: str,
        approved: bool,
        decided_by: str,
        reason: str | None = None,
    ) -> ApprovalRequest:
        req = self.approval_repo.get_approval_by_id(request_id)
        if not req:
            raise SifrError(f"Approval request '{request_id}' not found", exit_code=13)

        new_status = ApprovalStatus.APPROVED if approved else ApprovalStatus.REJECTED
        updated_req = ApprovalRequest(
            task_id=req.task_id,
            action_description=req.action_description,
            request_id=req.request_id,
            status=new_status,
            decided_by=decided_by,
            decision_reason=reason,
            created_at=req.created_at,
            decided_at=datetime.now(UTC),
        )
        self.approval_repo.save_approval_request(updated_req)

        # Update the associated task
        task = self.task_repo.get_task_by_id(req.task_id)
        if task:
            task_status = TaskStatus.PENDING if approved else TaskStatus.REJECTED
            updated_task = Task(
                title=task.title,
                description=task.description,
                project_id=task.project_id,
                task_id=task.task_id,
                assigned_agent=task.assigned_agent,
                status=task_status,
                dependencies=task.dependencies,
                requires_approval=False if approved else task.requires_approval,
                created_at=task.created_at,
                metadata=task.metadata,
            )
            self.task_repo.save_task(updated_task)

        self.audit.log_event(
            "approval_decided",
            {
                "request_id": request_id,
                "task_id": req.task_id,
                "approved": approved,
                "decided_by": decided_by,
            },
        )
        return updated_req

    def list_project_tasks(self, project_id: str) -> Sequence[Task]:
        return self.task_repo.list_tasks_for_project(project_id)
