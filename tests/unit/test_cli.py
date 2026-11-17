"""Unit tests for SIFR CLI commands."""

from typer.testing import CliRunner

from sifr.cli.main import app

runner = CliRunner()


def test_cli_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "SIFR — AI Engineering OS" in result.stdout
    assert "v0.1.0" in result.stdout


def test_cli_init_list_and_show(tmp_path, monkeypatch) -> None:
    db_file = tmp_path / "cli_test.db"
    monkeypatch.setenv("SIFR_DB_PATH", str(db_file))

    proj_dir = tmp_path / "demo_app"
    result = runner.invoke(
        app, ["init", "demo_app", "--path", str(proj_dir), "--profile", "laravel"]
    )
    assert result.exit_code == 0
    assert "Initialized project" in result.stdout

    # List projects
    list_result = runner.invoke(app, ["list"])
    assert list_result.exit_code == 0
    assert "demo_app" in list_result.stdout
    assert "laravel" in list_result.stdout

    # Show project
    show_result = runner.invoke(app, ["show", "demo_app"])
    assert show_result.exit_code == 0
    assert "Project: demo_app" in show_result.stdout
    assert "laravel" in show_result.stdout


def test_cli_show_non_existent(tmp_path, monkeypatch) -> None:
    db_file = tmp_path / "cli_test.db"
    monkeypatch.setenv("SIFR_DB_PATH", str(db_file))

    result = runner.invoke(app, ["show", "does_not_exist"])
    assert result.exit_code == 2
    assert "Project not found" in result.stdout
