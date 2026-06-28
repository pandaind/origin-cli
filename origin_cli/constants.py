FLEET_DELEGATION_PROMPT = """---
description: "Generate an agent-aware tasks checklist from the implementation plan"
---
# Task Breakdown & Fleet Delegation

Read the `.specify/implementation_plan.md` and generate a comprehensive `tasks.md` checklist in the project root. 
You must act as an orchestrator and delegate the tasks to the specialized Agent Forge agents.

## Delegation Protocol

1. **Scan Agents**: Review the available specialized agents located in `.github/agents/`.
2. **Delegate**: Assign each task to the most appropriate agent by prefixing the task description with `@agent-name`.
   - Example: `- [ ] @forge-frontend-expert: Create the React components for the login page.`
   - Example: `- [ ] @forge-database-expert: Write the migration script.`
3. **Parallelize**: Ensure independent tasks are assigned to specialized agents so they can be executed in parallel (Fleet Mode).
4. **Formatting**: Use standard GitHub Markdown checkboxes (`- [ ]`).
"""


