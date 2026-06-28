from pathlib import Path
import json
from origin_cli.generators.extension.base import AbstractGenerator
from origin_cli.generators.extension.context import ExtensionContext

class McpGenerator(AbstractGenerator):
    def generate(self, context: ExtensionContext, base_dir: Path) -> None:
        if not context.has_capability("mcp"):
            return
            
        mcp_dir = base_dir / "mcp"
        mcp_dir.mkdir(parents=True, exist_ok=True)
        
        mcp_config = {
            "mcpServers": {
                context.name: {
                    "command": "npx",
                    "args": ["-y", f"@modelcontextprotocol/server-{context.name}"]
                }
            }
        }
        
        for editor in ["github", "claude", "cursor"]:
            config_path = mcp_dir / f"{editor}.json"
            with open(config_path, "w") as f:
                json.dump(mcp_config, f, indent=2)
