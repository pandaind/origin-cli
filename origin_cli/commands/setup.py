import typer
from origin_cli.integrations import agent_forge, speckit
from origin_cli.integrations.prerequisites import ensure_node_npm, ensure_pipx

def setup_command(
    copilot: bool = typer.Option(None, "--copilot/--no-copilot", help="Install GitHub Copilot CLI and Agent Forge globally via npm")
):
    """
    Checks for and installs underlying CLI dependencies:
    - node + npm (required for @github/copilot and @agent-forge-copilot/cli)
    - pipx (used to install specify-cli in an isolated environment)
    - @agent-forge-copilot/cli via npm (optional)
    - specify-cli via pipx
    """
    typer.secho("Checking prerequisites...", fg=typer.colors.CYAN)
    ensure_node_npm()
    ensure_pipx()

    if copilot is None:
        copilot = typer.confirm("Would you like to install the GitHub Copilot CLI and Agent Forge globally via npm?", default=True)

    if copilot:
        agent_forge.install()
    else:
        typer.secho("Skipping GitHub Copilot CLI and Agent Forge installation.", fg=typer.colors.YELLOW)

    speckit.install()

    typer.secho("Setup complete! Dependencies are installed.", fg=typer.colors.GREEN, bold=True)
