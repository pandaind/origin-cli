from pathlib import Path
from origin_cli.generators.extension.base import AbstractGenerator
from origin_cli.generators.extension.context import ExtensionContext

class SkillsGenerator(AbstractGenerator):
    def generate(self, context: ExtensionContext, base_dir: Path) -> None:
        if not context.has_capability("skills"):
            return
            
        skill_dir = base_dir / "skills" / context.name
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        skill_path = skill_dir / "SKILL.md"
        skill_path.write_text(f"""---
name: {context.name}
description: "Core skill integrating {context.name} workflows"
---

# {context.name.capitalize()} Skill

## Purpose
Enables AI agents to seamlessly interact with {context.name}.

## When to use
Activate this skill when the user requests operations related to {context.name}.

## Examples
- "Sync {context.name} tickets"
- "Create a new {context.name} artifact"

## Best practices
- Always validate context before executing {context.name} actions.

## MCP usage
Leverage the configured MCP servers for {context.name} to perform actions.

## Fallback behavior
If MCP is unavailable, fallback to terminal CLI commands or inform the user.
""")

        examples_path = skill_dir / "examples.md"
        examples_path.write_text(f"# Examples for {context.name} skill\n\n- Example 1\n- Example 2")
        
        troubleshoot_path = skill_dir / "troubleshooting.md"
        troubleshoot_path.write_text(f"# Troubleshooting {context.name} skill\n\nCheck MCP connections.")
