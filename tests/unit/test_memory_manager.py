"""Unit tests for Phase 4: Markdown+SQLite Memory, indexing, and context retrieval."""

from pathlib import Path

from sifr.adapters.persistence.memory_sqlite_adapter import SQLiteMemoryRepositoryAdapter
from sifr.application.memory_manager import MemoryManager
from sifr.domain.memory_models import MemoryCategory


def test_memory_document_lifecycle(tmp_path: Path) -> None:
    db_file = tmp_path / "memory_test.db"
    adapter = SQLiteMemoryRepositoryAdapter(db_file)
    manager = MemoryManager(adapter)

    proj_dir = tmp_path / "my_project"
    proj_dir.mkdir()

    # 1. Record an architectural decision
    doc = manager.record_document(
        project_id="proj_1",
        project_root=proj_dir,
        title="ADR-001 Use Hexagonal Architecture",
        category=MemoryCategory.DECISION,
        content="We chose Ports and Adapters to isolate core domain logic from external dependencies.",
        tags=["architecture", "hexagonal"],
    )

    # Verify markdown file exists on disk
    md_file = proj_dir / ".sifr" / "memory" / "decision" / "adr-001_use_hexagonal_architecture.md"
    assert md_file.is_file()
    assert "Ports and Adapters" in md_file.read_text()

    # 2. Query context by text search
    matches = manager.query_context(project_id="proj_1", query="Ports")
    assert len(matches) == 1
    assert matches[0].doc_id == doc.doc_id

    # 3. Query context with category filter
    decision_matches = manager.query_context(
        project_id="proj_1",
        query="architecture",
        category=MemoryCategory.DECISION,
    )
    assert len(decision_matches) == 1

    # Unrelated category search
    empty_matches = manager.query_context(
        project_id="proj_1",
        query="architecture",
        category=MemoryCategory.INCIDENT,
    )
    assert len(empty_matches) == 0
