"""Unit tests for SIFR CLI commands."""

from typer.testing import CliRunner
from sifr.cli.main import app

runner = CliRunner()


def test_cli_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "SIFR — AI Engineering OS" in result.stdout
    assert "v0.1.0" in result.stdout


def test_cli_init_and_list(tmp_path) -> None:
    proj_dir = tmp_path / "demo_app"
    result = runner.invoke(app, ["init", "demo_app", "--path", str(proj_dir), "--profile", "laravel"])
    assert result.exit_code == 0
    assert "Initialized project" in result.stdout

    # List projects
    list_result = runner.invoke(app, ["list"])
    assert list_result.exit_code == 0
    assert "demo_app" in list_result.stdout
    assert "laravel" in list_result.stdout
