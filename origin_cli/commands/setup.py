import typer
from origin_cli.integrations import agent_forge, speckit

def setup_command(
    copilot: bool = typer.Option(None, "--copilot/--no-copilot", help="Install GitHub Copilot CLI and Agent Forge globally via npm")
):
    """
    Checks for and installs underlying CLI dependencies:
    - @agent-forge-copilot/cli via npm (optional)
    - specify-cli via uv
    """
    typer.secho("Setting up dependencies...", fg=typer.colors.CYAN)
    
    if copilot is None:
        copilot = typer.confirm("Would you like to install the GitHub Copilot CLI and Agent Forge globally via npm?", default=True)
        
    if copilot:
        agent_forge.install()
    else:
        typer.secho("Skipping GitHub Copilot CLI and Agent Forge installation.", fg=typer.colors.YELLOW)
        
    speckit.install()
    
    typer.secho("Setup complete! Dependencies are installed.", fg=typer.colors.GREEN, bold=True)
