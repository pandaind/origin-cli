# 🪐 Origin CLI

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> A unified AI Orchestrator CLI that seamlessly integrates **Agent Forge** and **Spec Kit** to establish a powerful "Coordinator-Worker" AI pattern directly in your VS Code Copilot environment.

## 📖 Table of Contents
- [Overview](#-overview)
- [Prerequisites](#-prerequisites)
- [Installation](./INSTALL.md) ← full cross-platform guide
- [Usage](#-usage)
  - [origin setup](#1-origin-setup)
  - [origin init](#2-origin-init)
- [How it Works](#-how-it-works)
- [Contributing](#-contributing)

---

## 🌟 Overview

`origin` simplifies the setup of multi-agent development workflows by bridging the gap between Agent Forge's expert generation and Spec Kit's Copilot integration. 

By default, it automatically generates a fleet of specialized writer agents (like `@forge-agent-writer`, `@forge-skill-writer`, etc.) natively bridging the gap between Agent Forge's expert generation and Spec Kit's Copilot integration.

## ⚡ Prerequisites

Before installing `origin`, ensure you have:
- **Python 3.9+**
- **Node.js** (npm) installed for `@github/copilot`
- **uv** or **pip** installed for Python dependency management

## 🚀 Installation

To install `origin`, you can install it directly from GitHub using `pip` (or `pipx` for global CLI tools):

```bash
# Install directly from the GitHub repository
pip install git+https://github.com/pandaind/origin-cli.git

# Or if published to a package registry like PyPI:
pip install origin-cli
```

*(Note: For local development, clone the repository and run `pip install -e .` from the root).*

## 💻 Usage

The CLI exposes two primary commands to get your AI environment up and running instantly.

### 1. `origin setup`

This command bootstraps your host machine with the necessary underlying tools.
It auto-detects and installs any missing prerequisites (`node`, `npm`, `pipx`) for your platform.

```bash
origin setup
```

**Interactive flow:**
1. **Mode selection** — choose spec-driven or agent-driven
2. **Agent Forge** — install `@github/copilot` + `@agent-forge-copilot/cli` via npm (optional)
3. **Spec Kit** — install `specify-cli` via pipx (spec-driven mode only)
4. **Headroom** — enable transparent prompt compression (optional)

**Headroom-AI prompt compression:**

When enabled, `headroom wrap` intercepts every LLM call made by `copilot` and `forge`
and compresses the full context window (file reads, tool outputs, previous turns)
before it reaches the model. Typical reduction: **60–95% fewer tokens**.

```bash
origin setup --headroom    # enable compression
origin setup --no-headroom # skip
```

**All flags (non-interactive):**

| Flag | Effect |
|------|--------|
| `--spec` / `--no-spec` | Force spec-driven or agent-driven mode |
| `--copilot` / `--no-copilot` | Install or skip GitHub Copilot CLI + Agent Forge |
| `--headroom` / `--no-headroom` | Enable or skip headroom-ai prompt compression |

### 2. `origin init`

This command performs the "invisible magic" setup inside any project directory to initialize the AI workspace.

```bash
origin init
```
**What it does:**
1. Runs `forge init --mode analyze` to scan your repository and generate implementation agents.
2. Runs `specify init . --integration copilot` to install the base Spec Kit slash commands.

**Options:**
- `--ide` (or `-i`): IDE-Only Mode. Bypasses underlying NPM CLI tools and deploys a bundled fleet of Agent Forge personas directly into your global `~/.copilot/agents/` configuration, along with injecting local prompts.
- `--extension <names>` (or `-e`): Automatically apply integration overrides. Accepts a single extension or a comma/space separated list. Available extensions: `jira`. For example, `--extension jira` injects a `/speckit.taskstoissues` template to natively sync Agent Forge workflows directly with your Jira MCP tools!

### 3. `origin extension`

Origin acts as an orchestrator to manage vendor-neutral AI workspace extensions (packaging GitHub Copilot, Spec Kit, and MCP assets together).

```bash
# Generate a new modular extension
origin extension new <name>

# Install an extension into the current project
origin extension add <path/to/extension>

# Manage extension lifecycle
origin extension remove <name>
origin extension enable <name>
origin extension disable <name>
origin extension list
origin extension info <name>
```

### 4. `origin preset`

Origin securely wraps the native Spec Kit CLI to orchestrate the lifecycle of your custom AI process presets, without overriding Spec Kit's core functionality.

```bash
# Generate a complete Spec Kit preset structure
origin preset new <name>

# Install a preset (delegates natively to Spec Kit)
origin preset add <path/to/preset>

# Manage preset lifecycle
origin preset remove <name>
origin preset enable <name>
origin preset disable <name>
origin preset list
origin preset info <name>
```

## 🧠 How it Works

1. Run `origin setup` once on your machine.
2. Run `origin init` (or `origin init --ide`) in your target repository.
3. Open your project in **VS Code**.
4. Open GitHub Copilot Chat and type `/forge-analyze` (or `/speckit.constitution`) — Copilot will instantly adopt the configured personas and automate the entire project scaffolding process based on the generated instructions!

## 🤝 The Best of Both Worlds

`origin` creates a true **Orchestrator-Worker** architecture by leveraging the strengths of both tools:

- **Spec Kit (The Manager):** Handles high-level orchestration, structured workflows, and task breakdowns (e.g., `/speckit.tasks` and `/speckit.implement`).
- **Agent Forge (The Fleet of Workers):** Scaffolds deeply specialized, domain-specific subagents (e.g., `@forge-frontend-expert`, `@forge-database-expert`).

**The Synergy:**
When you run `origin init`, it automatically overrides Spec Kit's task generator to become "Agent Aware." When Spec Kit creates a `tasks.md` checklist, it explicitly tags the Agent Forge experts (e.g., `- [ ] @forge-frontend-expert: Create the React components`). During execution, Copilot sees these tags and automatically delegates the work to your specialized agents in parallel (**Fleet Mode**)!

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/pandaind/origin-cli/issues).
