import typer
from pathlib import Path
from origin_cli.integrations import agent_forge, speckit
from origin_cli.constants import BASELINE_CONSTITUTION

def init_command(
    ide: bool = typer.Option(False, "--ide", "-i", help="IDE-only mode: do not run agent-forge init, use local Prompts")
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
    

    # Inject the Constitution
    typer.echo("Injecting baseline CONSTITUTION.md...")
    constitution_file = Path("CONSTITUTION.md")
    if not constitution_file.exists():
        constitution_file.write_text(BASELINE_CONSTITUTION)
        typer.echo("Created baseline CONSTITUTION.md")
    else:
        typer.echo("CONSTITUTION.md already exists, skipping.")
        
    typer.secho("Project initialization complete!", fg=typer.colors.GREEN, bold=True)
