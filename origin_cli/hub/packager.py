import json
import tarfile
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict, Any


class PackagerError(Exception):
    pass


def create_asset_bundle(source_dir: Path) -> tuple[Path, Dict[str, Any]]:
    """
    Validates a directory and packages it into an .originpkg tar.gz archive.
    Returns a tuple of (path_to_tmp_bundle, parsed_manifest_dict).
    """
    if not source_dir.is_dir():
        raise PackagerError(f"Source directory '{source_dir}' does not exist.")

    manifest_path = source_dir / "hub-manifest.json"
    if not manifest_path.exists():
        raise PackagerError(f"No hub-manifest.json found in '{source_dir}'.")

    try:
        manifest_data = json.loads(manifest_path.read_text())
    except json.JSONDecodeError as e:
        raise PackagerError(f"Invalid JSON in hub-manifest.json: {e}")

    # Validate minimal fields
    required = ["name", "version", "type"]
    for req in required:
        if req not in manifest_data:
            raise PackagerError(f"Missing required field '{req}' in manifest.")

    # Create temporary bundle file
    tmp_file = NamedTemporaryFile(delete=False, suffix=".originpkg")
    tmp_file.close()
    
    bundle_path = Path(tmp_file.name)

    # Directories and files to exclude from the bundle
    IGNORE_NAMES = {".git", ".specify", ".origin", "__pycache__", "node_modules", ".venv"}

    # Tar and gzip the directory contents
    try:
        with tarfile.open(bundle_path, "w:gz") as tar:
            packaged_files = []
            for item in source_dir.iterdir():
                if item.name in IGNORE_NAMES or item.name == "hub-manifest.json":
                    continue
                tar.add(item, arcname=item.name)
                packaged_files.append(item.name)
            
            # Auto-populate 'files' if missing so users don't have to list them manually
            if not manifest_data.get("files"):
                manifest_data["files"] = packaged_files
                
            # Write the updated manifest directly to the tarball
            import io
            manifest_bytes = json.dumps(manifest_data, indent=2).encode("utf-8")
            tarinfo = tarfile.TarInfo(name="hub-manifest.json")
            tarinfo.size = len(manifest_bytes)
            tar.addfile(tarinfo, io.BytesIO(manifest_bytes))
            
    except Exception as e:
        if bundle_path.exists():
            bundle_path.unlink()
        raise PackagerError(f"Failed to create bundle archive: {e}")

    return bundle_path, manifest_data
