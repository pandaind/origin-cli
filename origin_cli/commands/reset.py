import typer
from origin_cli.integrations import agent_forge, speckit
from origin_cli.integrations import headroom as hr
from origin_cli.integrations.prerequisites import check_command

def reset_command(
    force: bool = typer.Option(False, "--force", "-f", help="Bypass confirmation prompt"),
):
    """
    Uninstall all global AI dependencies added by `origin setup`.
    """
    if not force:
        typer.secho(
            "WARNING: This will completely uninstall the following global components:\n"
            "  - @github/copilot (npm)\n"
            "  - @agent-forge-copilot/cli (npm)\n"
            "  - specify-cli (pipx)\n"
            "  - headroom-ai (pipx)",
            fg=typer.colors.YELLOW, bold=True
        )
        typer.confirm("Are you sure you want to proceed?", abort=True)
        
    typer.secho("\nStarting global reset...", fg=typer.colors.CYAN)
    
    agent_forge.uninstall()
    
    if check_command("pipx"):
        speckit.uninstall()
        hr.uninstall()
    else:
        typer.secho("pipx not found, skipping pipx-based uninstalls (specify-cli, headroom-ai).", fg=typer.colors.YELLOW)
        
    typer.secho("\nReset complete! All global components have been removed.", fg=typer.colors.GREEN, bold=True)
