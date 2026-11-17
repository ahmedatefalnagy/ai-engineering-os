"""Ports for Phase 2: Workflow, Tasks, Agents, and Approval management."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from sifr.domain.workflow_models import AgentRole, ApprovalRequest, Task


class TaskRepositoryPort(ABC):
    """Port for persisting tasks and execution status."""

    @abstractmethod
    def save_task(self, task: Task) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_task_by_id(self, task_id: str) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    def list_tasks_for_project(self, project_id: str) -> Sequence[Task]:
        raise NotImplementedError


class ApprovalRepositoryPort(ABC):
    """Port for managing human approval gates."""

    @abstractmethod
    def save_approval_request(self, approval: ApprovalRequest) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_approval_by_id(self, request_id: str) -> ApprovalRequest | None:
        raise NotImplementedError

    @abstractmethod
    def get_pending_approvals_for_task(self, task_id: str) -> Sequence[ApprovalRequest]:
        raise NotImplementedError


class AgentRegistryPort(ABC):
    """Port for discovering and configuring agent personas."""

    @abstractmethod
    def register_role(self, role: AgentRole) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_role(self, name: str) -> AgentRole | None:
        raise NotImplementedError

    @abstractmethod
    def list_roles(self) -> Sequence[AgentRole]:
        raise NotImplementedError
