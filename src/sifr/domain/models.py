"""Core domain models for SIFR — AI Engineering OS.

These models represent pure business concepts, free of framework or I/O concerns.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any
import uuid


class IntegrationType(str, Enum):
    """The four strictly separated integration categories (ADR-009)."""
    NATIVE_PROVIDER = "native_provider"
    MODEL_GATEWAY = "model_gateway"
    CODING_TOOL = "coding_tool"
    SPEC_FRAMEWORK = "spec_framework"


class ProjectStatus(str, Enum):
    """Lifecycle status of a project under SIFR management."""
    INITIALIZED = "initialized"
    ACTIVE = "active"
    ARCHIVED = "archived"


@dataclass(frozen=True)
class Project:
    """Represents a software project governed by SIFR."""
    name: str
    root_path: Path
    technology_profile_id: str
    project_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: ProjectStatus = ProjectStatus.INITIALIZED
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)

    def is_path_within_project(self, target_path: Path) -> bool:
        """Security guard: verifies if a given path resides inside the project root."""
        try:
            target_path.resolve().relative_to(self.root_path.resolve())
            return True
        except ValueError:
            return False


@dataclass(frozen=True)
class ProjectConfig:
    """Configuration schema for a SIFR-managed project."""
    name: str
    version: str = "0.1.0"
    technology_profile: str = "generic"
    description: str = ""
    settings: dict[str, Any] = field(default_factory=dict)
