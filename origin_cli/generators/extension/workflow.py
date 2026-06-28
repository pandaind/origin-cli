from pathlib import Path
from origin_cli.generators.extension.base import AbstractGenerator
from origin_cli.generators.extension.context import ExtensionContext

class WorkflowGenerator(AbstractGenerator):
    def generate(self, context: ExtensionContext, base_dir: Path) -> None:
        if not context.has_capability("workflow contributions"):
            return
            
        workflow_dir = base_dir / "workflow"
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        for phase in ["plan", "tasks", "implement"]:
            workflow_path = workflow_dir / f"{phase}.md"
            workflow_path.write_text(f"""# {context.name.capitalize()} {phase} contribution

If {context.name} skill exists:
- Perform {context.name} specific actions during the {phase} workflow.
""")
