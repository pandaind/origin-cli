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
  - [origin migrate](#6-origin-migrate)
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

The CLI exposes core commands to get your AI environment up and running instantly.

### 1. `origin setup`

This command bootstraps your host machine with the necessary underlying tools.
It auto-detects and installs any missing prerequisites (`node`, `npm`, `pipx`) natively for Mac, Windows, or Linux.

```bash
origin setup
```

**Interactive Configuration:**
1. **Methodology** — Choose how you want to develop:
   - **Spec Driven Development (SDD)**: Architect-first workflow using Spec Kit.
   - **Agent Driven Development (ADD)**: Agent-first workflow using Agent Forge.
2. **Execution Environment** — Choose where you want the AI orchestration to happen:
   - **CLI Toolchains**: Installs robust global packages (`specify-cli`, `@agent-forge-copilot/cli`).
   - **IDE Native**: Zero global dependencies. Installs assets directly into native `.github/`, `.claude/`, or `.cursor/` configuration folders.
3. **Headroom** — Enable transparent prompt compression for token efficiency (optional).

### 2. `origin init`

This command initializes the AI workspace for a specific project.

```bash
origin init
```

**What it does:**
If you selected **CLI Toolchains** during setup, it orchestrates heavy commands like `forge init` and `specify init`.
If you selected **IDE Native**, or pass an `--ide` flag directly, it bypasses the heavy CLI tooling and instantly scaffolds local agent, skill, and instruction files directly into your IDE's native configuration structure.

**Options:**
- `--ide [copilot|vscode|claude|cursor]`: Forces IDE Native initialization and targets a specific editor's layout.
- `--extension <names>`: Applies integration overrides (e.g., `jira` to sync workflows to Jira issues).

### 3. `origin hub`

The Origin Hub is a decentralized package registry for AI assets (Agents, Instructions, Skills, Workflows, Extensions).

```bash
# Scaffold a new package with boilerplate templates
origin hub create my-database-expert --type agent

# Publish an asset bundle to the registry
origin hub publish ./my-database-expert

# Install a community asset seamlessly into your project
origin hub install forge-frontend-expert

# Discover new assets
origin hub search "react"
```

### 4. `origin extension`

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

### 5. `origin preset`

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

### 6. `origin migrate`

Seamlessly migrate your local project configuration (prompts, agents, rules) from one IDE folder structure to another.

```bash
# Migrate project setup from GitHub Copilot to Cursor
origin migrate --from copilot --to cursor

# Copy the configuration instead of moving it
origin migrate --from copilot --to cursor --copy
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
