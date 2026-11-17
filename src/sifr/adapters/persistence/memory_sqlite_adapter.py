"""SQLite Memory Repository implementation for text indexing and context retrieval."""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path

from sifr.domain.memory_models import MemoryCategory, MemoryDocument
from sifr.ports.memory_contracts import MemoryRepositoryPort


class SQLiteMemoryRepositoryAdapter(MemoryRepositoryPort):
    """Indexes memory documents using SQLite with full-text search capability."""

    def __init__(self, db_path: Path | str = ":memory:") -> None:
        self.db_path = str(db_path)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memory_documents (
                    doc_id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    markdown_content TEXT NOT NULL,
                    tags_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()

    def save_document(self, doc: MemoryDocument) -> None:
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO memory_documents (
                    doc_id, project_id, title, category, markdown_content, tags_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(doc_id) DO UPDATE SET
                    title=excluded.title,
                    markdown_content=excluded.markdown_content,
                    tags_json=excluded.tags_json
            """,
                (
                    doc.doc_id,
                    doc.project_id,
                    doc.title,
                    doc.category.value,
                    doc.markdown_content,
                    json.dumps(doc.tags),
                    doc.created_at.isoformat(),
                ),
            )
            conn.commit()

    def search_documents(
        self,
        project_id: str,
        query: str,
        category: MemoryCategory | None = None,
    ) -> Sequence[MemoryDocument]:
        with self._get_connection() as conn:
            like_query = f"%{query}%"
            if category:
                cursor = conn.execute(
                    """
                    SELECT * FROM memory_documents
                    WHERE project_id = ? AND category = ?
                      AND (title LIKE ? OR markdown_content LIKE ? OR tags_json LIKE ?)
                    ORDER BY created_at DESC
                """,
                    (project_id, category.value, like_query, like_query, like_query),
                )
            else:
                cursor = conn.execute(
                    """
                    SELECT * FROM memory_documents
                    WHERE project_id = ?
                      AND (title LIKE ? OR markdown_content LIKE ? OR tags_json LIKE ?)
                    ORDER BY created_at DESC
                """,
                    (project_id, like_query, like_query, like_query),
                )

            return [
                MemoryDocument(
                    doc_id=row["doc_id"],
                    project_id=row["project_id"],
                    title=row["title"],
                    category=MemoryCategory(row["category"]),
                    markdown_content=row["markdown_content"],
                    tags=json.loads(row["tags_json"]),
                    created_at=datetime.fromisoformat(row["created_at"]),
                )
                for row in cursor.fetchall()
            ]
