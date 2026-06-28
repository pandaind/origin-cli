import subprocess
import typer
from pathlib import Path
from typing import List

class SpecKitWrapper:
    """
    Native wrapper for 'specify' CLI commands.
    Origin delegates all Spec Kit lifecycle operations here.
    Covers both 'extension' and 'preset' subcommands.
    """
    
    @staticmethod
    def _run_cmd(args: List[str]) -> bool:
        """Run a specify command silently, printing errors on failure."""
        try:
            subprocess.run(args, check=True, capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError as e:
            typer.secho(f"\nSpec Kit error:\n{e.stderr or e.stdout}", fg=typer.colors.RED)
            return False
        except FileNotFoundError:
            typer.secho(
                "\nError: 'specify' command not found. Ensure Spec Kit is installed.",
                fg=typer.colors.RED
            )
            return False

    @staticmethod
    def _run_passthrough(args: List[str]) -> bool:
        """Run a specify command inheriting stdout/stderr (for info/list display)."""
        try:
            subprocess.run(args, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
        except FileNotFoundError:
            typer.secho(
                "\nError: 'specify' command not found. Ensure Spec Kit is installed.",
                fg=typer.colors.RED
            )
            return False

    # --- Extension Methods ---

    @staticmethod
    def add(path: Path) -> bool:
        return SpecKitWrapper._run_cmd(["specify", "extension", "add", str(path)])

    @staticmethod
    def remove(name: str) -> bool:
        return SpecKitWrapper._run_cmd(["specify", "extension", "remove", name])

    @staticmethod
    def enable(name: str) -> bool:
        return SpecKitWrapper._run_cmd(["specify", "extension", "enable", name])

    @staticmethod
    def disable(name: str) -> bool:
        return SpecKitWrapper._run_cmd(["specify", "extension", "disable", name])

    @staticmethod
    def info(name: str) -> bool:
        return SpecKitWrapper._run_passthrough(["specify", "extension", "info", name])

    @staticmethod
    def list() -> bool:
        return SpecKitWrapper._run_passthrough(["specify", "extension", "list"])

    # --- Preset Methods ---

    @staticmethod
    def preset_add(path: Path) -> bool:
        return SpecKitWrapper._run_cmd(["specify", "preset", "add", str(path)])

    @staticmethod
    def preset_remove(name: str) -> bool:
        return SpecKitWrapper._run_cmd(["specify", "preset", "remove", name])

    @staticmethod
    def preset_enable(name: str) -> bool:
        return SpecKitWrapper._run_cmd(["specify", "preset", "enable", name])

    @staticmethod
    def preset_disable(name: str) -> bool:
        return SpecKitWrapper._run_cmd(["specify", "preset", "disable", name])

    @staticmethod
    def preset_info(name: str) -> bool:
        return SpecKitWrapper._run_passthrough(["specify", "preset", "info", name])

    @staticmethod
    def preset_list() -> bool:
        return SpecKitWrapper._run_passthrough(["specify", "preset", "list"])
