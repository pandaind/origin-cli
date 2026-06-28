import yaml
import typer
from pathlib import Path
from origin_cli.installer.speckit_wrapper import SpecKitWrapper

class ExtensionStatusManager:
    @staticmethod
    def _update_enabled(name: str, enabled: bool) -> None:
        registry_path = Path.cwd() / ".origin" / "extensions.yaml"
        if not registry_path.exists():
            typer.secho("Extension registry not found.", fg=typer.colors.YELLOW)
            raise typer.Exit(code=1)
            
        with open(registry_path, "r") as f:
            data = yaml.safe_load(f) or {}
            
        extensions = data.get("extensions", [])
        ext_entry = next((e for e in extensions if e.get("name") == name), None)
        
        if not ext_entry:
            typer.secho(f"Extension '{name}' not found in registry.", fg=typer.colors.YELLOW)
            raise typer.Exit(code=1)
            
        speckit_name = ext_entry.get("speckit_extension_name")
        
        action_word = "enable" if enabled else "disable"
        typer.secho(f"Origin attempting to {action_word} extension '{name}'...", fg=typer.colors.CYAN)
        
        if speckit_name:
            typer.secho(f"Delegating to Spec Kit to {action_word} extension '{speckit_name}'...", fg=typer.colors.CYAN)
            success = SpecKitWrapper.enable(speckit_name) if enabled else SpecKitWrapper.disable(speckit_name)
            if not success:
                typer.secho(f"Failed to {action_word} Spec Kit extension. Aborting.", fg=typer.colors.RED)
                raise typer.Exit(code=1)
                
        # In a real system, you might rename files or comment out MCP entries to actually disable them.
        # For this orchestrator MVP, we just update the registry flag.
        ext_entry["enabled"] = enabled
        
        with open(registry_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            
        typer.secho(f"Successfully {action_word}d extension '{name}'!", fg=typer.colors.GREEN, bold=True)

    @staticmethod
    def enable(name: str) -> None:
        ExtensionStatusManager._update_enabled(name, True)

    @staticmethod
    def disable(name: str) -> None:
        ExtensionStatusManager._update_enabled(name, False)

    @staticmethod
    def list() -> None:
        typer.secho("--- Origin Managed Extensions ---", bold=True, fg=typer.colors.CYAN)
        registry_path = Path.cwd() / ".origin" / "extensions.yaml"
        if registry_path.exists():
            with open(registry_path, "r") as f:
                data = yaml.safe_load(f) or {}
            extensions = data.get("extensions", [])
            for ext in extensions:
                status = "🟢 Enabled" if ext.get("enabled") else "🔴 Disabled"
                typer.echo(f"{ext.get('name')} (v{ext.get('version')}) - {status}")
        else:
            typer.echo("No Origin extensions installed.")
            
        typer.secho("\n--- Spec Kit Extensions ---", bold=True, fg=typer.colors.CYAN)
        SpecKitWrapper.list()

    @staticmethod
    def info(name: str) -> None:
        typer.secho(f"--- Origin Extension Info: {name} ---", bold=True, fg=typer.colors.CYAN)
        registry_path = Path.cwd() / ".origin" / "extensions.yaml"
        if registry_path.exists():
            with open(registry_path, "r") as f:
                data = yaml.safe_load(f) or {}
            extensions = data.get("extensions", [])
            ext = next((e for e in extensions if e.get("name") == name), None)
            
            if ext:
                typer.echo(f"Version: {ext.get('version')}")
                typer.echo(f"Installed: {ext.get('install_date')}")
                typer.echo(f"Status: {'Enabled' if ext.get('enabled') else 'Disabled'}")
                typer.echo(f"GitHub Assets: {len(ext.get('github_assets', []))} files")
                typer.echo(f"MCP Servers: {', '.join(ext.get('mcp_servers', [])) or 'None'}")
                
                speckit_name = ext.get("speckit_extension_name")
                if speckit_name:
                    typer.secho(f"\n--- Underlying Spec Kit Extension: {speckit_name} ---", bold=True, fg=typer.colors.CYAN)
                    SpecKitWrapper.info(speckit_name)
            else:
                typer.secho(f"Extension '{name}' not found in registry.", fg=typer.colors.YELLOW)
        else:
            typer.secho("Extension registry not found.", fg=typer.colors.YELLOW)
