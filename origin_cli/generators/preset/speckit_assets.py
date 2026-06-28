from pathlib import Path
from origin_cli.generators.extension.base import AbstractGenerator
from typing import Dict, Any

class SpecKitAssetsGenerator(AbstractGenerator):
    def generate(self, context: Dict[str, Any], output_dir: Path) -> None:
        preset_dir = output_dir / "speckit" / "preset"
        
        # Commands
        commands_dir = preset_dir / "commands"
        commands_dir.mkdir(parents=True, exist_ok=True)
        for cmd in ["specify", "plan", "tasks", "implement", "analyze", "constitution"]:
            with open(commands_dir / f"{cmd}.md", "w") as f:
                f.write(f"---\ndescription: Custom {cmd} command for this preset\n---\n\n# Custom {cmd.capitalize()} Command\n")
                
        # Templates
        templates_dir = preset_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        for tpl in ["spec", "plan", "tasks", "checklist", "constitution"]:
            with open(templates_dir / f"{tpl}.md", "w") as f:
                f.write(f"# Custom {tpl.capitalize()} Template\n")
                
        # Scripts
        scripts_dir = preset_dir / "scripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        for script in ["pre-plan", "post-plan", "pre-implement", "post-implement"]:
            script_path = scripts_dir / f"{script}.sh"
            with open(script_path, "w") as f:
                f.write(f"#!/bin/bash\n# Custom {script} script\necho 'Running {script}'\n")
            # chmod +x would happen here if supported natively, but simple write is fine for scaffold
