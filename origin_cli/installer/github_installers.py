from pathlib import Path
from origin_cli.installer.base import AbstractInstaller
from origin_cli.installer.models import InstallContext, InstallResult
from origin_cli.installer.file_utils import copy_directory

class GitHubSkillInstaller(AbstractInstaller):
    def install(self, context: InstallContext) -> InstallResult:
        src = context.managed_dir / "github" / "skills"
        dest = Path.cwd() / ".github" / "skills"
        
        added, replaced, skipped, errors = copy_directory(src, dest, force=context.force, dry_run=context.dry_run)
        github_assets = added + replaced
        return InstallResult(installer_name="GitHub Skills", added=added, replaced=replaced, skipped=skipped, errors=errors, github_assets=github_assets)


class GitHubPromptInstaller(AbstractInstaller):
    def install(self, context: InstallContext) -> InstallResult:
        src = context.managed_dir / "github" / "prompts"
        dest = Path.cwd() / ".github" / "prompts"
        
        added, replaced, skipped, errors = copy_directory(src, dest, force=context.force, dry_run=context.dry_run)
        github_assets = added + replaced
        return InstallResult(installer_name="GitHub Prompts", added=added, replaced=replaced, skipped=skipped, errors=errors, github_assets=github_assets)


class GitHubHookInstaller(AbstractInstaller):
    def install(self, context: InstallContext) -> InstallResult:
        src = context.managed_dir / "github" / "hooks"
        dest = Path.cwd() / ".github" / "hooks"
        
        added, replaced, skipped, errors = copy_directory(src, dest, force=context.force, dry_run=context.dry_run)
        github_assets = added + replaced
        return InstallResult(installer_name="GitHub Hooks", added=added, replaced=replaced, skipped=skipped, errors=errors, github_assets=github_assets)
