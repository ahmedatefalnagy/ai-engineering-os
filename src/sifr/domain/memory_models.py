"""Domain models for Phase 4: Markdown+SQLite Memory, Technology Profiles, and Templates."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class MemoryCategory(StrEnum):
    DECISION = "decision"  # Architecture decisions (ADRs)
    REQUIREMENT = "requirement"  # Functional specs and requirements
    SUMMARY = "summary"  # Session or milestone summaries
    INCIDENT = "incident"  # Known bugs or postmortems


@dataclass(frozen=True)
class MemoryDocument:
    """Represents a human-readable Markdown document indexed into SQLite."""

    title: str
    category: MemoryCategory
    markdown_content: str
    project_id: str
    doc_id: str
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class TechnologyProfile:
    """Encapsulates toolchain, build, test, and quality commands for a tech stack."""

    profile_id: str
    name: str
    language: str
    test_command: str
    lint_command: str
    build_command: str | None = None
    default_files: dict[str, str] = field(default_factory=dict)
    rules: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ProjectTemplate:
    """Scaffolding template for generating ready-to-run projects."""

    template_id: str
    name: str
    technology_profile_id: str
    description: str
    files: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
