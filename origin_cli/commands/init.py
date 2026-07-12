import json
import typer
from enum import Enum
from pathlib import Path
from origin_cli.integrations import agent_forge, speckit

class TargetIDE(str, Enum):
    copilot = "copilot"
    vscode = "vscode"  # VS Code with GitHub Copilot — uses same paths as copilot
    claude = "claude"
    cursor = "cursor"

def init_command(
    ide: TargetIDE = typer.Option(TargetIDE.copilot, "--ide", "-i", help="Target IDE for Origin CLI integration (copilot, claude, cursor)"),
    ide_only: bool = typer.Option(False, "--ide-only", help="Do not run agent-forge init, just configure the IDE."),
    extension: str = typer.Option(None, "--extension", "-e", help="Apply integration extensions (e.g., 'jira')")
):
    """
    Initializes a project with Agent Forge and Spec Kit workflows.
    """
    typer.secho("Initializing Origin CLI Project...", fg=typer.colors.CYAN)
    
    # Save configuration
    config_dir = Path.cwd() / ".origin"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "config.json"
    
    config = {}
    if config_file.exists():
        try:
            config = json.loads(config_file.read_text())
        except json.JSONDecodeError:
            pass
            
    config["ide"] = ide.value
    config_file.write_text(json.dumps(config, indent=2))
    typer.secho(f"Target IDE configured as: {ide.value}", fg=typer.colors.CYAN)
    
    COPILOT_IDES = {TargetIDE.copilot, TargetIDE.vscode}
    
    if ide_only:
        typer.secho("Initializing IDE-only local files...", fg=typer.colors.CYAN)
        agent_forge.init_ide()
    else:
        agent_forge.init()
        
    # Speckit is a GitHub Copilot-specific toolchain — only run for copilot/vscode
    if ide in COPILOT_IDES:
        speckit.init()
        speckit.inject_core_overrides()
        
        if extension:
            speckit.apply_extensions(extension)
    else:
        typer.secho(f"Skipping Speckit setup (not required for {ide.value}).", fg=typer.colors.YELLOW)
        
    typer.secho("Project initialization complete!", fg=typer.colors.GREEN, bold=True)
