import yaml
import typer
import shutil
from pathlib import Path
from origin_cli.installer.speckit_wrapper import SpecKitWrapper

class PresetRemover:
    def remove(self, name: str) -> None:
        typer.secho(f"Removing Origin Preset: {name}...", fg=typer.colors.CYAN)
        
        registry_path = Path.cwd() / ".origin" / "presets.yaml"
        if not registry_path.exists():
            typer.secho("Preset registry not found. Nothing to remove.", fg=typer.colors.YELLOW)
            raise typer.Exit(code=1)
            
        with open(registry_path, "r") as f:
            data = yaml.safe_load(f) or {}
            
        presets = data.get("presets", [])
        preset_entry = next((e for e in presets if e.get("name") == name), None)
        
        if not preset_entry:
            typer.secho(f"Preset '{name}' not found in registry.", fg=typer.colors.YELLOW)
            raise typer.Exit(code=1)
            
        # 1. Spec Kit wrapper
        speckit_name = preset_entry.get("speckit_preset_name")
        if speckit_name:
            typer.secho(f"Delegating to Spec Kit to remove preset '{speckit_name}'...", fg=typer.colors.CYAN)
            if not SpecKitWrapper.preset_remove(speckit_name):
                typer.secho("Failed to remove Spec Kit preset. Aborting.", fg=typer.colors.RED)
                raise typer.Exit(code=1)
                
        # 2. Update Registry
        data["presets"] = [e for e in presets if e.get("name") != name]
        with open(registry_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            
        # 3. Delete cached preset folder
        managed_dir = Path.cwd() / ".origin" / "presets" / name
        if managed_dir.exists():
            shutil.rmtree(managed_dir)
            typer.echo(f"Removed cached directory: {managed_dir}")
            
        typer.secho(f"\n✔ Successfully removed Origin Preset: {name}", fg=typer.colors.GREEN, bold=True)
