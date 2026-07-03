---
name: forge-create
description: Generate a new Agent Forge setup from scratch
agent: forge-greenfield-orchestrator
---

/fleet Please generate a complete Agent Forge setup for this new project based on the following description:
> ${input:description:Describe the project and tech stack}

**CRITICAL PREREQUISITE**: 
Before writing any files from scratch, you MUST use your terminal tools to search the Origin Hub Registry for existing, high-quality templates. 
1. Run `origin hub search <tech>` for the core technologies mentioned.
2. If you find highly relevant assets, run `origin hub install <name>` to download them. 
3. Use those installed templates as the foundation for your work.
4. **IMPORTANT**: Completely IGNORE the `.specify` directory if it exists in the project. Do NOT read it, and do NOT attempt to recreate or port its templates into `.github`.

Execute the following tasks in parallel to build the agent factory:

1. `@forge-agent-writer`: Create the necessary agent personas based on the described tech stack (incorporating any installed Hub templates).
2. `@forge-instruction-writer`: Create foundational `.instructions.md` rulesets (e.g., best practices, linters) for the selected technologies.
3. `@forge-skill-writer`: Generate starter `SKILL.md` knowledge packs for the core framework.
4. `@forge-prompt-writer`: Create global slash commands (e.g., `/test`, `/refactor`) to easily trigger these new agents.
