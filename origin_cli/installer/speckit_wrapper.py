import subprocess
import typer
from pathlib import Path

class SpecKitWrapper:
    """
    Wrapper for 'specify extension' native commands.
    Origin delegates all spec-kit specific logic here.
    """
    
    @staticmethod
    def _run_cmd(args: list[str]) -> bool:
        try:
            result = subprocess.run(
                args,
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError as e:
            typer.secho(f"\nSpec Kit error:\n{e.stderr or e.stdout}", fg=typer.colors.RED)
            return False
        except FileNotFoundError:
            typer.secho("\nError: 'specify' command not found. Ensure Spec Kit is installed.", fg=typer.colors.RED)
            return False

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
        # Note: Origin info command will likely call this just to print to stdout.
        # However, to be consistent, we might just want to use subprocess.call directly for info/list to inherit stdout.
        try:
            subprocess.run(["specify", "extension", "info", name], check=True)
            return True
        except Exception:
            return False
            
    @staticmethod
    def list() -> bool:
        try:
            subprocess.run(["specify", "extension", "list"], check=True)
            return True
        except Exception:
            return False

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
        try:
            subprocess.run(["specify", "preset", "info", name], check=True)
            return True
        except Exception:
            return False
            
    @staticmethod
    def preset_list() -> bool:
        try:
            subprocess.run(["specify", "preset", "list"], check=True)
            return True
        except Exception:
            return False
