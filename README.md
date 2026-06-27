# Origin CLI

A unified AI Orchestrator CLI that seamlessly integrates **Agent Forge** and **Spec Kit** to establish a "Coordinator-Worker" AI pattern in your projects.

## Overview

`origin` simplifies the setup of multi-agent development workflows by combining Agent Forge's expert generation with Spec Kit's Copilot integration. It automatically generates a `@legislator` agent responsible for architectural planning and constitution drafting, and configures GitHub Copilot commands to route specific workflows to this agent.

## Installation

To install `origin` without manually downloading or cloning the repository, you can install it directly from GitHub using `pip` (or `pipx` for global CLI tools):

```bash
# Install directly from the GitHub repository
pip install git+https://github.com/pandaind/origin-cli.git

# Or if published to a package registry like PyPI:
pip install origin-cli
```

*(Note: For local development, you can use `pip install -e .` from the root of this repository).*

## Commands

### `origin setup`

Checks for and installs the necessary underlying tools on your host machine:
- Installs `@github/copilot` globally via `npm` (required prerequisite for agent-forge).
- Installs `@agent-forge-copilot/cli` globally via `npm`.
- Installs `specify-cli` globally via `uv` (or `pip` as a fallback).

**Usage:**
```bash
origin setup
```

### `origin init-project`

Performs the "invisible magic" setup to initialize a project with Agent Forge and Spec Kit. It will:
1. Run `forge init --mode analyze` to scan your repository and generate implementation agents.
2. Run `specify init . --integration copilot` to install the base Spec Kit slash commands.
3. Automatically generate the `.github/agents/legislator.agent.md` persona.
4. Cross-wire the Spec Kit commands by creating `.specify/templates/overrides/commands/speckit.constitution.prompt.md` tied to the `@legislator` agent.
5. Inject a baseline `CONSTITUTION.md` into the project root if it does not already exist.

**Usage:**
```bash
origin init-project
```
