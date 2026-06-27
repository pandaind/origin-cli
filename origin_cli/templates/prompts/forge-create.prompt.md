---
name: forge-create
description: Generate a new Agent Forge setup from scratch
agent: forge-greenfield-orchestrator
---

/fleet Please generate a complete Agent Forge setup for this new project based on the following description:
> ${input:description:Describe the project and tech stack}

Execute the following tasks in parallel to build the agent factory:

1. `@forge-agent-writer`: Create the necessary agent personas based on the described tech stack.
2. `@forge-instruction-writer`: Create foundational `.instructions.md` rulesets (e.g., best practices, linters) for the selected technologies.
3. `@forge-skill-writer`: Generate starter `SKILL.md` knowledge packs for the core framework.
4. `@forge-prompt-writer`: Create global slash commands (e.g., `/test`, `/refactor`) to easily trigger these new agents.
