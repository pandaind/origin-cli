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


def get_dest_dir(filename: str, target_ide: str, is_global: bool, target_project_dir: Path) -> Optional[Path]:
    ext = Path(filename).suffixes
    full_ext = "".join(ext).lower()
    
    home = Path.home()
    
    # VS Code uses GitHub Copilot which shares the same path structure
    if target_ide == "vscode":
        target_ide = "copilot"
    
    if full_ext.endswith(".agent.md"):
        if target_ide == "copilot":
            return home / ".copilot" / "agents" if is_global else target_project_dir / ".github" / "agents"
        elif target_ide == "claude":
            return home / ".claude" / "agents" if is_global else target_project_dir / ".claude" / "agents"
        elif target_ide == "cursor":
            # Fallback to rules for Cursor since agents are not officially supported
            return target_project_dir / ".cursor" / "rules"
            
    elif full_ext.endswith(".instructions.md") or full_ext.endswith(".rule.md"):
        if target_ide == "copilot":
            return home / ".copilot" / "instructions" if is_global else target_project_dir / ".github" / "instructions"
        elif target_ide == "claude":
            return home / ".claude" / "rules" if is_global else target_project_dir / ".claude" / "rules"
        elif target_ide == "cursor":
            return target_project_dir / ".cursor" / "rules"
            
    elif full_ext.endswith(".skill.md"):
        if target_ide == "copilot":
            return home / ".copilot" / "skills" if is_global else target_project_dir / ".github" / "skills"
        elif target_ide == "claude":
            return home / ".claude" / "skills" if is_global else target_project_dir / ".claude" / "skills"
        elif target_ide == "cursor":
            return target_project_dir / ".cursor" / "skills"
            
    elif full_ext.endswith(".prompt.md") or full_ext.endswith(".command.md"):
        if target_ide == "copilot":
            return target_project_dir / ".github" / "prompts"
        elif target_ide == "claude":
            return home / ".claude" / "commands" if is_global else target_project_dir / ".claude" / "commands"
        elif target_ide == "cursor":
            return home / ".cursor" / "commands" if is_global else target_project_dir / ".cursor" / "commands"
            
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

        if asset_type == "workflow":
            dest_dir = target_project_dir / ".specify" / "templates"
            _copy_files(tmp_path, dest_dir, files)
            return asset_type, str(dest_dir)
            
        elif asset_type == "extension":
            dest_dir = target_project_dir / ".origin" / "extensions" / name
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            shutil.copytree(tmp_path, dest_dir, dirs_exist_ok=True)
            return asset_type, str(dest_dir)
            
        else:
            # Per-file dynamic routing based on extensions
            installed_paths = set()
            for f in files:
                dest_dir = get_dest_dir(f, target_ide, is_global, target_project_dir)
                if dest_dir:
                    _copy_files(tmp_path, dest_dir, [f])
                    installed_paths.add(str(dest_dir))
            
            return asset_type, ", ".join(installed_paths) if installed_paths else str(target_project_dir)


def _copy_files(src_dir: Path, dest_dir: Path, files: list[str]) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    for f in files:
        src_file = src_dir / f
        if src_file.exists():
            if src_file.is_dir():
                shutil.copytree(src_file, dest_dir / f, dirs_exist_ok=True)
            else:
                shutil.copy2(src_file, dest_dir / f)


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

