"""Domain models for Phase 2: Agents, Tasks, Workflows, and Approvals."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class TaskStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    AWAITING_APPROVAL = "awaiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    REJECTED = "rejected"


class ApprovalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass(frozen=True)
class AgentRole:
    """Represents a persona or execution capability within SIFR."""

    name: str
    description: str
    allowed_tools: list[str] = field(default_factory=list)
    budget_limit_usd: float = 10.0
    permissions: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Task:
    """A granular unit of work within a project workflow."""

    title: str
    description: str
    project_id: str
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    assigned_agent: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    dependencies: list[str] = field(default_factory=list)
    requires_approval: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ApprovalRequest:
    """Represents a human-in-the-loop approval gate."""

    task_id: str
    action_description: str
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: ApprovalStatus = ApprovalStatus.PENDING
    decided_by: str | None = None
    decision_reason: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    decided_at: datetime | None = None
