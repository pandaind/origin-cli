import shutil
import json
from pathlib import Path
from typing import Dict, Any, Tuple, List

def copy_directory(src: Path, dest: Path, force: bool = False, dry_run: bool = False) -> Tuple[List[str], List[str], List[str], List[str]]:
    """
    Recursively copies files from src to dest.
    Returns lists of (added, replaced, skipped, errors) paths.
    """
    added = []
    replaced = []
    skipped = []
    errors = []

    if not src.exists() or not src.is_dir():
        return added, replaced, skipped, errors

    for item in src.rglob("*"):
        if item.is_dir():
            continue
            
        rel_path = item.relative_to(src)
        dest_path = dest / rel_path

        if dest_path.exists():
            if not force:
                skipped.append(str(dest_path))
                continue
            replaced.append(str(dest_path))
        else:
            added.append(str(dest_path))

        if not dry_run:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(item, dest_path)
            except Exception as e:
                errors.append(f"Failed to copy {item} to {dest_path}: {e}")

    return added, replaced, skipped, errors

def merge_json(src_json_path: Path, dest_json_path: Path, force: bool = False, dry_run: bool = False) -> Tuple[List[str], List[str], List[str], List[str]]:
    """
    Merges src JSON into dest JSON. Focuses primarily on "mcpServers" key.
    """
    added = []
    replaced = []
    skipped = []
    errors = []

    if not src_json_path.exists():
        return added, replaced, skipped, errors

    try:
        with open(src_json_path, 'r') as f:
            src_data = json.load(f)
    except Exception as e:
        errors.append(f"Invalid JSON in {src_json_path}: {e}")
        return added, replaced, skipped, errors

    if not dest_json_path.exists():
        if not dry_run:
            dest_json_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dest_json_path, 'w') as f:
                json.dump(src_data, f, indent=2)
        added.append(str(dest_json_path))
        return added, replaced, skipped, errors

    try:
        with open(dest_json_path, 'r') as f:
            dest_data = json.load(f)
    except Exception as e:
        errors.append(f"Invalid JSON in target {dest_json_path}: {e}")
        return added, replaced, skipped, errors

    # Merge mcpServers specifically
    modified = False
    if "mcpServers" in src_data:
        if "mcpServers" not in dest_data:
            dest_data["mcpServers"] = {}
        
        for server_name, server_config in src_data["mcpServers"].items():
            if server_name in dest_data["mcpServers"]:
                if not force:
                    skipped.append(f"mcpServers.{server_name} in {dest_json_path}")
                    continue
                replaced.append(f"mcpServers.{server_name} in {dest_json_path}")
            else:
                added.append(f"mcpServers.{server_name} in {dest_json_path}")
            
            dest_data["mcpServers"][server_name] = server_config
            modified = True

    if modified and not dry_run:
        with open(dest_json_path, 'w') as f:
            json.dump(dest_data, f, indent=2)

    return added, replaced, skipped, errors

def remove_json_keys(dest_json_path: Path, server_names: List[str], dry_run: bool = False) -> Tuple[List[str], List[str]]:
    """
    Removes specific mcpServers keys from a JSON file.
    Returns (removed_keys, errors).
    """
    removed = []
    errors = []
    
    if not dest_json_path.exists():
        return removed, errors
        
    try:
        with open(dest_json_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        errors.append(f"Invalid JSON in {dest_json_path}: {e}")
        return removed, errors
        
    if "mcpServers" not in data:
        return removed, errors
        
    modified = False
    for name in server_names:
        if name in data["mcpServers"]:
            del data["mcpServers"][name]
            removed.append(name)
            modified = True
            
    if modified and not dry_run:
        try:
            with open(dest_json_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            errors.append(f"Failed to write to {dest_json_path}: {e}")
            
    return removed, errors
