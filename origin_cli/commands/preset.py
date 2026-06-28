import typer
from pathlib import Path
from origin_cli.generators.preset.builder import PresetBuilder
from origin_cli.generators.preset.manifest import PresetManifestGenerator
from origin_cli.generators.preset.docs import PresetDocsGenerator
from origin_cli.generators.preset.speckit_assets import SpecKitAssetsGenerator
from origin_cli.installer.preset_manager import PresetInstallationManager
from origin_cli.installer.preset_remover import PresetRemover
from origin_cli.installer.preset_status import PresetStatusManager

app = typer.Typer(help="Manage Origin presets (Spec Kit customization).")

@app.command(name="new")
def new_preset(
    name: str = typer.Argument(..., help="The name of the new preset")
):
    """
    Generate a new Origin preset.
    """
    typer.secho(f"Scaffolding new Origin Preset: {name}\n", fg=typer.colors.CYAN, bold=True)
    
    # Interactive Prompts
    description = typer.prompt("Description", default="A custom Spec Kit preset.")
    author = typer.prompt("Author", default="Unknown")
    version = typer.prompt("Version", default="1.0.0")
    license_type = typer.prompt("License", default="MIT")
    
    context = {
        "name": name,
        "description": description,
        "author": author,
        "version": version,
        "license": license_type
    }
    
    generators = [
        PresetManifestGenerator(),
        PresetDocsGenerator(),
        SpecKitAssetsGenerator()
    ]
    
    builder = PresetBuilder(generators)
    output_dir = Path.cwd() / f"{name}-preset"
    
    builder.build(context, output_dir)

@app.command(name="add")
def add_preset(
    source: str = typer.Argument(..., help="Path or URL to the preset"),
    force: bool = typer.Option(False, "--force", "-f", help="Force overwrite existing files"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate installation without making changes")
):
    """
    Install an Origin preset into the current project.
    """
    source_path = Path(source).resolve()
    manager = PresetInstallationManager()
    manager.install_preset(source_path=source_path, force=force, dry_run=dry_run)

@app.command(name="remove")
def remove_preset(
    name: str = typer.Argument(..., help="The name of the preset to remove")
):
    """
    Remove an Origin preset from the current project.
    """
    remover = PresetRemover()
    remover.remove(name)

@app.command(name="enable")
def enable_preset(
    name: str = typer.Argument(..., help="The name of the preset to enable")
):
    """
    Enable a previously disabled Origin preset.
    """
    PresetStatusManager.enable(name)

@app.command(name="disable")
def disable_preset(
    name: str = typer.Argument(..., help="The name of the preset to disable")
):
    """
    Disable an active Origin preset.
    """
    PresetStatusManager.disable(name)

@app.command(name="list")
def list_presets():
    """
    List all installed presets (Origin and Spec Kit).
    """
    PresetStatusManager.list()

@app.command(name="info")
def info_preset(
    name: str = typer.Argument(..., help="The name of the preset")
):
    """
    Show detailed information about an installed preset.
    """
    PresetStatusManager.info(name)
