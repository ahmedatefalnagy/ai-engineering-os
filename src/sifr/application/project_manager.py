"""Project Manager Use Cases."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from sifr.domain.models import Project, ProjectConfig, ProjectStatus
from sifr.ports.contracts import ConfigPort, RepositoryPort


class ProjectManager:
    """Orchestrates project lifecycle operations."""

    def __init__(self, config_port: ConfigPort, repository_port: RepositoryPort) -> None:
        self.config_port = config_port
        self.repository_port = repository_port

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
            raise ValueError(f"A project with name '{name}' is already registered.")

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
        return project

    def get_project(self, name_or_id: str) -> Project | None:
        """Finds a project by name or ID."""
        by_name = self.repository_port.get_project_by_name(name_or_id)
        if by_name:
            return by_name
        return self.repository_port.get_project_by_id(name_or_id)

    def list_all_projects(self) -> Sequence[Project]:
        """Lists all registered projects."""
        return self.repository_port.list_projects()
