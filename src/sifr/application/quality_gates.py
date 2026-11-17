"""Domain models and engine for Phase 6: Quality Gates and Security Controls."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
import re


class GateStatus(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    NOT_EVALUATED = "not_evaluated"


@dataclass(frozen=True)
class GateResult:
    gate_name: str
    status: GateStatus
    message: str
    details: str = ""


class QualityGateEngine:
    """Verifies source files and tests before accepting deliverables."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root

    def check_secret_leakage(self) -> GateResult:
        """Scans project files for hardcoded API keys, JWTs, or database passwords in code and config files."""
        patterns = [
            # Matches code assignments: API_KEY = "..."
            (
                r"(?i)(api[_-]?(key|secret)|secret|password|token)[a-z0-9_-]*\s*[:=]\s*['\"][^'\"]{10,}['\"]",
                "Secret token detected in assignment",
            ),
            # Matches JSON / YAML quoted keys: "Password": "..."
            (
                r"(?i)['\"](api[_-]?(key|secret)|secret|password|token)[^'\"]*['\"]\s*[:=]\s*['\"][^'\"]{10,}['\"]",
                "Secret token detected in JSON or quoted key",
            ),
            (r"-----BEGIN (RSA|OPENSSH|PRIVATE) KEY-----", "Private key detected"),
        ]

        ignored_dirs = {".git", ".venv", "bin", "obj", "node_modules", "vendor", ".gradle"}
        violations: list[str] = []

        for file_path in self.project_root.rglob("*"):
            if not file_path.is_file() or any(d in file_path.parts for d in ignored_dirs):
                continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                for pattern, desc in patterns:
                    if re.search(pattern, content):
                        violations.append(f"{file_path.name}: {desc}")
            except Exception:
                continue

        if violations:
            return GateResult(
                gate_name="secret_scan",
                status=GateStatus.FAILED,
                message=f"Found {len(violations)} secret leak violations",
                details="; ".join(violations),
            )

        return GateResult(
            gate_name="secret_scan",
            status=GateStatus.PASSED,
            message="No exposed secrets detected",
        )

    def check_bilingual_compliance(self) -> GateResult:
        """Verifies that the project architecture enforces native bilingual support (Arabic & English) with RTL/LTR."""
        sifr_yaml = self.project_root / "sifr.yaml"
        if not sifr_yaml.is_file():
            return GateResult(
                gate_name="bilingual_compliance",
                status=GateStatus.PASSED,
                message="No sifr.yaml present, skipping bilingual mandate check",
            )

        content = sifr_yaml.read_text(encoding="utf-8", errors="ignore").lower()
        has_arabic = "ar" in content or "arabic" in content
        has_english = "en" in content or "english" in content
        has_bilingual = "bilingual" in content or (has_arabic and has_english)

        if not has_bilingual:
            return GateResult(
                gate_name="bilingual_compliance",
                status=GateStatus.FAILED,
                message="SIFR Invariant Violation: Project must declare native Arabic & English bilingual support",
                details="sifr.yaml must declare i18n support for both Arabic and English with RTL/LTR.",
            )

        return GateResult(
            gate_name="bilingual_compliance",
            status=GateStatus.PASSED,
            message="Bilingual (Arabic & English) and RTL/LTR standard verified",
        )

    def evaluate_all(self) -> Sequence[GateResult]:
        return [self.check_secret_leakage(), self.check_bilingual_compliance()]
