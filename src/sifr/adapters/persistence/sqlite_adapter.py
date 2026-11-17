"""SQLite Persistence Adapter for SIFR."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from typing import Sequence

from sifr.domain.models import Project, ProjectStatus
from sifr.ports.contracts import RepositoryPort


class SQLiteRepositoryAdapter(RepositoryPort):
    """SQLite implementation of the RepositoryPort."""

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
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version INTEGER PRIMARY KEY,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    project_id TEXT PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL,
                    root_path TEXT NOT NULL,
                    technology_profile_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    metadata_json TEXT NOT NULL
                )
            """)
            conn.commit()

    def save_project(self, project: Project) -> None:
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO projects (
                    project_id, name, root_path, technology_profile_id, status, created_at, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(project_id) DO UPDATE SET
                    name=excluded.name,
                    root_path=excluded.root_path,
                    technology_profile_id=excluded.technology_profile_id,
                    status=excluded.status,
                    metadata_json=excluded.metadata_json
            """, (
                project.project_id,
                project.name,
                str(project.root_path),
                project.technology_profile_id,
                project.status.value,
                project.created_at.isoformat(),
                json.dumps(project.metadata)
            ))
            conn.commit()

    def get_project_by_id(self, project_id: str) -> Project | None:
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM projects WHERE project_id = ?", (project_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return self._row_to_project(row)

    def get_project_by_name(self, name: str) -> Project | None:
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM projects WHERE name = ?", (name,))
            row = cursor.fetchone()
            if not row:
                return None
            return self._row_to_project(row)

    def list_projects(self) -> Sequence[Project]:
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM projects ORDER BY created_at DESC")
            return [self._row_to_project(row) for row in cursor.fetchall()]

    def _row_to_project(self, row: sqlite3.Row) -> Project:
        return Project(
            project_id=row["project_id"],
            name=row["name"],
            root_path=Path(row["root_path"]),
            technology_profile_id=row["technology_profile_id"],
            status=ProjectStatus(row["status"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            metadata=json.loads(row["metadata_json"])
        )
