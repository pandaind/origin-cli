import typer
from pathlib import Path
from origin_cli.utils import run_command
from origin_cli.constants import FLEET_DELEGATION_PROMPT, IMPLEMENT_OVERRIDE_PROMPT, JIRA_EXTENSION_PROMPT

def install():
    """Install specify-cli via pipx."""
    typer.echo("Installing specify-cli via pipx...")
    run_command(["pipx", "install", "specify-cli"])

def init():
    """Run specify init."""
    typer.echo("Running 'specify init . --integration copilot'...")
    run_command(["specify", "init", ".", "--integration", "copilot"])

def inject_core_overrides():
    """Override the default speckit commands to enforce Agent Forge fleet delegation and MCP awareness."""
    typer.echo("Creating template overrides for /speckit.tasks and /speckit.implement...")
    overrides_dir = Path(".specify/templates/overrides/commands")
    overrides_dir.mkdir(parents=True, exist_ok=True)
    
    tasks_override_file = overrides_dir / "speckit.tasks.prompt.md"
    tasks_override_file.write_text(FLEET_DELEGATION_PROMPT)
    
    implement_override_file = overrides_dir / "speckit.implement.prompt.md"
    implement_override_file.write_text(IMPLEMENT_OVERRIDE_PROMPT)

def apply_extensions(extensions_str: str):
    """Apply specialized integration extensions like Jira."""
    import re
    extensions = [e.strip().lower() for e in re.split(r'[,\s]+', extensions_str) if e.strip()]
    
    agents_override_dir = Path(".specify/templates/overrides/agents")
    agents_override_dir.mkdir(parents=True, exist_ok=True)
    
    for ext in extensions:
        if ext == "jira":
            typer.echo("Applying 'jira' extension: Overriding /speckit.taskstoissues agent...")
            prompt_file = agents_override_dir / "speckit.taskstoissues.agent.md"
            prompt_file.write_text(JIRA_EXTENSION_PROMPT)
        else:
            typer.secho(f"Warning: Extension '{ext}' is not recognized.", fg=typer.colors.YELLOW)
