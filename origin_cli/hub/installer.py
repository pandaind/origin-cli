import json
import shutil
import tarfile
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, List, Optional

INSTALL_MANIFEST = Path(".origin") / "installed.json"


class InstallerError(Exception):
    pass


def get_base_dest_dir(rel_path: Path, target_ide: str, is_global: bool, target_project_dir: Path) -> Optional[Path]:
    home = Path.home()
    if target_ide == "vscode": target_ide = "copilot"
    
    parts = rel_path.parts
    top_dir = parts[0] if len(parts) > 1 else None
    
    # Define the local directory prefix for the IDE
    ide_prefix = ".github" if target_ide == "copilot" else f".{target_ide}"
    
    # 1. Path-based routing for structured packages
    if top_dir == "agents":
        if target_ide == "copilot": return home / ".copilot" / "agents" if is_global else target_project_dir / ide_prefix / "agents"
        elif target_ide == "cursor": return target_project_dir / ide_prefix / "rules"
        else: return home / ide_prefix / "agents" if is_global else target_project_dir / ide_prefix / "agents"
            
    elif top_dir == "instructions":
        if target_ide == "copilot": return home / ".copilot" / "instructions" if is_global else target_project_dir / ide_prefix / "instructions"
        else: return home / ide_prefix / "rules" if is_global else target_project_dir / ide_prefix / "rules"
            
    elif top_dir == "skills":
        if target_ide == "copilot": return home / ".copilot" / "skills" if is_global else target_project_dir / ide_prefix / "skills"
        else: return home / ide_prefix / "skills" if is_global else target_project_dir / ide_prefix / "skills"
            
    elif top_dir == "prompts":
        if target_ide == "copilot": return target_project_dir / ide_prefix / "prompts"
        else: return home / ide_prefix / "commands" if is_global else target_project_dir / ide_prefix / "commands"

    elif top_dir == "workflows":
        return target_project_dir / ide_prefix / "workflows"

    # 2. Extension-based fallback for flat files
    filename = rel_path.name
    ext = Path(filename).suffixes
    full_ext = "".join(ext).lower()
    
    if full_ext.endswith(".agent.md"):
        if target_ide == "copilot": return home / ".copilot" / "agents" if is_global else target_project_dir / ide_prefix / "agents"
        elif target_ide == "cursor": return target_project_dir / ide_prefix / "rules"
        else: return home / ide_prefix / "agents" if is_global else target_project_dir / ide_prefix / "agents"
            
    elif full_ext.endswith(".instructions.md") or full_ext.endswith(".rule.md"):
        if target_ide == "copilot": return home / ".copilot" / "instructions" if is_global else target_project_dir / ide_prefix / "instructions"
        else: return home / ide_prefix / "rules" if is_global else target_project_dir / ide_prefix / "rules"
            
    elif filename == "SKILL.md" or full_ext.endswith(".skill.md"):
        if target_ide == "copilot": return home / ".copilot" / "skills" if is_global else target_project_dir / ide_prefix / "skills"
        else: return home / ide_prefix / "skills" if is_global else target_project_dir / ide_prefix / "skills"
            
    elif full_ext.endswith(".prompt.md") or full_ext.endswith(".command.md"):
        if target_ide == "copilot": return target_project_dir / ide_prefix / "prompts"
        else: return home / ide_prefix / "commands" if is_global else target_project_dir / ide_prefix / "commands"
            
    return target_project_dir / ".origin" / "misc"


def install_asset_bundle(bundle_bytes: bytes, target_project_dir: Optional[Path] = None, is_global: bool = False) -> tuple[str, str]:
    """
    Extracts an .originpkg bundle from bytes in memory, reads its manifest, 
    and copies it to the appropriate local paths.
    """
    target_project_dir = target_project_dir or Path.cwd()

    with TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        bundle_path = tmp_path / "bundle.originpkg"
        bundle_path.write_bytes(bundle_bytes)

        # Extract
        try:
            with tarfile.open(bundle_path, "r:gz") as tar:
                tar.extractall(path=tmp_path)
        except tarfile.TarError as e:
            raise InstallerError(f"Invalid or corrupted bundle: {e}")

        # Read manifest
        manifest_path = tmp_path / "hub-manifest.json"
        if not manifest_path.exists():
            raise InstallerError("Downloaded bundle is missing hub-manifest.json")
        
        manifest = json.loads(manifest_path.read_text())
        asset_type = manifest.get("type")
        files = manifest.get("files", [])
        name = manifest.get("name")

        if not asset_type:
            raise InstallerError("Manifest missing 'type'")

        # Load configured IDE
        target_ide = "copilot"
        config_file = target_project_dir / ".origin" / "config.json"
        if config_file.exists():
            try:
                config = json.loads(config_file.read_text())
                target_ide = config.get("ide", "copilot")
            except json.JSONDecodeError:
                pass

        if asset_type == "extension":
            dest_dir = target_project_dir / ".origin" / "extensions" / name
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            shutil.copytree(tmp_path, dest_dir, dirs_exist_ok=True)
            return asset_type, str(dest_dir)
            
        else:
            # Universal path-based routing
            installed_paths = set()
            for f in files:
                rel_path = Path(f)
                src_file = tmp_path / rel_path
                if not src_file.is_file(): 
                    continue
                
                base_dest_dir = get_base_dest_dir(rel_path, target_ide, is_global, target_project_dir)
                if not base_dest_dir:
                    continue
                
                # Strip the standard top-level directory (e.g. 'skills') and append the rest
                if len(rel_path.parts) > 1 and rel_path.parts[0] in ["agents", "skills", "instructions", "prompts", "workflows"]:
                    sub_path = Path(*rel_path.parts[1:])
                else:
                    sub_path = rel_path
                    
                final_dest = base_dest_dir / sub_path
                final_dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, final_dest)
                installed_paths.add(str(base_dest_dir))
            
            return asset_type, ", ".join(installed_paths) if installed_paths else str(target_project_dir)


def record_install(name: str, version: str, asset_type: str, install_path: str, project_dir: Optional[Path] = None) -> None:
    """Record a successful asset installation to .origin/installed.json."""
    manifest_path = (project_dir or Path.cwd()) / INSTALL_MANIFEST
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    
    data: Dict[str, dict] = {}
    if manifest_path.exists():
        try:
            data = json.loads(manifest_path.read_text())
        except Exception:
            pass
    
    data[name] = {
        "version": version,
        "type": asset_type,
        "install_path": install_path,
        "installed_at": datetime.utcnow().isoformat(),
    }
    manifest_path.write_text(json.dumps(data, indent=2))


def get_installed_assets(project_dir: Optional[Path] = None) -> Dict[str, dict]:
    """Read the local installed.json manifest. Returns an empty dict if not found."""
    manifest_path = (project_dir or Path.cwd()) / INSTALL_MANIFEST
    if not manifest_path.exists():
        return {}
    try:
        return json.loads(manifest_path.read_text())
    except Exception:
        return {}

