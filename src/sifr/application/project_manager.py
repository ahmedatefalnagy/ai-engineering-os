"""Project Manager Use Cases with strict error domain semantics and audit logging."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from sifr.application.logging import AuditLogger
from sifr.domain.errors import (
    ProjectAlreadyExistsError,
    ProjectNotFoundError,
    SecurityViolationError,
)
from sifr.domain.models import Project, ProjectConfig, ProjectStatus
from sifr.ports.contracts import ConfigPort, RepositoryPort


class ProjectManager:
    """Orchestrates project lifecycle operations with boundary checks and audit logging."""

    def __init__(
        self,
        config_port: ConfigPort,
        repository_port: RepositoryPort,
        audit_logger: AuditLogger | None = None,
    ) -> None:
        self.config_port = config_port
        self.repository_port = repository_port
        self.audit = audit_logger or AuditLogger()

    def initialize_project(
        self,
        name: str,
        target_dir: Path,
        technology_profile: str = "generic",
        description: str = "",
    ) -> Project:
        """Initializes a new SIFR project in the specified target directory."""
        target_dir = target_dir.resolve()
        target_dir.mkdir(parents=True, exist_ok=True)

        existing = self.repository_port.get_project_by_name(name)
        if existing:
            raise ProjectAlreadyExistsError(name)

        config = ProjectConfig(
            name=name,
            technology_profile=technology_profile,
            description=description,
        )
        config_path = target_dir / "sifr.yaml"
        self.config_port.save_project_config(config_path, config)

        project = Project(
            name=name,
            root_path=target_dir,
            technology_profile_id=technology_profile,
            status=ProjectStatus.INITIALIZED,
            metadata={"config_file": "sifr.yaml"},
        )
        self.repository_port.save_project(project)

        self.audit.log_event(
            "project_initialized",
            {
                "project_id": project.project_id,
                "name": project.name,
                "root_path": str(project.root_path),
                "profile": project.technology_profile_id,
            },
        )
        return project

    def get_project(self, name_or_id: str) -> Project:
        """Finds a project by name or ID, raising ProjectNotFoundError if missing."""
        by_name = self.repository_port.get_project_by_name(name_or_id)
        if by_name:
            return by_name
        by_id = self.repository_port.get_project_by_id(name_or_id)
        if by_id:
            return by_id
        raise ProjectNotFoundError(name_or_id)

    def verify_file_access(self, project: Project, target_path: Path) -> Path:
        """Enforces that access to a target path stays strictly within the project boundary."""
        target_resolved = target_path.resolve()
        if not project.is_path_within_project(target_resolved):
            raise SecurityViolationError(
                f"Path '{target_path}' is outside project boundary '{project.root_path}'"
            )
        return target_resolved

    def list_all_projects(self) -> Sequence[Project]:
        """Lists all registered projects."""
        return self.repository_port.list_projects()
