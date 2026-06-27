import typer
from origin_cli.integrations import agent_forge, speckit

def setup_command():
    """
    Checks for and installs underlying CLI dependencies:
    - @agent-forge-copilot/cli via npm
    - specify-cli via uv
    """
    typer.secho("Setting up dependencies...", fg=typer.colors.CYAN)
    
    agent_forge.install()
    speckit.install()
    
    typer.secho("Setup complete! Dependencies are installed.", fg=typer.colors.GREEN, bold=True)
