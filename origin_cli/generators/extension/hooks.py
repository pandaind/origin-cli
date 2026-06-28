from pathlib import Path
from origin_cli.generators.extension.base import AbstractGenerator
from origin_cli.generators.extension.context import ExtensionContext

class HooksGenerator(AbstractGenerator):
    def generate(self, context: ExtensionContext, base_dir: Path) -> None:
        if not context.has_capability("hooks"):
            return
            
        hooks_dir = base_dir / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)
        
        for hook_name in ["pre-plan", "post-plan", "pre-implement", "post-implement"]:
            hook_path = hooks_dir / f"{hook_name}.md"
            hook_path.write_text(f"""# {context.name.capitalize()} {hook_name} hook

Execute {context.name} specific instructions during the {hook_name} phase.
""")
