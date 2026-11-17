"""Command Line Interface for SIFR — AI Engineering OS."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from sifr.adapters.config.yaml_adapter import YamlConfigAdapter
from sifr.adapters.persistence.sqlite_adapter import SQLiteRepositoryAdapter
from sifr.application.logging import AuditLogger
from sifr.application.project_manager import ProjectManager
from sifr.domain.errors import SifrError

app = typer.Typer(
    name="sifr",
    help="SIFR — AI Engineering OS: Modular, vendor-agnostic software engineering operating system.",
    add_completion=False,
)
console = Console()


def _get_db_path() -> Path:
    env_db = os.getenv("SIFR_DB_PATH")
    if env_db:
        return Path(env_db)
    return Path.home() / ".sifr" / "sifr_state.db"


def _get_project_manager() -> ProjectManager:
    db_path = _get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    repo = SQLiteRepositoryAdapter(db_path)
    config = YamlConfigAdapter()
    audit = AuditLogger(db_path.parent / "logs")
    return ProjectManager(config, repo, audit)


@app.command("version")
def version() -> None:
    """Displays SIFR system version and status."""
    console.print("[bold cyan]SIFR — AI Engineering OS[/bold cyan] [green]v0.1.0[/green]")
    console.print("[italic dim]From a Small Core to Systems Without Limits.[/italic dim]")


@app.command("init")
def init(
    name: str = typer.Argument(..., help="Name of the new project"),
    path: Path = typer.Option(Path("."), "--path", "-p", help="Target project root directory"),
    profile: str = typer.Option("generic", "--profile", help="Technology profile ID"),
    desc: str = typer.Option("", "--desc", "-d", help="Short project description"),
) -> None:
    """Initializes a new SIFR project in the target directory."""
    pm = _get_project_manager()
    try:
        project = pm.initialize_project(
            name=name,
            target_dir=path,
            technology_profile=profile,
            description=desc,
        )
        console.print(
            f"[bold green]✓ Initialized project:[/bold green] [cyan]{project.name}[/cyan]"
        )
        console.print(f"  [dim]ID:[/dim] {project.project_id}")
        console.print(f"  [dim]Root Path:[/dim] {project.root_path}")
        console.print(f"  [dim]Profile:[/dim] {project.technology_profile_id}")
    except SifrError as e:
        console.print(f"[bold red]Error:[/bold red] {e.message}")
        sys.exit(e.exit_code)
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/bold red] {e}")
        sys.exit(1)


@app.command("list")
def list_projects() -> None:
    """Lists all SIFR registered projects."""
    pm = _get_project_manager()
    projects = pm.list_all_projects()

    if not projects:
        console.print(
            "[yellow]No registered projects found. Use `sifr init <name>` to start.[/yellow]"
        )
        return

    table = Table(title="SIFR Registered Projects", header_style="bold magenta")
    table.add_column("Name", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Profile", style="yellow")
    table.add_column("Path", style="dim")
    table.add_column("Created At", style="dim")

    for p in projects:
        table.add_row(
            p.name,
            p.status.value,
            p.technology_profile_id,
            str(p.root_path),
            p.created_at.strftime("%Y-%m-%d %H:%M"),
        )

    console.print(table)


@app.command("show")
def show_project(name_or_id: str = typer.Argument(..., help="Project name or ID")) -> None:
    """Shows detailed information about a registered project."""
    pm = _get_project_manager()
    try:
        project = pm.get_project(name_or_id)
        panel_content = f"""[bold cyan]Name:[/bold cyan] {project.name}
[bold cyan]ID:[/bold cyan] {project.project_id}
[bold cyan]Status:[/bold cyan] {project.status.value}
[bold cyan]Technology Profile:[/bold cyan] {project.technology_profile_id}
[bold cyan]Root Path:[/bold cyan] {project.root_path}
[bold cyan]Registered At:[/bold cyan] {project.created_at.isoformat()}"""
        console.print(Panel(panel_content, title=f"Project: {project.name}", expand=False))
    except SifrError as e:
        console.print(f"[bold red]Error:[/bold red] {e.message}")
        sys.exit(e.exit_code)


if __name__ == "__main__":
    app()
