"""Unit tests for Phase 5 & 6: Coding tools, Spec generation, and Quality Gates."""

from pathlib import Path

from sifr.adapters.tools.coding_adapters import (
    AntigravityToolAdapter,
    CursorToolAdapter,
    SpecKitAdapter,
)
from sifr.application.quality_gates import GateStatus, QualityGateEngine


def test_cursor_and_antigravity_adapters(tmp_path: Path) -> None:
    # 1. Cursor adapter
    cursor = CursorToolAdapter()
    res = cursor.execute_task(tmp_path, "Follow PEP8 conventions.")
    assert res.success is True
    assert (tmp_path / ".cursorrules").is_file()

    # 2. Antigravity adapter
    antigravity = AntigravityToolAdapter()
    ag_res = antigravity.execute_task(tmp_path, "Analyze project boundaries.")
    assert ag_res.success is True
    assert (tmp_path / ".antigravity" / "instructions.md").is_file()

    # 3. Spec Kit adapter
    spec_kit = SpecKitAdapter()
    spec_file = spec_kit.generate_spec(tmp_path, "As a developer I want quality gates")
    assert spec_file.is_file()
    assert "Functional Specification" in spec_file.read_text()


def test_quality_gate_secret_scanner(tmp_path: Path) -> None:
    engine = QualityGateEngine(tmp_path)

    # Clean project check
    clean_file = tmp_path / "main.py"
    clean_file.write_text("print('Clean project without secrets')")

    res_clean = engine.check_secret_leakage()
    assert res_clean.status == GateStatus.PASSED

    # Leaked secret check
    leaked_file = tmp_path / "config.py"
    leaked_file.write_text("API_SECRET_KEY = 'sk-proj-1234567890abcdef1234567890'")

    res_leaked = engine.check_secret_leakage()
    assert res_leaked.status == GateStatus.FAILED
    assert "secret leak" in res_leaked.message
