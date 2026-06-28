from pathlib import Path
from origin_cli.generators.extension.base import AbstractGenerator
from origin_cli.generators.extension.context import ExtensionContext

class DocsGenerator(AbstractGenerator):
    def generate(self, context: ExtensionContext, base_dir: Path) -> None:
        # Create directories
        docs_dir = base_dir / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        examples_dir = base_dir / "examples"
        examples_dir.mkdir(parents=True, exist_ok=True)
        
        # README.md
        readme_path = base_dir / "README.md"
        readme_content = f"""# {context.name} Extension

{context.description}

## Installation

```bash
origin extension install {context.name}
```

## Usage

This extension contributes various AI-driven workflows and capabilities for your Origin-scaffolded projects. 

### Rendering
Origin will natively render this extension into:
- GitHub Copilot (`.github/prompts/` and `.github/agents/`)
- Claude Code (`.claude/`)
- Cursor (`.cursor/`)
- Spec Kit (`.specify/`)
"""
        readme_path.write_text(readme_content)
        
        # docs/overview.md
        overview_path = docs_dir / "overview.md"
        overview_path.write_text(f"# {context.name} Overview\n\nDetailed architectural overview of the {context.name} extension capabilities.")
        
        # examples/install.md
        install_path = examples_dir / "install.md"
        install_path.write_text(f"# Example Installation\n\n```bash\norigin extension install {context.name}\n```")
