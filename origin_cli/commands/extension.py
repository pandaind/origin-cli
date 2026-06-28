import typer
from rich.prompt import Prompt, Confirm
from pathlib import Path

from origin_cli.generators.extension.context import ExtensionContext
from origin_cli.generators.extension.builder import ExtensionBuilder
from origin_cli.generators.extension.manifest import ManifestGenerator
from origin_cli.generators.extension.docs import DocsGenerator
from origin_cli.generators.extension.skills import SkillsGenerator
from origin_cli.generators.extension.commands_gen import CommandsGenerator
from origin_cli.generators.extension.mcp import McpGenerator
from origin_cli.generators.extension.hooks import HooksGenerator
from origin_cli.generators.extension.workflow import WorkflowGenerator
from origin_cli.generators.extension.templates import TemplatesGenerator
from origin_cli.generators.extension.assets import AssetsGenerator
from origin_cli.generators.extension.tests_gen import TestsGenerator

app = typer.Typer(help="Manage Origin extensions")

@app.command(name="new")
def new_extension(
    name: str = typer.Argument(..., help="The name of the extension to scaffold")
):
    """
    Scaffold a new Origin extension with specific capabilities.
    """
    typer.secho(f"\nScaffolding new Origin extension: {name}\n", fg=typer.colors.CYAN, bold=True)
    
    # Interactive Prompts
    description = Prompt.ask("Description")
    author = Prompt.ask("Author")
    version = Prompt.ask("Version", default="0.1.0")
    license_val = Prompt.ask("License", default="MIT")
    
    typer.secho("\nCapabilities", bold=True)
    capabilities = set()
    
    for cap in ["Skills", "Commands", "MCP", "Hooks", "Templates", "Workflow Contributions"]:
        if Confirm.ask(f"Include {cap}?"):
            capabilities.add(cap.lower())
            
    # Create context
    context = ExtensionContext(
        name=name,
        description=description,
        author=author,
        version=version,
        license=license_val,
        capabilities=capabilities
    )
    
    # Register generators
    generators = [
        ManifestGenerator(),
        DocsGenerator(),
        SkillsGenerator(),
        CommandsGenerator(),
        McpGenerator(),
        HooksGenerator(),
        WorkflowGenerator(),
        TemplatesGenerator(),
        AssetsGenerator(),
        TestsGenerator()
    ]
    
    # Build
    builder = ExtensionBuilder(generators)
    output_dir = Path.cwd() / f"{name}-extension"
    
    builder.build(context, output_dir)

@app.command(name="add")
def add_extension(
    source: str = typer.Argument(..., help="Path or URL to the extension"),
    force: bool = typer.Option(False, "--force", "-f", help="Force overwrite existing files"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate installation without making changes")
):
    """
    Install an Origin extension into the current project.
    """
    from origin_cli.installer.manager import InstallationManager
    
    # In this MVP, we treat `source` as a local path.
    # Remote git URL resolution would happen here before proceeding.
    source_path = Path(source).resolve()
    
    manager = InstallationManager()
    manager.install_extension(source_path=source_path, force=force, dry_run=dry_run)
@app.command(name="remove")
def remove_extension(
    name: str = typer.Argument(..., help="The name of the extension to remove")
):
    """
    Remove an Origin extension from the current project.
    """
    from origin_cli.installer.remover import ExtensionRemover
    remover = ExtensionRemover()
    remover.remove(name)

@app.command(name="enable")
def enable_extension(
    name: str = typer.Argument(..., help="The name of the extension to enable")
):
    """
    Enable a previously disabled Origin extension.
    """
    from origin_cli.installer.status import ExtensionStatusManager
    ExtensionStatusManager.enable(name)

@app.command(name="disable")
def disable_extension(
    name: str = typer.Argument(..., help="The name of the extension to disable")
):
    """
    Disable an active Origin extension.
    """
    from origin_cli.installer.status import ExtensionStatusManager
    ExtensionStatusManager.disable(name)

@app.command(name="list")
def list_extensions():
    """
    List all installed extensions (Origin and Spec Kit).
    """
    from origin_cli.installer.status import ExtensionStatusManager
    ExtensionStatusManager.list()

@app.command(name="info")
def info_extension(
    name: str = typer.Argument(..., help="The name of the extension")
):
    """
    Show detailed information about an installed extension.
    """
    from origin_cli.installer.status import ExtensionStatusManager
    ExtensionStatusManager.info(name)
