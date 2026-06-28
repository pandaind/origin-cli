from pathlib import Path
import yaml
import datetime
from typing import Dict, Any, List, Optional

from origin_cli.installer.base import AbstractInstaller
from origin_cli.installer.models import InstallContext, InstallResult


class ExtensionRegistry:
    """
    Maintains .origin/extensions.yaml, tracking all Origin-managed extension metadata.
    """

    def install(
        self,
        context: InstallContext,
        github_assets: List[str] = None,
        mcp_servers: List[str] = None,
        speckit_extension_name: Optional[str] = None,
    ) -> InstallResult:
        registry_path = Path.cwd() / ".origin" / "extensions.yaml"
        added: List[str] = []
        replaced: List[str] = []
        errors: List[str] = []

        if not context.dry_run:
            registry_path.parent.mkdir(parents=True, exist_ok=True)

            data: Dict[str, Any] = {"extensions": []}
            if registry_path.exists():
                try:
                    with open(registry_path, "r") as f:
                        loaded = yaml.safe_load(f)
                        if loaded and "extensions" in loaded:
                            data = loaded
                except Exception as e:
                    errors.append(f"Failed to read registry: {e}")
                    return InstallResult(installer_name="Extension Registry", errors=errors)

            extensions: List[Dict[str, Any]] = data.get("extensions", [])

            existing = next((ext for ext in extensions if ext.get("name") == context.extension_name), None)

            ext_entry: Dict[str, Any] = {
                "name": context.extension_name,
                "version": context.manifest.get("version", "unknown"),
                "install_date": datetime.datetime.now().isoformat(),
                "enabled": True,
                "speckit_extension_name": speckit_extension_name,
                "github_assets": github_assets or [],
                "mcp_servers": mcp_servers or [],
            }

            if existing:
                existing.update(ext_entry)
                replaced.append(str(registry_path))
            else:
                extensions.append(ext_entry)
                added.append(str(registry_path))

            data["extensions"] = extensions

            try:
                with open(registry_path, "w") as f:
                    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            except Exception as e:
                errors.append(f"Failed to write registry: {e}")
        else:
            added.append(str(registry_path))

        return InstallResult(
            installer_name="Extension Registry",
            added=added,
            replaced=replaced,
            errors=errors,
        )
