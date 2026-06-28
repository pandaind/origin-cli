from pathlib import Path
from origin_cli.installer.base import AbstractInstaller
from origin_cli.installer.models import InstallContext, InstallResult
from origin_cli.installer.file_utils import merge_json

class McpInstaller(AbstractInstaller):
    def install(self, context: InstallContext) -> InstallResult:
        src_dir = context.managed_dir / "mcp"
        dest_json = Path.cwd() / ".vscode" / "mcp.json"
        
        all_added = []
        all_replaced = []
        all_skipped = []
        all_errors = []

        if src_dir.exists() and src_dir.is_dir():
            for json_file in src_dir.glob("*.json"):
                added, replaced, skipped, errors = merge_json(json_file, dest_json, force=context.force, dry_run=context.dry_run)
                all_added.extend(added)
                all_replaced.extend(replaced)
                all_skipped.extend(skipped)
                all_errors.extend(errors)

        mcp_servers = []
        for msg in all_added + all_replaced:
            if msg.startswith("mcpServers."):
                mcp_servers.append(msg.split(" ")[0].replace("mcpServers.", ""))

        return InstallResult(
            installer_name="MCP Config", 
            added=all_added, 
            replaced=all_replaced, 
            skipped=all_skipped, 
            errors=all_errors,
            mcp_servers=list(set(mcp_servers))
        )
