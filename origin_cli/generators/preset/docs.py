from pathlib import Path
from origin_cli.generators.extension.base import AbstractGenerator
from typing import Dict, Any

class PresetDocsGenerator(AbstractGenerator):
    def generate(self, context: Dict[str, Any], output_dir: Path) -> None:
        name = context.get("name")
        desc = context.get("description", "A custom Spec Kit preset.")
        
        readme_content = f"""# {name} (Origin Preset)

{desc}

## Overview

This preset customizes the behavior, templates, and scripts for Spec Kit.

## Installation

To install this preset into your active project via Origin:

```bash
origin preset add ./
```

## Structure

- `origin-preset.yaml`: The Origin preset manifest.
- `speckit/preset/`: The native Spec Kit preset files.
  - `commands/`: Custom markdown command definitions.
  - `templates/`: Custom markdown templates.
  - `scripts/`: Custom lifecycle scripts.
"""
        
        with open(output_dir / "README.md", "w") as f:
            f.write(readme_content)
