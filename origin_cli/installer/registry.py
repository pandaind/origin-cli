from pathlib import Path
import yaml
import datetime
from typing import Dict, Any, List
from origin_cli.installer.base import AbstractInstaller
from origin_cli.installer.models import InstallContext, InstallResult

class ExtensionRegistry(AbstractInstaller):
    def install(self, context: InstallContext) -> InstallResult:
        registry_path = Path.cwd() / ".origin" / "extensions.yaml"
        added = []
        replaced = []
        errors = []

        if not context.dry_run:
            registry_path.parent.mkdir(parents=True, exist_ok=True)
            
            data = {"extensions": []}
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
            
            ext_entry = {
                "name": context.extension_name,
                "version": context.manifest.get("version", "unknown"),
                "install_date": datetime.datetime.now().isoformat(),
                "enabled": True,
                "speckit_extension_name": context.manifest.get("_speckit_extension_name"),
                "github_assets": context.manifest.get("_github_assets", []),
                "mcp_servers": context.manifest.get("_mcp_servers", [])
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
            errors=errors
        )
