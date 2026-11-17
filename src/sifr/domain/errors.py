"""Custom domain exceptions and error taxonomy for SIFR."""

from __future__ import annotations


class SifrError(Exception):
    """Base exception for all SIFR system errors."""

    def __init__(self, message: str, exit_code: int = 1) -> None:
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code


class ProjectNotFoundError(SifrError):
    """Raised when a requested project cannot be located."""

    def __init__(self, identifier: str) -> None:
        super().__init__(f"Project not found: '{identifier}'", exit_code=2)


class ProjectAlreadyExistsError(SifrError):
    """Raised when attempting to register a project name that already exists."""

    def __init__(self, name: str) -> None:
        super().__init__(f"Project already registered: '{name}'", exit_code=3)


class ConfigurationError(SifrError):
    """Raised when configuration loading or schema validation fails."""

    def __init__(self, reason: str) -> None:
        super().__init__(f"Configuration error: {reason}", exit_code=4)


class SecurityViolationError(SifrError):
    """Raised when an operation attempts to access paths or resources outside permitted scope."""

    def __init__(self, detail: str) -> None:
        super().__init__(f"Security violation: {detail}", exit_code=5)
