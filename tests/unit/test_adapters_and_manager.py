"""Unit tests for Config and Persistence Adapters and Project Manager."""

from pathlib import Path
import pytest
from sifr.adapters.config.yaml_adapter import YamlConfigAdapter
from sifr.adapters.persistence.memory_adapter import InMemoryRepositoryAdapter
from sifr.adapters.persistence.sqlite_adapter import SQLiteRepositoryAdapter
from sifr.application.project_manager import ProjectManager
from sifr.domain.models import Project, ProjectConfig


def test_yaml_config_adapter(tmp_path: Path) -> None:
    adapter = YamlConfigAdapter()
    config_file = tmp_path / "sifr.yaml"

    config = ProjectConfig(
        name="test_proj",
        version="1.0.0",
        technology_profile="flutter",
        description="A Flutter App",
    )
    adapter.save_project_config(config_file, config)

    loaded = adapter.load_project_config(config_file)
    assert loaded.name == "test_proj"
    assert loaded.version == "1.0.0"
    assert loaded.technology_profile == "flutter"


def test_sqlite_repository_adapter(tmp_path: Path) -> None:
    db_file = tmp_path / "test.db"
    repo = SQLiteRepositoryAdapter(db_file)

    project = Project(
        name="fleet",
        root_path=tmp_path / "fleet",
        technology_profile_id="laravel",
    )
    repo.save_project(project)

    retrieved = repo.get_project_by_id(project.project_id)
    assert retrieved is not None
    assert retrieved.name == "fleet"
    assert retrieved.technology_profile_id == "laravel"

    by_name = repo.get_project_by_name("fleet")
    assert by_name is not None
    assert by_name.project_id == project.project_id

    all_projs = repo.list_projects()
    assert len(all_projs) == 1


def test_project_manager_workflow(tmp_path: Path) -> None:
    config_port = YamlConfigAdapter()
    repo_port = InMemoryRepositoryAdapter()
    pm = ProjectManager(config_port, repo_port)

    proj_dir = tmp_path / "my_app"
    project = pm.initialize_project("my_app", proj_dir, technology_profile="dotnet")

    assert project.name == "my_app"
    assert (proj_dir / "sifr.yaml").is_file()

    # Verify duplicate name rejection
    with pytest.raises(ValueError, match="already registered"):
        pm.initialize_project("my_app", tmp_path / "other")
