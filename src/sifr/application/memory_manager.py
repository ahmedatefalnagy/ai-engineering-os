"""Memory Manager and Context Retrieval Use Cases."""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from pathlib import Path

from sifr.application.logging import AuditLogger
from sifr.domain.memory_models import MemoryCategory, MemoryDocument
from sifr.ports.memory_contracts import MemoryRepositoryPort


class MemoryManager:
    """Stores human-readable Markdown files in project directories while indexing them in SQLite."""

    def __init__(
        self,
        memory_repo: MemoryRepositoryPort,
        audit_logger: AuditLogger | None = None,
    ) -> None:
        self.memory_repo = memory_repo
        self.audit = audit_logger or AuditLogger()

    def record_document(
        self,
        project_id: str,
        project_root: Path,
        title: str,
        category: MemoryCategory,
        content: str,
        tags: list[str] | None = None,
    ) -> MemoryDocument:
        doc_id = str(uuid.uuid4())
        doc = MemoryDocument(
            title=title,
            category=category,
            markdown_content=content,
            project_id=project_id,
            doc_id=doc_id,
            tags=tags or [],
        )

        # 1. Save Markdown file on disk for human transparency
        docs_dir = project_root / ".sifr" / "memory" / category.value
        docs_dir.mkdir(parents=True, exist_ok=True)
        safe_filename = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in title.lower())
        file_path = docs_dir / f"{safe_filename}.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(
                f"# {title}\n\n**Category:** {category.value}\n**Tags:** {', '.join(doc.tags)}\n\n---\n\n{content}\n"
            )

        # 2. Index in SQLite for fast full-text lookup
        self.memory_repo.save_document(doc)
        self.audit.log_event(
            "memory_document_recorded",
            {
                "project_id": project_id,
                "doc_id": doc_id,
                "title": title,
                "category": category.value,
            },
        )
        return doc

    def query_context(
        self,
        project_id: str,
        query: str,
        category: MemoryCategory | None = None,
    ) -> Sequence[MemoryDocument]:
        """Retrieves minimal necessary context without bloating token budgets."""
        results = self.memory_repo.search_documents(project_id, query, category)
        self.audit.log_event(
            "memory_query_executed",
            {
                "project_id": project_id,
                "query": query,
                "matches_count": len(results),
            },
        )
        return results
