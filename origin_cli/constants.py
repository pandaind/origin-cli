FLEET_DELEGATION_PROMPT = """---
description: "Generate an agent-aware tasks checklist from the implementation plan"
agent: speckit.tasks
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

IMPLEMENT_OVERRIDE_PROMPT = """---
description: "Execute implementation tasks with MCP and Skill awareness"
agent: speckit.implement
---
# Implementation Orchestrator

You are the Implementation Orchestrator. Read the `tasks.md` checklist and execute each uncompleted task sequentially or by delegating to specialized agents.

## Execution Rules:
1. **MCP Integration**: Scan the currently enabled and running MCP servers in your environment. If a task requires external context (like Jira tickets, Git operations, or database schemas), you MUST actively use the appropriate MCP tools.
2. **Skill Utilization**: Review the available `SKILL.md` and `.instructions.md` files in the workspace (under `.github/` or `.specify/`). Follow their exact guidelines on *how* and *when* to implement specific architectural patterns.
3. **Delegation**: If a task is assigned to a specific `@agent-name`, use your subagent capabilities to delegate the work.
4. **Completion**: Update `tasks.md` by marking `[x]` as tasks are completed.
"""

JIRA_EXTENSION_PROMPT = """---
description: Convert existing tasks into actionable Jira issues for the feature based on available design artifacts.
tools: ['jira-mcp/search_issues', 'jira-mcp/create_issue']
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before tasks-to-issues conversion)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_taskstoissues` key
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- For each executable hook, output the following based on its `optional` flag:
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Pre-Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Mandatory hook** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Pre-Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}

    Wait for the result of the hook command before proceeding to the Outline.
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session. Emitting the block alone does not run the hook.
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## Outline

1. Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute.
1. **IF EXISTS**: Load `.specify/memory/constitution.md` for project principles and governance constraints.
1. From the executed script, extract the path to **tasks**.
1. **Fetch existing Jira issues for deduplication**: Before creating anything, build the set of task IDs you are about to process from `tasks.md` (e.g. `T001`). Use the Jira MCP server's `search_issues` tool to look for issues that already cover those IDs to avoid duplicating work.
1. For each task in the list, use the Jira MCP server to create a new Jira issue. Task lines in `tasks.md` start with a markdown checkbox, so first strip the leading `- [ ]` (and any `[P]` / `[US#]` markers) to recover the task ID and its description. 
   - Create the issue with a canonical title of the form `T001: <description>`.
   - **Skip** any task whose ID is already present in the set of existing Jira issues.
   - **Agent Assignment**: If the task line contains an `@agent-name` tag (e.g. `@forge-database-expert`), ensure this tag is preserved in the Jira ticket description so the Agent Forge worker knows it is assigned.

## Post-Execution Checks

**Check for extension hooks (after tasks-to-issues conversion)**:
Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.after_taskstoissues` key
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- For each executable hook, output the following based on its `optional` flag:
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Mandatory hook** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session. Emitting the block alone does not run the hook.
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently
"""
