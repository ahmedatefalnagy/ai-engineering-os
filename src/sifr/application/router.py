"""Model Router and Cost Tracker Use Cases."""

from __future__ import annotations

from collections.abc import Sequence

from sifr.application.logging import AuditLogger
from sifr.domain.errors import SifrError
from sifr.domain.provider_models import (
    ModelClass,
    ModelDescriptor,
    ModelTier,
    ModelUsage,
    ProviderResponse,
)
from sifr.ports.provider_contracts import (
    CostTrackerPort,
    ModelRegistryPort,
    ProviderPort,
)


class BudgetExceededError(SifrError):
    def __init__(self, project_id: str, cost: float, limit: float) -> None:
        super().__init__(
            f"Budget limit exceeded for project '{project_id}': total ${cost:.4f} >= limit ${limit:.4f}",
            exit_code=20,
        )


class ModelRouter:
    """Selects the optimal model and provider based on task tier, cost awareness, and local availability."""

    def __init__(
        self,
        registry: ModelRegistryPort,
        providers: dict[str, ProviderPort],
        cost_tracker: CostTrackerPort,
        audit_logger: AuditLogger | None = None,
    ) -> None:
        self.registry = registry
        self.providers = providers
        self.cost_tracker = cost_tracker
        self.audit = audit_logger or AuditLogger()

    def select_model(
        self,
        tier: ModelTier = ModelTier.BALANCED,
        prefer_local: bool = False,
    ) -> ModelDescriptor:
        models = self.registry.list_models()
        matching: list[ModelDescriptor] = []

        if prefer_local:
            matching = [
                m
                for m in models
                if m.model_class in (ModelClass.LOCAL, ModelClass.FREE) and m.tier == tier
            ]

        if not matching:
            matching = [m for m in models if m.tier == tier]

        if not matching:
            # Fallback to any available model
            if not models:
                raise SifrError("No models registered in Model Registry", exit_code=21)
            matching = list(models)

        # Sort by cost (quality-first with cost-awareness: pick lowest cost within the required tier)
        matching.sort(key=lambda m: m.cost_per_million_input + m.cost_per_million_output)
        return matching[0]

    def execute_completion(
        self,
        project_id: str,
        prompt: str,
        tier: ModelTier = ModelTier.BALANCED,
        prefer_local: bool = False,
        budget_limit_usd: float | None = None,
    ) -> ProviderResponse:
        # 1. Budget enforcement check
        if budget_limit_usd is not None and not self.cost_tracker.check_budget_limit(
            project_id, budget_limit_usd
        ):
            current_cost = self.cost_tracker.get_project_total_cost(project_id)
            raise BudgetExceededError(project_id, current_cost, budget_limit_usd)

        # 2. Select optimal model
        selected_model = self.select_model(tier=tier, prefer_local=prefer_local)

        provider = self.providers.get(selected_model.provider_id)
        if not provider:
            raise SifrError(
                f"Provider adapter '{selected_model.provider_id}' is not loaded/configured",
                exit_code=22,
            )

        # 3. Call provider
        response = provider.complete(prompt, model_id=selected_model.model_id)

        # 4. Record cost & audit
        self.cost_tracker.record_usage(project_id, response.usage)
        self.audit.log_event(
            "model_completion",
            {
                "project_id": project_id,
                "model_id": response.model_id,
                "provider_id": response.usage.provider_id,
                "cost_usd": response.usage.cost_usd,
            },
        )
        return response


class InMemoryCostTracker(CostTrackerPort):
    """In-memory cost tracking implementation."""

    def __init__(self) -> None:
        self.usage_records: dict[str, list[ModelUsage]] = {}

    def record_usage(self, project_id: str, usage: ModelUsage) -> None:
        self.usage_records.setdefault(project_id, []).append(usage)

    def get_project_total_cost(self, project_id: str) -> float:
        records = self.usage_records.get(project_id, [])
        return sum(r.cost_usd for r in records)

    def check_budget_limit(self, project_id: str, budget_limit_usd: float) -> bool:
        return self.get_project_total_cost(project_id) < budget_limit_usd


class InMemoryModelRegistry(ModelRegistryPort):
    """In-memory model registry implementation."""

    def __init__(self) -> None:
        self._models: dict[str, ModelDescriptor] = {}

    def register_model(self, descriptor: ModelDescriptor) -> None:
        self._models[descriptor.model_id] = descriptor

    def get_model(self, model_id: str) -> ModelDescriptor | None:
        return self._models.get(model_id)

    def list_models(self) -> Sequence[ModelDescriptor]:
        return list(self._models.values())
