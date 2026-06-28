from abc import ABC, abstractmethod
from origin_cli.installer.models import InstallContext, InstallResult

class AbstractInstaller(ABC):
    @abstractmethod
    def install(self, context: InstallContext) -> InstallResult:
        """
        Executes the installation logic for a specific extension component.
        """
        pass
