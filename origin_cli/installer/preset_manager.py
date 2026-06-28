import yaml
import typer
import shutil
from pathlib import Path
from typing import Optional

from origin_cli.installer.models import InstallContext, InstallResult
from origin_cli.installer.speckit_wrapper import SpecKitWrapper
from origin_cli.installer.preset_registry import PresetRegistry

class PresetInstallationManager:
    def __init__(self):
        self.registry = PresetRegistry()

    def install_preset(self, source_path: Path, force: bool = False, dry_run: bool = False) -> None:
        typer.secho(f"Validating preset at '{source_path}'...", fg=typer.colors.CYAN)
        
        # 1. Validate
        manifest_path = source_path / "origin-preset.yaml"
        if not source_path.exists() or not source_path.is_dir():
            typer.secho(f"Error: Preset source path does not exist or is not a directory: {source_path}", fg=typer.colors.RED)
            raise typer.Exit(code=1)
            
        if not manifest_path.exists():
            typer.secho(f"Error: Missing origin-preset.yaml at {manifest_path}", fg=typer.colors.RED)
            raise typer.Exit(code=1)
            
        try:
            with open(manifest_path, "r") as f:
                manifest = yaml.safe_load(f)
        except Exception as e:
            typer.secho(f"Error parsing manifest: {e}", fg=typer.colors.RED)
            raise typer.Exit(code=1)
            
        name = manifest.get("name")
        version = manifest.get("version")
        
        if not name:
            typer.secho("Error: Preset manifest is missing 'name'", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        typer.secho(f"✔ Validated preset {name} (v{version})", fg=typer.colors.GREEN)
        
        # 2. Copy preset to managed directory
        managed_dir = Path.cwd() / ".origin" / "presets" / name
        if not dry_run:
            managed_dir.parent.mkdir(parents=True, exist_ok=True)
            if managed_dir.exists():
                shutil.rmtree(managed_dir)
            shutil.copytree(source_path, managed_dir)
            
        # Create Context
        context = InstallContext(
            extension_source_path=source_path,
            extension_name=name,
            manifest=manifest,
            force=force,
            dry_run=dry_run
        )
        if dry_run:
            context.managed_dir = source_path
            
        # 3. Spec Kit Orchestration (Wrapper)
        speckit_preset_dir = managed_dir / "speckit" / "preset"
        speckit_name = name # Default assumption
        if speckit_preset_dir.exists() and speckit_preset_dir.is_dir():
            typer.secho(f"Delegating to Spec Kit to install preset...", fg=typer.colors.CYAN)
            if not dry_run:
                # We pass the absolute path to the preset
                if not SpecKitWrapper.preset_add(speckit_preset_dir.resolve()):
                    typer.secho("Failed to install Spec Kit preset. Aborting Origin installation.", fg=typer.colors.RED)
                    # Rollback
                    if managed_dir.exists():
                        shutil.rmtree(managed_dir)
                    raise typer.Exit(code=1)
        else:
            typer.secho("Warning: No speckit/preset/ directory found in the preset.", fg=typer.colors.YELLOW)
            
        # 4. Register
        typer.secho("\nRegistering preset in Origin...", fg=typer.colors.CYAN)
        result = self.registry.register(context, speckit_name)
        if not result.is_success() and not dry_run:
            typer.secho("Failed to register preset. Initiating rollback...", fg=typer.colors.YELLOW)
            if managed_dir.exists():
                shutil.rmtree(managed_dir)
            raise typer.Exit(code=1)

        if not dry_run:
            typer.secho(f"\n✔ Successfully installed Origin Preset: {name}!", fg=typer.colors.GREEN, bold=True)
        else:
            typer.secho(f"\nDry run complete. No files were modified.", fg=typer.colors.YELLOW, bold=True)
