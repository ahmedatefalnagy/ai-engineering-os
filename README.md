# SIFR — AI Engineering OS

> **"From a Small Core to Systems Without Limits"**

**SIFR** is a vendor-agnostic, technology-independent AI Engineering Operating System designed to plan, scaffold, verify, and orchestrate software engineering workflows with strict quality gates, budget management, and verifiable architecture.

---

## 🚀 Key Architectural Principles
- **Hexagonal Architecture:** Strict separation between pure Domain Models, Application Use Cases, Ports, and Adapters.
- **CLI-First:** Built from the ground up for command-line operation.
- **Provider & Tech Agnostic:** Runs on Python 3.12+, but manages projects in Flutter, Laravel, .NET, React, Go, and more.
- **No Mandatory External AI Providers:** Operates offline with mock providers for deterministic contract testing.
- **Local-First & Safe:** Markdown + SQLite for memory and audit trails. Budget limits warning and blocking by default.

---

## 🛠️ Development Setup

### Requirements
- Linux / Ubuntu
- Python `>= 3.12`
- `uv` package manager

### Getting Started
```bash
# Sync environment and dependencies
uv sync --extra dev

# Run unit and architecture boundary tests
uv run pytest

# Check code style and type safety
uv run ruff check .
uv run mypy src
```

---

## 📚 Documentation
Detailed architectural blueprints, requirements matrix, and decisions are maintained in the [`docs/`](docs/) directory:
- [Architecture Proposal](docs/ARCHITECTURE_PROPOSAL.md)
- [Requirements Register](docs/REQUIREMENTS.md)
- [Traceability Matrix](docs/TRACEABILITY.md)
- [Decisions (ADRs)](docs/DECISIONS.md)
- [Roadmap](docs/ROADMAP.md)
- [Project State](docs/PROJECT_STATE.md)
