"""Architecture Boundary tests to strictly enforce Hexagonal Architecture.

Ensures that Domain and Ports never import from Adapters or Frameworks.
"""

import importlib
import inspect
from pathlib import Path
import sifr.domain.models
import sifr.ports.contracts


def test_domain_has_no_adapter_imports() -> None:
    source = inspect.getsource(sifr.domain.models)
    forbidden_terms = ["adapters", "sqlite3", "yaml", "typer", "rich", "pydantic"]
    for term in forbidden_terms:
        assert f"import {term}" not in source, f"Domain model must not import {term}"
        assert f"from {term}" not in source, f"Domain model must not import {term}"


def test_ports_has_no_adapter_imports() -> None:
    source = inspect.getsource(sifr.ports.contracts)
    forbidden_terms = ["adapters", "sqlite3", "yaml", "typer", "rich"]
    for term in forbidden_terms:
        assert f"import {term}" not in source, f"Ports must not import {term}"
        assert f"from {term}" not in source, f"Ports must not import {term}"
