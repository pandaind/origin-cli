"""Headroom-AI integration — transparent prompt compression via agent wrap."""

import typer
from origin_cli.utils import run_command
from origin_cli.integrations.prerequisites import check_command

# Agents that origin manages and that headroom supports wrapping
WRAPPED_AGENTS = ["copilot", "forge"]


def install() -> None:
    """Install headroom-ai via pipx."""
    typer.echo("Installing headroom-ai via pipx...")
    run_command(["pipx", "install", "headroom-ai"])

def uninstall() -> None:
    """Uninstall headroom-ai."""
    typer.echo("Uninstalling headroom-ai via pipx...")
    unwrap_agents()
    run_command(["pipx", "uninstall", "headroom-ai"], check=False)


def is_installed() -> bool:
    """Return True if the headroom binary is available on PATH."""
    return check_command("headroom")


def wrap_agents() -> None:
    """
    Wrap supported agents (copilot, forge) with headroom compression.
    Skips any agent that is not currently installed.
    """
    for agent in WRAPPED_AGENTS:
        if check_command(agent):
            typer.echo(f"  Wrapping '{agent}' with headroom compression...")
            run_command(["headroom", "wrap", agent], check=False)
            typer.secho(f"  ✔ '{agent}' wrapped — every LLM call will be compressed.", fg=typer.colors.GREEN)
        else:
            typer.secho(f"  Skipping '{agent}' (not installed).", fg=typer.colors.YELLOW)


def unwrap_agents() -> None:
    """Remove headroom compression from all wrapped agents."""
    for agent in WRAPPED_AGENTS:
        typer.echo(f"  Unwrapping '{agent}'...")
        run_command(["headroom", "unwrap", agent], check=False)
