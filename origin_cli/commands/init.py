import typer
from pathlib import Path
from origin_cli.integrations import agent_forge, speckit

def init_command(
    ide: bool = typer.Option(False, "--ide", "-i", help="IDE-only mode: do not run agent-forge init, use local Prompts"),
    extension: str = typer.Option(None, "--extension", "-e", help="Apply integration extensions (e.g., 'jira')")
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
    speckit.inject_core_overrides()
    
    if extension:
        speckit.apply_extensions(extension)
        
    typer.secho("Project initialization complete!", fg=typer.colors.GREEN, bold=True)
