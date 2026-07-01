import typer
from origin_cli.integrations import agent_forge, speckit
from origin_cli.integrations.prerequisites import ensure_node_npm, ensure_pipx

def setup_command(
    copilot: bool = typer.Option(None, "--copilot/--no-copilot", help="Install GitHub Copilot CLI and Agent Forge globally via npm"),
    spec: bool = typer.Option(None, "--spec/--no-spec", help="Install Spec Kit (specify-cli) for spec-driven development"),
):
    """
    Bootstraps your machine with the AI development dependencies.

    Two modes:
      Spec-driven  — installs Agent Forge + Spec Kit (full Coordinator-Worker setup)
      Agent-driven — installs Agent Forge only (no Spec Kit)
    """
    # ── Mode selection ──────────────────────────────────────────────────────
    if spec is None:
        typer.secho("\nSelect your development mode:", fg=typer.colors.CYAN, bold=True)
        typer.echo("  [1] Spec-driven  — Agent Forge + Spec Kit (recommended for full workflows)")
        typer.echo("  [2] Agent-driven — Agent Forge only (no Spec Kit)\n")

        while True:
            choice = typer.prompt("Enter your choice", default="1")
            if choice in ("1", "2"):
                break
            typer.secho("  Please enter 1 or 2.", fg=typer.colors.RED)

        spec = choice == "1"

    if spec:
        typer.secho("Mode: Spec-driven (Agent Forge + Spec Kit)", fg=typer.colors.GREEN)
    else:
        typer.secho("Mode: Agent-driven (Agent Forge only)", fg=typer.colors.YELLOW)

    # ── Prerequisites ───────────────────────────────────────────────────────
    typer.secho("\nChecking prerequisites...", fg=typer.colors.CYAN)
    ensure_node_npm()
    if spec:
        ensure_pipx()

    # ── Agent Forge ─────────────────────────────────────────────────────────
    if copilot is None:
        copilot = typer.confirm(
            "\nInstall GitHub Copilot CLI and Agent Forge globally via npm?",
            default=True,
        )

    if copilot:
        agent_forge.install()
    else:
        typer.secho("Skipping GitHub Copilot CLI and Agent Forge installation.", fg=typer.colors.YELLOW)

    # ── Spec Kit ────────────────────────────────────────────────────────────
    if spec:
        speckit.install()
    else:
        typer.secho("Skipping Spec Kit installation (agent-driven mode).", fg=typer.colors.YELLOW)

    typer.secho("\nSetup complete! Dependencies are installed.", fg=typer.colors.GREEN, bold=True)
