import yaml
from pathlib import Path
from origin_cli.generators.extension.base import AbstractGenerator
from typing import Dict, Any

class PresetManifestGenerator(AbstractGenerator):
    def generate(self, context: Dict[str, Any], output_dir: Path) -> None:
        manifest_path = output_dir / "origin-preset.yaml"
        
        manifest = {
            "name": context.get("name"),
            "version": context.get("version", "1.0.0"),
            "description": context.get("description", ""),
            "author": context.get("author", ""),
            "license": context.get("license", "MIT"),
            "speckit": {
                "preset": {
                    "commands": [
                        "specify",
                        "plan",
                        "tasks",
                        "implement",
                        "analyze",
                        "constitution"
                    ],
                    "templates": [
                        "spec",
                        "plan",
                        "tasks",
                        "checklist",
                        "constitution"
                    ],
                    "scripts": [
                        "pre-plan",
                        "post-plan",
                        "pre-implement",
                        "post-implement"
                    ]
                }
            }
        }
        
        with open(manifest_path, "w") as f:
            yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
