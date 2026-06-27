---
name: forge-analyze
description: Scan this codebase and generate Agent Forge setup
agent: forge-brownfield-orchestrator
---

/fleet Please scan this existing codebase and generate a complete Agent Forge setup tailored to the actual patterns used here. Execute the following tasks in parallel:

1. `@forge-agent-writer`: Scan the codebase to identify the tech stack and create core agent personas (e.g., developer, reviewer) tailored to this specific repository.
2. `@forge-instruction-writer`: Analyze existing code to generate `.instructions.md` rulesets that enforce the actual coding standards and patterns found here.
3. `@forge-skill-writer`: Document the core architectural patterns and domain knowledge into a `SKILL.md` file.
4. `@forge-prompt-writer`: Generate useful slash commands for the new agents created in Task 1.
5. `@forge-hook-writer`: Scaffold Copilot lifecycle hooks for automated validation if applicable.
