from dataclasses import dataclass, field
from typing import Set

@dataclass
class ExtensionContext:
    name: str
    description: str
    author: str
    version: str
    license: str
    capabilities: Set[str] = field(default_factory=set)

    def has_capability(self, capability: str) -> bool:
        return capability.lower() in self.capabilities
