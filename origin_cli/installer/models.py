from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, List

@dataclass
class InstallContext:
    extension_source_path: Path
    extension_name: str
    manifest: Dict[str, Any]
    force: bool = False
    dry_run: bool = False
    managed_dir: Path = field(init=False)
    
    def __post_init__(self):
        self.managed_dir = Path(".origin/extensions") / self.extension_name

@dataclass
class InstallResult:
    installer_name: str
    added: List[str] = field(default_factory=list)
    replaced: List[str] = field(default_factory=list)
    skipped: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    
    # Specific asset tracking for registry and removal
    mcp_servers: List[str] = field(default_factory=list)
    github_assets: List[str] = field(default_factory=list)
    speckit_extension_name: str = None

    def is_success(self) -> bool:
        return len(self.errors) == 0
