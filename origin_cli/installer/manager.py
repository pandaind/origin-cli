import yaml
import typer
import shutil
import datetime
from pathlib import Path
from typing import List

from origin_cli.installer.base import AbstractInstaller
from origin_cli.installer.models import InstallContext, InstallResult
from origin_cli.installer.github_installers import GitHubSkillInstaller, GitHubPromptInstaller, GitHubHookInstaller
from origin_cli.installer.mcp_installer import McpInstaller
from origin_cli.installer.registry import ExtensionRegistry
from origin_cli.installer.speckit_wrapper import SpecKitWrapper

class InstallationManager:
    def __init__(self, installers: List[AbstractInstaller] = None):
        if installers is None:
            self.installers = [
                GitHubSkillInstaller(),
                GitHubPromptInstaller(),
                GitHubHookInstaller(),
                McpInstaller(),
                ExtensionRegistry()
            ]
        else:
            self.installers = installers
            
        self.results: List[InstallResult] = []

    def install_extension(self, source_path: Path, force: bool = False, dry_run: bool = False) -> None:
        typer.secho(f"Validating extension at '{source_path}'...", fg=typer.colors.CYAN)
        
        # 1. Validate
        manifest_path = source_path / "origin-extension.yaml"
        if not source_path.exists() or not source_path.is_dir():
            typer.secho(f"Error: Extension source path does not exist or is not a directory: {source_path}", fg=typer.colors.RED)
            raise typer.Exit(code=1)
            
        if not manifest_path.exists():
            typer.secho(f"Error: Missing origin-extension.yaml at {manifest_path}", fg=typer.colors.RED)
            raise typer.Exit(code=1)
            
        try:
            with open(manifest_path, "r") as f:
                manifest = yaml.safe_load(f)
        except Exception as e:
            typer.secho(f"Error parsing manifest: {e}", fg=typer.colors.RED)
            raise typer.Exit(code=1)
            
        name = manifest.get("name")
        version = manifest.get("version")
        
        if not name:
            typer.secho("Error: Extension manifest is missing 'name'", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        typer.secho(f"✔ Validated {name} (v{version})", fg=typer.colors.GREEN)
        
        # 2. Copy extension to managed directory
        managed_dir = Path.cwd() / ".origin" / "extensions" / name
        if not dry_run:
            managed_dir.parent.mkdir(parents=True, exist_ok=True)
            if managed_dir.exists():
                shutil.rmtree(managed_dir)
            shutil.copytree(source_path, managed_dir)
            
        # 3. Spec Kit Orchestration (Wrapper)
        speckit_ext_dir = managed_dir / "speckit" / "extension"
        speckit_name = None
        if speckit_ext_dir.exists() and speckit_ext_dir.is_dir():
            typer.secho(f"Delegating to Spec Kit to install extension...", fg=typer.colors.CYAN)
            if not dry_run:
                if not SpecKitWrapper.add(speckit_ext_dir):
                    typer.secho("Failed to install Spec Kit extension. Aborting Origin installation.", fg=typer.colors.RED)
                    # rollback copied dir
                    if managed_dir.exists():
                        shutil.rmtree(managed_dir)
                    raise typer.Exit(code=1)
                speckit_name = name # Defaulting to extension name, assumes speckit extension shares the same name

        # Create Context
        context = InstallContext(
            extension_source_path=source_path,
            extension_name=name,
            manifest=manifest,
            force=force,
            dry_run=dry_run
        )
        if dry_run:
            context.managed_dir = source_path
            
        # Hack to inject data into context for registry
        context.manifest["_speckit_extension_name"] = speckit_name
        
        # Track all installed assets across all installers to inject into registry
        all_github_assets = []
        all_mcp_servers = []

        typer.secho(f"\nInstalling Origin-managed assets for {name}...", fg=typer.colors.CYAN)
        
        # Run Installers
        for installer in self.installers:
            # If this is the Registry installer, we inject the accumulated asset paths
            if isinstance(installer, ExtensionRegistry):
                context.manifest["_github_assets"] = all_github_assets
                context.manifest["_mcp_servers"] = all_mcp_servers
                
            result = installer.install(context)
            self.results.append(result)
            self._log_result(result)
            
            # Aggregate assets
            all_github_assets.extend(result.github_assets)
            all_mcp_servers.extend(result.mcp_servers)
            
            # Rollback if an installer failed
            if not result.is_success() and not dry_run:
                typer.secho("Installation failed. Initiating rollback of Origin-managed assets...", fg=typer.colors.YELLOW)
                self.rollback()
                raise typer.Exit(code=1)

        if not dry_run:
            typer.secho(f"\nSuccessfully installed Origin Extension: {name}!", fg=typer.colors.GREEN, bold=True)
        else:
            typer.secho(f"\nDry run complete. No files were modified.", fg=typer.colors.YELLOW, bold=True)

    def _log_result(self, result: InstallResult) -> None:
        if result.errors:
            typer.secho(f"✖ Failed {result.installer_name}", fg=typer.colors.RED)
            for err in result.errors:
                typer.secho(f"  - {err}", fg=typer.colors.RED)
            return

        added_count = len(result.added)
        replaced_count = len(result.replaced)
        skipped_count = len(result.skipped)
        
        if added_count == 0 and replaced_count == 0 and skipped_count == 0:
            return 
            
        typer.secho(f"✔ Installed {result.installer_name} ", fg=typer.colors.GREEN, nl=False)
        details = []
        if added_count > 0:
            details.append(f"{added_count} added")
        if replaced_count > 0:
            details.append(f"{replaced_count} replaced")
        if skipped_count > 0:
            details.append(f"{skipped_count} skipped (conflict)")
            
        if details:
            typer.secho(f"({', '.join(details)})", fg=typer.colors.WHITE)
        else:
            typer.echo("")
            
    def rollback(self):
        """
        Reverts any files that were explicitly added by installers before failure.
        We do NOT revert Spec Kit because Spec Kit manages its own lifecycle.
        """
        for res in reversed(self.results):
            for added_file in res.added:
                p = Path(added_file)
                if p.exists() and p.is_file():
                    p.unlink()
                    typer.secho(f"Rolled back file: {p}", fg=typer.colors.YELLOW)
