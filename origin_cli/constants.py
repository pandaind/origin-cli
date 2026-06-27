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

JIRA_PRESET_PROMPT = """---
description: "Break down a Jira Epic into Agent-aware sub-tasks via MCP"
---
# Jira Epic to Agent Forge Tasks

Please use your Jira MCP tool to fetch the requested Epic, break it down into technical implementation tasks, and write them back into Jira as sub-tasks assigned to the specialized Agent Forge fleet.

## Execution Protocol

1. **Fetch Epic**: Use your Jira MCP tool to read the Epic ID provided by the user.
2. **Breakdown**: Analyze the Epic's acceptance criteria and break it down into smaller, technical implementation sub-tasks.
3. **Agent Selection**: Review the available specialized agents located in `.github/agents/`.
4. **Write to Jira**: Use your Jira MCP tool to create a sub-task for each technical task. 
5. **Agent Assignment**: In the description of EACH sub-task you create in Jira, you MUST prepend the assignment tag so the IDE knows which agent to route the work to.
   - Format: `Assigned AI Worker: @agent-name`
   - Example: `Assigned AI Worker: @forge-database-expert`

Input Epic ID: ${input:epic_id:Enter the Jira Epic ID (e.g. PROJ-123)}
"""

GIT_PRESET_PROMPT = """---
description: "Review changes, commit, and create a PR using the Agent Forge fleet"
---
# Git Workflow & Code Review

Please use your Git MCP tools or terminal access to review the current workspace changes.

## Execution Protocol
1. **Analyze Changes**: Review the `git diff` for all staged and unstaged changes.
2. **Agent Review**: Delegate a review of the changes to the appropriate domain expert in `.github/agents/` (e.g., `@forge-security-expert` or `@forge-frontend-expert`).
3. **Commit**: If the expert approves, commit the changes using the conventional commit format.
4. **Pull Request**: Push the branch and create a Pull Request. Include the expert's review summary in the PR description.
"""

JENKINS_PRESET_PROMPT = """---
description: "Trigger a Jenkins build and orchestrate DevOps agents on failure"
---
# Jenkins CI/CD Orchestration

Please use your Jenkins MCP tool to trigger the CI/CD pipeline for the current branch.

## Execution Protocol
1. **Trigger Build**: Trigger the Jenkins build for the current branch.
2. **Monitor**: Poll the build status until it completes.
3. **Handle Failure**: If the build fails, fetch the Jenkins build logs.
4. **Delegate Triage**: Create a `tasks.md` checklist containing the failure logs and assign a triage task to the `@forge-devops-expert` or the appropriate domain expert to investigate and fix the pipeline.
"""
