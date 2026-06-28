from pathlib import Path
from origin_cli.generators.extension.base import AbstractGenerator
from origin_cli.generators.extension.context import ExtensionContext

class TemplatesGenerator(AbstractGenerator):
    def generate(self, context: ExtensionContext, base_dir: Path) -> None:
        if not context.has_capability("templates"):
            return
            
        templates_dir = base_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        for template in ["release-note", "architecture-review", f"{context.name}-story"]:
            template_path = templates_dir / f"{template}.md"
            template_path.write_text(f"""# {template.replace('-', ' ').title()}

Generated template for {context.name} integration.
""")
