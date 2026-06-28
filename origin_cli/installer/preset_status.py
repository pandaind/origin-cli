import yaml
import typer
from pathlib import Path
from origin_cli.installer.speckit_wrapper import SpecKitWrapper

class PresetStatusManager:
    @staticmethod
    def _update_enabled(name: str, enabled: bool) -> None:
        registry_path = Path.cwd() / ".origin" / "presets.yaml"
        if not registry_path.exists():
            typer.secho("Preset registry not found.", fg=typer.colors.YELLOW)
            raise typer.Exit(code=1)
            
        with open(registry_path, "r") as f:
            data = yaml.safe_load(f) or {}
            
        presets = data.get("presets", [])
        preset_entry = next((e for e in presets if e.get("name") == name), None)
        
        if not preset_entry:
            typer.secho(f"Preset '{name}' not found in registry.", fg=typer.colors.YELLOW)
            raise typer.Exit(code=1)
            
        speckit_name = preset_entry.get("speckit_preset_name")
        
        action_word = "enable" if enabled else "disable"
        typer.secho(f"Origin attempting to {action_word} preset '{name}'...", fg=typer.colors.CYAN)
        
        if speckit_name:
            typer.secho(f"Delegating to Spec Kit to {action_word} preset '{speckit_name}'...", fg=typer.colors.CYAN)
            success = SpecKitWrapper.preset_enable(speckit_name) if enabled else SpecKitWrapper.preset_disable(speckit_name)
            if not success:
                typer.secho(f"Failed to {action_word} Spec Kit preset. Aborting.", fg=typer.colors.RED)
                raise typer.Exit(code=1)
                
        preset_entry["enabled"] = enabled
        
        with open(registry_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            
        typer.secho(f"✔ Successfully {action_word}d preset '{name}'!", fg=typer.colors.GREEN, bold=True)

    @staticmethod
    def enable(name: str) -> None:
        PresetStatusManager._update_enabled(name, True)

    @staticmethod
    def disable(name: str) -> None:
        PresetStatusManager._update_enabled(name, False)

    @staticmethod
    def list() -> None:
        typer.secho("--- Origin Managed Presets ---", bold=True, fg=typer.colors.CYAN)
        registry_path = Path.cwd() / ".origin" / "presets.yaml"
        if registry_path.exists():
            with open(registry_path, "r") as f:
                data = yaml.safe_load(f) or {}
            presets = data.get("presets", [])
            for p in presets:
                status = "🟢 Enabled" if p.get("enabled") else "🔴 Disabled"
                typer.echo(f"{p.get('name')} (v{p.get('version')}) - Priority: {p.get('priority', 0)} - {status}")
        else:
            typer.echo("No Origin presets installed.")
            
        typer.secho("\n--- Spec Kit Presets ---", bold=True, fg=typer.colors.CYAN)
        SpecKitWrapper.preset_list()

    @staticmethod
    def info(name: str) -> None:
        typer.secho(f"--- Origin Preset Info: {name} ---", bold=True, fg=typer.colors.CYAN)
        registry_path = Path.cwd() / ".origin" / "presets.yaml"
        if registry_path.exists():
            with open(registry_path, "r") as f:
                data = yaml.safe_load(f) or {}
            presets = data.get("presets", [])
            p = next((e for e in presets if e.get("name") == name), None)
            
            if p:
                typer.echo(f"Version: {p.get('version')}")
                typer.echo(f"Installed: {p.get('install_date')}")
                typer.echo(f"Status: {'Enabled' if p.get('enabled') else 'Disabled'}")
                typer.echo(f"Priority: {p.get('priority', 0)}")
                
                speckit_name = p.get("speckit_preset_name")
                if speckit_name:
                    typer.secho(f"\n--- Underlying Spec Kit Preset: {speckit_name} ---", bold=True, fg=typer.colors.CYAN)
                    SpecKitWrapper.preset_info(speckit_name)
            else:
                typer.secho(f"Preset '{name}' not found in registry.", fg=typer.colors.YELLOW)
        else:
            typer.secho("Preset registry not found.", fg=typer.colors.YELLOW)
