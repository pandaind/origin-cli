import json
import shutil
import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional


class InstallerError(Exception):
    pass


def install_asset_bundle(bundle_bytes: bytes, target_project_dir: Optional[Path] = None) -> None:
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

        # Route to appropriate locations
        if asset_type in ("skill", "agent"):
            # Global vs local preference? For now, install locally to .github/prompts/
            dest_dir = target_project_dir / ".github" / "prompts"
            _copy_files(tmp_path, dest_dir, files)
            
        elif asset_type == "instruction":
            dest_dir = target_project_dir / ".github" / "instructions"
            _copy_files(tmp_path, dest_dir, files)
            
        elif asset_type == "workflow":
            dest_dir = target_project_dir / ".specify" / "templates"
            _copy_files(tmp_path, dest_dir, files)
            
        elif asset_type == "extension":
            dest_dir = target_project_dir / ".origin" / "extensions" / name
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            shutil.copytree(tmp_path, dest_dir, dirs_exist_ok=True)
            
        else:
            raise InstallerError(f"Unknown asset type '{asset_type}'. Please update origin-cli.")


def _copy_files(src_dir: Path, dest_dir: Path, files: list[str]) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    for f in files:
        src_file = src_dir / f
        if src_file.exists():
            if src_file.is_dir():
                shutil.copytree(src_file, dest_dir / f, dirs_exist_ok=True)
            else:
                shutil.copy2(src_file, dest_dir / f)
