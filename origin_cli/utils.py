import subprocess
import sys
import typer
import shutil

def run_command(cmd: list[str], shell: bool = False, check: bool = True):
    """Helper to run a subprocess command and stream output."""
    exe = shutil.which(cmd[0])
    if exe:
        cmd = [exe] + cmd[1:]
        
    try:
        subprocess.run(cmd, shell=shell, check=check)
    except subprocess.CalledProcessError as e:
        typer.secho(f"Command failed (exit code {e.returncode}): {' '.join(cmd) if isinstance(cmd, list) else cmd}", fg=typer.colors.RED)
        sys.exit(e.returncode)
    except FileNotFoundError as e:
        typer.secho(f"Command not found: {cmd[0] if isinstance(cmd, list) else cmd}. Please ensure it is installed.", fg=typer.colors.RED)
        sys.exit(1)
