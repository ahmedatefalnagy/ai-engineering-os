"""Structured logging and audit trail infrastructure for SIFR."""

from __future__ import annotations

import json
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class AuditLogger:
    """Provides structured JSON event logging and console output for SIFR operations."""

    def __init__(self, log_dir: Path | None = None) -> None:
        self.log_dir = log_dir or (Path.home() / ".sifr" / "logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.audit_file = self.log_dir / "audit.jsonl"

        self._logger = logging.getLogger("sifr")
        self._logger.setLevel(logging.INFO)
        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stderr)
            formatter = logging.Formatter("[%(levelname)s] %(message)s")
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    def log_event(self, event_type: str, payload: dict[str, Any], level: str = "INFO") -> None:
        """Records an auditable event with UTC timestamp in JSONL format."""
        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "event_type": event_type,
            "level": level.upper(),
            "payload": payload,
        }
        with open(self.audit_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def error(self, message: str) -> None:
        self._logger.error(message)
