import typer
from pathlib import Path
from typing import List, Dict, Any
from origin_cli.generators.extension.base import AbstractGenerator

class PresetBuilder:
    def __init__(self, generators: List[AbstractGenerator]):
        self.generators = generators

    def build(self, context: Dict[str, Any], output_dir: Path) -> None:
        name = context.get("name")
        typer.secho(f"Generating preset '{name}' at {output_dir}...", fg=typer.colors.CYAN)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for generator in self.generators:
            generator.generate(context, output_dir)
            
        typer.secho(f"Successfully generated preset '{name}'!", fg=typer.colors.GREEN, bold=True)
