from abc import ABC, abstractmethod
from pathlib import Path
from origin_cli.generators.extension.context import ExtensionContext

class AbstractGenerator(ABC):
    @abstractmethod
    def generate(self, context: ExtensionContext, base_dir: Path) -> None:
        """
        Generates the necessary files and directories for a specific extension capability.
        """
        pass
