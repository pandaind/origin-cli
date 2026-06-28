import yaml
import typer
import shutil
from pathlib import Path
from origin_cli.installer.speckit_wrapper import SpecKitWrapper
from origin_cli.installer.file_utils import remove_json_keys

class ExtensionRemover:
    def remove(self, name: str) -> None:
        typer.secho(f"Removing Origin Extension: {name}...", fg=typer.colors.CYAN)
        
        registry_path = Path.cwd() / ".origin" / "extensions.yaml"
        if not registry_path.exists():
            typer.secho("Extension registry not found. Nothing to remove.", fg=typer.colors.YELLOW)
            raise typer.Exit(code=1)
            
        with open(registry_path, "r") as f:
            data = yaml.safe_load(f) or {}
            
        extensions = data.get("extensions", [])
        ext_entry = next((e for e in extensions if e.get("name") == name), None)
        
        if not ext_entry:
            typer.secho(f"Extension '{name}' not found in registry.", fg=typer.colors.YELLOW)
            raise typer.Exit(code=1)
            
        # 1. Spec Kit wrapper
        speckit_name = ext_entry.get("speckit_extension_name")
        if speckit_name:
            typer.secho(f"Delegating to Spec Kit to remove extension '{speckit_name}'...", fg=typer.colors.CYAN)
            if not SpecKitWrapper.remove(speckit_name):
                typer.secho("Failed to remove Spec Kit extension. Aborting.", fg=typer.colors.RED)
                raise typer.Exit(code=1)
                
        # 2. Remove Github Assets
        github_assets = ext_entry.get("github_assets", [])
        for asset in github_assets:
            p = Path(asset)
            if p.exists() and p.is_file():
                p.unlink()
                typer.echo(f"Removed {p}")
                
        # 3. Remove MCP Entries
        mcp_servers = ext_entry.get("mcp_servers", [])
        if mcp_servers:
            mcp_path = Path.cwd() / ".vscode" / "mcp.json"
            removed_keys, errors = remove_json_keys(mcp_path, mcp_servers)
            for k in removed_keys:
                typer.echo(f"Removed MCP server: {k}")
            for err in errors:
                typer.secho(f"Error removing MCP server: {err}", fg=typer.colors.RED)
                
        # 4. Update Registry
        data["extensions"] = [e for e in extensions if e.get("name") != name]
        with open(registry_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            
        # 5. Delete cached extension folder
        managed_dir = Path.cwd() / ".origin" / "extensions" / name
        if managed_dir.exists():
            shutil.rmtree(managed_dir)
            typer.echo(f"Removed cached directory: {managed_dir}")
            
        typer.secho(f"\nSuccessfully removed Origin Extension: {name}", fg=typer.colors.GREEN, bold=True)
