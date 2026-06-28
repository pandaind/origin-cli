from pathlib import Path
from origin_cli.generators.extension.base import AbstractGenerator
from origin_cli.generators.extension.context import ExtensionContext

class CommandsGenerator(AbstractGenerator):
    def generate(self, context: ExtensionContext, base_dir: Path) -> None:
        if not context.has_capability("commands"):
            return
            
        commands_dir = base_dir / "commands"
        commands_dir.mkdir(parents=True, exist_ok=True)
        
        sync_path = commands_dir / f"{context.name}-sync.md"
        sync_path.write_text(f"""---
description: "Sync {context.name} artifacts with the workspace"
---
# {context.name.capitalize()} Sync

Please sync the remote {context.name} environment with the local workspace using available MCP tools.
""")

        create_path = commands_dir / f"{context.name}-create-story.md"
        create_path.write_text(f"""---
description: "Create a new story/ticket in {context.name}"
---
# Create {context.name.capitalize()} Story

Analyze the provided requirements and create a structured artifact in {context.name}.
""")

        release_path = commands_dir / f"{context.name}-release.md"
        release_path.write_text(f"""---
description: "Draft release notes for {context.name}"
---
# {context.name.capitalize()} Release

Generate release notes and publish them via {context.name} integrations.
""")
