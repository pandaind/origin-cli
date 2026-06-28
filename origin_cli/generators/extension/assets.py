from pathlib import Path
from origin_cli.generators.extension.base import AbstractGenerator
from origin_cli.generators.extension.context import ExtensionContext

class AssetsGenerator(AbstractGenerator):
    def generate(self, context: ExtensionContext, base_dir: Path) -> None:
        assets_dir = base_dir / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
