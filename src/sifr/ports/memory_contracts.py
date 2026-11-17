"""Ports for Phase 4: Memory Manager, Technology Profiles, and Templates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from sifr.domain.memory_models import (
    MemoryCategory,
    MemoryDocument,
    ProjectTemplate,
    TechnologyProfile,
)


class MemoryRepositoryPort(ABC):
    """Port for indexing and querying markdown documents via SQLite."""

    @abstractmethod
    def save_document(self, doc: MemoryDocument) -> None:
        raise NotImplementedError

    @abstractmethod
    def search_documents(
        self,
        project_id: str,
        query: str,
        category: MemoryCategory | None = None,
    ) -> Sequence[MemoryDocument]:
        raise NotImplementedError


class ProfileRegistryPort(ABC):
    """Port for accessing technology profiles (Laravel, Flutter, Python, etc.)."""

    @abstractmethod
    def register_profile(self, profile: TechnologyProfile) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_profile(self, profile_id: str) -> TechnologyProfile | None:
        raise NotImplementedError

    @abstractmethod
    def list_profiles(self) -> Sequence[TechnologyProfile]:
        raise NotImplementedError


class TemplateRegistryPort(ABC):
    """Port for discovering project scaffolding templates."""

    @abstractmethod
    def register_template(self, template: ProjectTemplate) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_template(self, template_id: str) -> ProjectTemplate | None:
        raise NotImplementedError

    @abstractmethod
    def list_templates(self) -> Sequence[ProjectTemplate]:
        raise NotImplementedError
