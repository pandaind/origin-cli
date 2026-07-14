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
    gemini = "gemini"
    codebuddy = "codebuddy"
    pi = "pi"
    omp = "omp"

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
    
    if ide == TargetIDE.copilot and not ide_only:
        typer.secho("Initializing Agent Forge via Copilot CLI...", fg=typer.colors.CYAN)
        agent_forge.init()
    else:
        typer.secho(f"Initializing IDE-native local files for {ide.value}...", fg=typer.colors.CYAN)
        agent_forge.init_ide(ide.value)
        
    if not ide_only:
        # Speckit supports various integrations
        integration = "copilot" if ide.value == "vscode" else ide.value
        speckit.init(integration)
        speckit.inject_core_overrides()
        
        if extension:
            speckit.apply_extensions(extension)
        
    typer.secho("Project initialization complete!", fg=typer.colors.GREEN, bold=True)
