"""InMemory Persistence Adapter for fast isolated testing."""

from __future__ import annotations

from typing import Sequence

from sifr.domain.models import Project
from sifr.ports.contracts import RepositoryPort


class InMemoryRepositoryAdapter(RepositoryPort):
    """In-memory implementation of the RepositoryPort."""

    def __init__(self) -> None:
        self._projects_by_id: dict[str, Project] = {}
        self._projects_by_name: dict[str, Project] = {}

    def save_project(self, project: Project) -> None:
        self._projects_by_id[project.project_id] = project
        self._projects_by_name[project.name] = project

    def get_project_by_id(self, project_id: str) -> Project | None:
        return self._projects_by_id.get(project_id)

    def get_project_by_name(self, name: str) -> Project | None:
        return self._projects_by_name.get(name)

    def list_projects(self) -> Sequence[Project]:
        return list(self._projects_by_id.values())
