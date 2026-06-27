import typer
from pathlib import Path
from origin_cli.integrations import agent_forge, speckit

def init_command(
    ide: bool = typer.Option(False, "--ide", "-i", help="IDE-only mode: do not run agent-forge init, use local Prompts"),
    preset: str = typer.Option(None, "--preset", "-p", help="Apply integration presets (comma or space separated, e.g., 'jira,git,jenkins')")
):
    """
    Initializes a project with Agent Forge and Spec Kit workflows.
    """
    typer.secho("Initializing Origin CLI Project...", fg=typer.colors.CYAN)
    
    if ide:
        typer.secho("Initializing IDE-only local files...", fg=typer.colors.CYAN)
        agent_forge.init_ide()
    else:
        agent_forge.init()
        
    speckit.init()
    speckit.override_speckit_tasks()
    
    if preset:
        speckit.apply_preset(preset)
        
    typer.secho("Project initialization complete!", fg=typer.colors.GREEN, bold=True)
