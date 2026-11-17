"""Unit tests for Phase 3: Model Router, Cost Tracking, and Budget Limits."""

import pytest

from sifr.adapters.providers.mock_adapter import MockProviderAdapter
from sifr.application.router import (
    BudgetExceededError,
    InMemoryCostTracker,
    InMemoryModelRegistry,
    ModelRouter,
)
from sifr.domain.provider_models import (
    ModelClass,
    ModelDescriptor,
    ModelTier,
)


def test_model_routing_and_budget_enforcement() -> None:
    registry = InMemoryModelRegistry()
    cost_tracker = InMemoryCostTracker()

    # Register local fast model
    local_model = ModelDescriptor(
        model_id="llama3-8b",
        provider_id="ollama",
        tier=ModelTier.FAST,
        model_class=ModelClass.LOCAL,
        context_window=8192,
        cost_per_million_input=0.0,
        cost_per_million_output=0.0,
    )
    registry.register_model(local_model)

    # Register balanced paid model
    paid_model = ModelDescriptor(
        model_id="deepseek-v3",
        provider_id="deepseek",
        tier=ModelTier.BALANCED,
        model_class=ModelClass.PAID,
        context_window=64000,
        cost_per_million_input=0.14,
        cost_per_million_output=0.28,
    )
    registry.register_model(paid_model)

    # Setup mock provider adapters
    ollama_mock = MockProviderAdapter(
        mock_response="Local generation", provider_name="ollama", fixed_cost=0.0
    )
    deepseek_mock = MockProviderAdapter(
        mock_response="DeepSeek generation", provider_name="deepseek", fixed_cost=0.05
    )

    providers = {
        "ollama": ollama_mock,
        "deepseek": deepseek_mock,
    }

    router = ModelRouter(registry=registry, providers=providers, cost_tracker=cost_tracker)

    # 1. Routing for local/fast
    resp_local = router.execute_completion(
        project_id="p1",
        prompt="Write a unit test",
        tier=ModelTier.FAST,
        prefer_local=True,
    )
    assert resp_local.content == "Local generation"
    assert resp_local.usage.cost_usd == 0.0

    # 2. Routing for balanced/paid
    resp_paid = router.execute_completion(
        project_id="p1",
        prompt="Refactor database layer",
        tier=ModelTier.BALANCED,
        budget_limit_usd=1.0,  # Limit is $1.0, current cost is $0.05 -> Should succeed
    )
    assert resp_paid.content == "DeepSeek generation"
    assert resp_paid.usage.cost_usd == 0.05
    assert cost_tracker.get_project_total_cost("p1") == 0.05

    # 3. Budget limit violation (setting limit below accumulated cost)
    with pytest.raises(BudgetExceededError):
        router.execute_completion(
            project_id="p1",
            prompt="Another big prompt",
            tier=ModelTier.BALANCED,
            budget_limit_usd=0.04,  # $0.05 >= $0.04 -> Blocking
        )
