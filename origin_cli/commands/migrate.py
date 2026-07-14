import json
import shutil
import typer
from pathlib import Path
from origin_cli.commands.init import TargetIDE

def get_ide_paths(ide: TargetIDE):
    """Returns a dictionary mapping conceptual directories to their IDE-specific local paths."""
    if ide in (TargetIDE.copilot, TargetIDE.vscode):
        return {
            "prompts": Path(".github/prompts"),
            "agents": Path(".github/agents"),
            "copilot": Path(".github/copilot")
        }
    elif ide == TargetIDE.claude:
        return {
            "prompts": Path(".claude/prompts"),
            "agents": Path(".claude/agents")
        }
    elif ide == TargetIDE.cursor:
        return {
            "prompts": Path(".cursor/prompts"),
            "agents": Path(".cursor/rules")
        }
    return {}

def migrate_command(
    from_ide: TargetIDE = typer.Option(..., "--from", help="Source IDE to migrate from"),
    to_ide: TargetIDE = typer.Option(..., "--to", help="Target IDE to migrate to"),
    copy_only: bool = typer.Option(False, "--copy", help="Copy files instead of moving them")
):
    """
    Migrates local project folder structure from one IDE to another seamlessly.
    """
    if from_ide == to_ide:
        typer.secho("Source and target IDE are the same. Nothing to migrate.", fg=typer.colors.YELLOW)
        raise typer.Exit()

    typer.secho(f"Migrating project structure from {from_ide.value} to {to_ide.value}...", fg=typer.colors.CYAN)

    source_paths = get_ide_paths(from_ide)
    target_paths = get_ide_paths(to_ide)

    migrated_items = 0

    for concept, src_path in source_paths.items():
        if concept in target_paths and src_path.exists():
            dest_path = target_paths[concept]
            
            # Ensure destination parent exists
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            if dest_path.exists():
                typer.secho(f"Warning: Destination {dest_path} already exists. Merging contents...", fg=typer.colors.YELLOW)
                # Merge contents manually
                if src_path.is_dir():
                    for item in src_path.iterdir():
                        d_item = dest_path / item.name
                        if not d_item.exists():
                            if copy_only:
                                if item.is_dir():
                                    shutil.copytree(item, d_item)
                                else:
                                    shutil.copy2(item, d_item)
                            else:
                                shutil.move(str(item), str(d_item))
                            migrated_items += 1
                
                # If moving and directory is empty after merge, remove it
                if not copy_only and src_path.is_dir() and not any(src_path.iterdir()):
                    src_path.rmdir()
            else:
                if copy_only:
                    if src_path.is_dir():
                        shutil.copytree(src_path, dest_path)
                    else:
                        shutil.copy2(src_path, dest_path)
                else:
                    shutil.move(str(src_path), str(dest_path))
                
                action = "Copied" if copy_only else "Moved"
                typer.secho(f"{action} {src_path} -> {dest_path}", fg=typer.colors.GREEN)
                migrated_items += 1

    # Update .origin/config.json if it exists
    config_file = Path.cwd() / ".origin" / "config.json"
    if config_file.exists():
        try:
            config = json.loads(config_file.read_text())
            config["ide"] = to_ide.value
            config_file.write_text(json.dumps(config, indent=2))
            typer.secho(f"Updated .origin/config.json with target IDE: {to_ide.value}", fg=typer.colors.CYAN)
        except json.JSONDecodeError:
            pass

    if migrated_items > 0:
        typer.secho("Migration completed successfully!", fg=typer.colors.GREEN, bold=True)
    else:
        typer.secho(f"No corresponding {from_ide.value} folders found to migrate.", fg=typer.colors.YELLOW)
