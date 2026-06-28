from pathlib import Path
import yaml
from origin_cli.generators.extension.base import AbstractGenerator
from origin_cli.generators.extension.context import ExtensionContext

class ManifestGenerator(AbstractGenerator):
    def generate(self, context: ExtensionContext, base_dir: Path) -> None:
        manifest = {
            "name": context.name,
            "version": context.version,
            "description": context.description,
            "author": context.author,
            "contributes": {}
        }
        
        contributes = manifest["contributes"]
        
        if context.has_capability("skills"):
            contributes["skills"] = [context.name]
            
        if context.has_capability("commands"):
            contributes["commands"] = [
                f"{context.name}-sync",
                f"{context.name}-create-story"
            ]
            
        if context.has_capability("templates"):
            contributes["templates"] = [
                "release-note"
            ]
            
        if context.has_capability("hooks"):
            contributes["hooks"] = [
                "pre-plan",
                "post-implement"
            ]
            
        if context.has_capability("workflow contributions"):
            contributes["workflow"] = {
                "plan": {"append": "workflow/plan.md"},
                "tasks": {"append": "workflow/tasks.md"},
                "implement": {"append": "workflow/implement.md"}
            }
            
        if context.has_capability("mcp"):
            contributes["mcp"] = {
                "github": {"config": "mcp/github.json"},
                "claude": {"config": "mcp/claude.json"},
                "cursor": {"config": "mcp/cursor.json"}
            }
            
        # Clean empty contributes dict if no capabilities selected
        if not contributes:
            del manifest["contributes"]
            
        manifest_path = base_dir / "origin-extension.yaml"
        
        with open(manifest_path, "w") as f:
            yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
