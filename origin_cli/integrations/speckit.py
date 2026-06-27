import typer
import subprocess
import sys
from pathlib import Path
from origin_cli.utils import run_command

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
