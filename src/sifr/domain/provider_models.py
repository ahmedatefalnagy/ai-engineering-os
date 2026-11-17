"""Domain models for Phase 3: Providers, Model Routing, and Cost Tracking."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum


class ModelTier(StrEnum):
    FRONTIER = "frontier"  # Complex architecture, high-stakes decisions (Opus, GPT-4o)
    BALANCED = "balanced"  # Code generation, reasoning, refactoring (Sonnet, DeepSeek-V3/R1)
    FAST = "fast"  # Routine edits, unit tests, summarization (Gemini Flash, Haiku)
    LOCAL = "local"  # Offline, private execution (Ollama / Llama3)


class ModelClass(StrEnum):
    FREE = "free"
    PAID = "paid"
    LOCAL = "local"


@dataclass(frozen=True)
class ModelDescriptor:
    """Registered metadata and capabilities for an AI model."""

    model_id: str
    provider_id: str
    tier: ModelTier
    model_class: ModelClass
    context_window: int
    cost_per_million_input: float
    cost_per_million_output: float
    supports_tools: bool = True
    supports_vision: bool = False
    verified_at: str = "2026-11-17"
    source_url: str = "https://sifr.local/docs/models"


@dataclass(frozen=True)
class ModelUsage:
    """Token consumption and monetary cost for a single model call."""

    model_id: str
    provider_id: str
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class ProviderResponse:
    """Normalized response returned by any Model Provider adapter."""

    content: str
    usage: ModelUsage
    model_id: str
    finish_reason: str = "stop"
