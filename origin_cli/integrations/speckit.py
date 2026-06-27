import typer
import subprocess
import sys
from pathlib import Path
from origin_cli.utils import run_command
from origin_cli.constants import SPECKIT_CONSTITUTION_OVERRIDE

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

def cross_wire_commands():
    """Create the Spec Kit constitution override."""
    typer.echo("Cross-wiring commands for /speckit.constitution...")
    overrides_dir = Path(".specify/templates/overrides/commands")
    overrides_dir.mkdir(parents=True, exist_ok=True)
    speckit_override_file = overrides_dir / "speckit.constitution.prompt.md"
    speckit_override_file.write_text(SPECKIT_CONSTITUTION_OVERRIDE)
