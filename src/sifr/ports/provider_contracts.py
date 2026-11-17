"""Ports for Phase 3: Provider contracts, Model Registry, and Cost Tracking."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from sifr.domain.provider_models import ModelDescriptor, ModelUsage, ProviderResponse


class ProviderPort(ABC):
    """Normalized port that every AI Provider (or Gateway) must implement."""

    @property
    @abstractmethod
    def provider_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def complete(self, prompt: str, model_id: str | None = None) -> ProviderResponse:
        """Executes a synchronous model completion."""
        raise NotImplementedError


class ModelRegistryPort(ABC):
    """Port for querying available models and capabilities."""

    @abstractmethod
    def register_model(self, descriptor: ModelDescriptor) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_model(self, model_id: str) -> ModelDescriptor | None:
        raise NotImplementedError

    @abstractmethod
    def list_models(self) -> Sequence[ModelDescriptor]:
        raise NotImplementedError


class CostTrackerPort(ABC):
    """Port for recording token usage, tracking budget, and blocking on limits."""

    @abstractmethod
    def record_usage(self, project_id: str, usage: ModelUsage) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_project_total_cost(self, project_id: str) -> float:
        raise NotImplementedError

    @abstractmethod
    def check_budget_limit(self, project_id: str, budget_limit_usd: float) -> bool:
        """Returns True if project spending is strictly below the budget limit."""
        raise NotImplementedError
