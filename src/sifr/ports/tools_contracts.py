"""Domain models and Ports for Phase 5: Coding Tool Adapters, Spec Frameworks, and Git."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class ToolExecutionCapability(StrEnum):
    DIRECT_EXECUTION = "direct_execution"  # Tool CLI can be spawned programmatically
    PROMPT_INSTRUCTION = (
        "prompt_instruction"  # Generates instruction files (.cursorrules, AGENTS.md)
    )


@dataclass(frozen=True)
class ToolExecutionResult:
    """Outcome of running an external coding tool or instruction generator."""

    tool_id: str
    success: bool
    output: str
    exit_code: int = 0
    artifacts_generated: list[Path] = field(default_factory=list)


class CodingToolPort(ABC):
    """Port interface for external coding assistants (Claude Code, Cursor, Copilot, Antigravity, etc.)."""

    @property
    @abstractmethod
    def tool_id(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def capability(self) -> ToolExecutionCapability:
        raise NotImplementedError

    @abstractmethod
    def execute_task(self, project_root: Path, prompt_instruction: str) -> ToolExecutionResult:
        raise NotImplementedError


class SpecFrameworkPort(ABC):
    """Port for Spec frameworks (Spec Kit, OpenSpec, Superpowers)."""

    @property
    @abstractmethod
    def framework_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate_spec(self, project_root: Path, user_story: str) -> Path:
        raise NotImplementedError
