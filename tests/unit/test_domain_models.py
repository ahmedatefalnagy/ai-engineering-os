"""Unit tests for Core Domain Models."""

from pathlib import Path

from sifr.domain.models import IntegrationType, Project, ProjectStatus


def test_project_instantiation() -> None:
    root = Path("/tmp/sample_project")
    project = Project(
        name="sample",
        root_path=root,
        technology_profile_id="laravel",
    )
    assert project.name == "sample"
    assert project.technology_profile_id == "laravel"
    assert project.status == ProjectStatus.INITIALIZED
    assert project.project_id is not None


def test_project_path_security_guard() -> None:
    root = Path("/tmp/sample_project").resolve()
    project = Project(name="sample", root_path=root, technology_profile_id="generic")

    inside_file = root / "src" / "index.php"
    outside_file = Path("/etc/passwd").resolve()

    assert project.is_path_within_project(inside_file) is True
    assert project.is_path_within_project(outside_file) is False


def test_integration_types_enum() -> None:
    assert IntegrationType.NATIVE_PROVIDER.value == "native_provider"
    assert IntegrationType.MODEL_GATEWAY.value == "model_gateway"
    assert IntegrationType.CODING_TOOL.value == "coding_tool"
    assert IntegrationType.SPEC_FRAMEWORK.value == "spec_framework"
