import typer
import subprocess
import sys
from pathlib import Path
from origin_cli.utils import run_command
from origin_cli.constants import FLEET_DELEGATION_PROMPT, JIRA_PRESET_PROMPT, GIT_PRESET_PROMPT, JENKINS_PRESET_PROMPT

def install():
    """Install specify-cli globally via uv."""
    typer.echo("Installing specify-cli globally via uv...")
    try:
        subprocess.run(["uv", "--version"], check=True, stdout=subprocess.DEVNULL)
        run_command(["uv", "tool", "install", "specify-cli"])
    except FileNotFoundError:
        typer.secho("uv is not installed. Falling back to pip for specify-cli...", fg=typer.colors.YELLOW)
        run_command([sys.executable, "-m", "pip", "install", "specify-cli"])

def init():
    """Run specify init."""
    typer.echo("Running 'specify init . --integration copilot'...")
    run_command(["specify", "init", ".", "--integration", "copilot"])

def override_speckit_tasks():
    """Override the default speckit.tasks command to enforce Agent Forge fleet delegation."""
    typer.echo("Creating template override for /speckit.tasks to enforce fleet delegation...")
    overrides_dir = Path(".specify/templates/overrides/commands")
    overrides_dir.mkdir(parents=True, exist_ok=True)
    tasks_override_file = overrides_dir / "speckit.tasks.prompt.md"
    tasks_override_file.write_text(FLEET_DELEGATION_PROMPT)

def apply_preset(presets_str: str):
    """Apply specialized integration presets like Jira, Git, or Jenkins (comma or space separated)."""
    # Split by comma or space and filter out empty strings
    import re
    presets = [p.strip().lower() for p in re.split(r'[,\s]+', presets_str) if p.strip()]
    
    commands_dir = Path(".specify/templates/commands")
    commands_dir.mkdir(parents=True, exist_ok=True)
    
    for preset in presets:
        if preset == "jira":
            typer.echo("Applying 'jira' preset: Injecting /speckit.epic-to-jira command template...")
            prompt_file = commands_dir / "speckit.epic-to-jira.prompt.md"
            prompt_file.write_text(JIRA_PRESET_PROMPT)
        elif preset == "git":
            typer.echo("Applying 'git' preset: Injecting /speckit.git-review command template...")
            prompt_file = commands_dir / "speckit.git-review.prompt.md"
            prompt_file.write_text(GIT_PRESET_PROMPT)
        elif preset == "jenkins":
            typer.echo("Applying 'jenkins' preset: Injecting /speckit.jenkins-deploy command template...")
            prompt_file = commands_dir / "speckit.jenkins-deploy.prompt.md"
            prompt_file.write_text(JENKINS_PRESET_PROMPT)
        else:
            typer.secho(f"Warning: Preset '{preset}' is not recognized.", fg=typer.colors.YELLOW)
