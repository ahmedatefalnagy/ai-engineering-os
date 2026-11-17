"""Adapters for Phase 5: Coding tools (Cursor, Claude Code, Antigravity) and Spec Kit."""

from __future__ import annotations

from pathlib import Path

from sifr.ports.tools_contracts import (
    CodingToolPort,
    SpecFrameworkPort,
    ToolExecutionCapability,
    ToolExecutionResult,
)


class CursorToolAdapter(CodingToolPort):
    """Generates and manages .cursorrules instruction files."""

    @property
    def tool_id(self) -> str:
        return "cursor"

    @property
    def capability(self) -> ToolExecutionCapability:
        return ToolExecutionCapability.PROMPT_INSTRUCTION

    def execute_task(self, project_root: Path, prompt_instruction: str) -> ToolExecutionResult:
        rules_file = project_root / ".cursorrules"
        with open(rules_file, "w", encoding="utf-8") as f:
            f.write(f"# SIFR Generated Cursor Rules\n\n{prompt_instruction}\n")

        return ToolExecutionResult(
            tool_id=self.tool_id,
            success=True,
            output=f"Wrote Cursor instructions to {rules_file}",
            artifacts_generated=[rules_file],
        )


class AntigravityToolAdapter(CodingToolPort):
    """Optional adapter for Google Antigravity (subject to AGY-G1 boundary verification)."""

    @property
    def tool_id(self) -> str:
        return "antigravity"

    @property
    def capability(self) -> ToolExecutionCapability:
        return ToolExecutionCapability.PROMPT_INSTRUCTION

    def execute_task(self, project_root: Path, prompt_instruction: str) -> ToolExecutionResult:
        agent_spec = project_root / ".antigravity" / "instructions.md"
        agent_spec.parent.mkdir(parents=True, exist_ok=True)
        with open(agent_spec, "w", encoding="utf-8") as f:
            f.write(f"# SIFR Antigravity Context\n\n{prompt_instruction}\n")

        return ToolExecutionResult(
            tool_id=self.tool_id,
            success=True,
            output=f"Generated Antigravity instructions at {agent_spec}",
            artifacts_generated=[agent_spec],
        )


class SpecKitAdapter(SpecFrameworkPort):
    """Spec Kit adapter generating structured requirements and Gherkin features."""

    @property
    def framework_id(self) -> str:
        return "spec_kit"

    def generate_spec(self, project_root: Path, user_story: str) -> Path:
        specs_dir = project_root / "specs"
        specs_dir.mkdir(parents=True, exist_ok=True)
        spec_path = specs_dir / "functional_spec.md"
        with open(spec_path, "w", encoding="utf-8") as f:
            f.write(
                f"# Functional Specification (Spec Kit)\n\n## User Story\n{user_story}\n\n## Acceptance Criteria (Gherkin)\n- Given initialized project\n- When task is executed\n- Then quality gates verify output\n"
            )
        return spec_path
