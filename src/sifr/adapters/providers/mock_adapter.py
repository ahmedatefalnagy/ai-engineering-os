"""Mock Provider Adapter for deterministic, network-free testing of SIFR."""

from __future__ import annotations

from sifr.domain.provider_models import ModelUsage, ProviderResponse
from sifr.ports.provider_contracts import ProviderPort


class MockProviderAdapter(ProviderPort):
    """Deterministic, zero-cost mock provider conforming to ProviderPort."""

    def __init__(
        self,
        mock_response: str = "Mock generation completed successfully.",
        provider_name: str = "mock",
        fixed_cost: float = 0.0,
    ) -> None:
        self._provider_name = provider_name
        self._response = mock_response
        self._cost = fixed_cost
        self.call_history: list[str] = []

    @property
    def provider_id(self) -> str:
        return self._provider_name

    def complete(self, prompt: str, model_id: str | None = None) -> ProviderResponse:
        self.call_history.append(prompt)
        target_model = model_id or "mock-model-v1"
        usage = ModelUsage(
            model_id=target_model,
            provider_id=self._provider_name,
            prompt_tokens=len(prompt.split()),
            completion_tokens=len(self._response.split()),
            cost_usd=self._cost,
        )
        return ProviderResponse(
            content=self._response,
            usage=usage,
            model_id=target_model,
        )
