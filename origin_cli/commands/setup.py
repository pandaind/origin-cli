import typer
from origin_cli.integrations import agent_forge, speckit

def setup_command(
    ide: bool = typer.Option(False, "--ide", "-i", help="IDE-only mode: do not install NPM dependencies, install global Copilot agents instead")
):
    """
    Checks for and installs underlying CLI dependencies or global agents:
    - @agent-forge-copilot/cli via npm (default)
    - specify-cli via uv (default)
    """
    if ide:
        typer.secho("Setting up IDE-only templates...", fg=typer.colors.CYAN)
        agent_forge.install_ide()
        typer.secho("Setup complete! IDE templates are installed.", fg=typer.colors.GREEN, bold=True)
    else:
        typer.secho("Setting up dependencies...", fg=typer.colors.CYAN)
        agent_forge.install()
        speckit.install()
        typer.secho("Setup complete! Dependencies are installed.", fg=typer.colors.GREEN, bold=True)
