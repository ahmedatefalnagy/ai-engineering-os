"""Domain contracts and ports for SIFR."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Sequence

from sifr.domain.models import Project, ProjectConfig


class ConfigPort(ABC):
    """Port for loading and validating project and system configurations."""

    @abstractmethod
    def load_project_config(self, config_path: Path) -> ProjectConfig:
        """Safely loads and validates a project YAML configuration."""
        raise NotImplementedError

    @abstractmethod
    def save_project_config(self, config_path: Path, config: ProjectConfig) -> None:
        """Saves a project configuration to disk safely."""
        raise NotImplementedError


class RepositoryPort(ABC):
    """Port for persistence of projects and system state."""

    @abstractmethod
    def save_project(self, project: Project) -> None:
        """Persists or updates a project."""
        raise NotImplementedError

    @abstractmethod
    def get_project_by_id(self, project_id: str) -> Project | None:
        """Finds a project by its unique identifier."""
        raise NotImplementedError

    @abstractmethod
    def get_project_by_name(self, name: str) -> Project | None:
        """Finds a project by its unique name."""
        raise NotImplementedError

    @abstractmethod
    def list_projects(self) -> Sequence[Project]:
        """Lists all managed projects."""
        raise NotImplementedError
