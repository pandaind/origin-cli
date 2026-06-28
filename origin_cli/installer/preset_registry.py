from pathlib import Path
import yaml
import datetime
from typing import Dict, Any, List, Optional
from origin_cli.installer.models import InstallContext, InstallResult

class PresetRegistry:
    def __init__(self):
        self.registry_path = Path.cwd() / ".origin" / "presets.yaml"

    def register(self, context: InstallContext, speckit_preset_name: str) -> InstallResult:
        added = []
        replaced = []
        errors = []

        if not context.dry_run:
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            
            data = {"presets": []}
            if self.registry_path.exists():
                try:
                    with open(self.registry_path, "r") as f:
                        loaded = yaml.safe_load(f)
                        if loaded and "presets" in loaded:
                            data = loaded
                except Exception as e:
                    errors.append(f"Failed to read preset registry: {e}")
                    return InstallResult(installer_name="Preset Registry", errors=errors)

            presets: List[Dict[str, Any]] = data.get("presets", [])
            
            existing = next((p for p in presets if p.get("name") == context.extension_name), None)
            
            preset_entry = {
                "name": context.extension_name,
                "version": context.manifest.get("version", "unknown"),
                "install_date": datetime.datetime.now().isoformat(),
                "enabled": True,
                "priority": 0,
                "speckit_preset_name": speckit_preset_name
            }
            
            if existing:
                existing.update(preset_entry)
                replaced.append(str(self.registry_path))
            else:
                presets.append(preset_entry)
                added.append(str(self.registry_path))
                
            data["presets"] = presets
            
            try:
                with open(self.registry_path, "w") as f:
                    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            except Exception as e:
                errors.append(f"Failed to write preset registry: {e}")
        else:
            added.append(str(self.registry_path))
            
        return InstallResult(
            installer_name="Preset Registry",
            added=added,
            replaced=replaced,
            errors=errors
        )
