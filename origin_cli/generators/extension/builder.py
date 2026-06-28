from pathlib import Path
from typing import List
import typer
from origin_cli.generators.extension.context import ExtensionContext
from origin_cli.generators.extension.base import AbstractGenerator

class ExtensionBuilder:
    def __init__(self, generators: List[AbstractGenerator]):
        self.generators = generators

    def build(self, context: ExtensionContext, output_dir: Path) -> None:
        """
        Executes all registered generators sequentially.
        """
        typer.secho(f"Building extension '{context.name}' in {output_dir}...", fg=typer.colors.CYAN)
        
        # Ensure base output dir exists
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for generator in self.generators:
            generator.generate(context, output_dir)
            
        typer.secho(f"Successfully generated extension '{context.name}'!", fg=typer.colors.GREEN, bold=True)
