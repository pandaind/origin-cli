---
name: forge-analyze
description: Scan this codebase and generate Agent Forge setup
agent: forge-brownfield-orchestrator
---

/fleet Please scan this existing codebase and generate a complete Agent Forge setup tailored to the actual patterns used here. 

**CRITICAL PREREQUISITE**: 
Before generating the setup from scratch, you MUST use your terminal tools to check the Origin Hub Registry for official templates matching this tech stack.
1. Run `origin hub search <framework>` to find matching assets.
2. If you find highly relevant assets, run `origin hub install <name>` to download them into this project.
3. Use those installed templates as the baseline, and adapt them to match the specific patterns you scanned in this codebase.
4. **IMPORTANT**: Completely IGNORE the `.specify` directory if it exists in the project. Do NOT read it, and do NOT attempt to recreate or port its templates into `.github`.

Execute the following tasks in parallel:

1. `@forge-agent-writer`: Scan the codebase to identify the tech stack and create core agent personas (incorporating any Hub templates installed above).
2. `@forge-instruction-writer`: Analyze existing code to generate `.instructions.md` rulesets that enforce the actual coding standards and patterns found here.
3. `@forge-skill-writer`: Document the core architectural patterns and domain knowledge into a `SKILL.md` file.
4. `@forge-prompt-writer`: Generate useful slash commands for the new agents created in Task 1.
5. `@forge-hook-writer`: Scaffold Copilot lifecycle hooks for automated validation if applicable.
