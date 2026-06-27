# 🪐 Origin CLI

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> A unified AI Orchestrator CLI that seamlessly integrates **Agent Forge** and **Spec Kit** to establish a "Coordinator-Worker" AI pattern in your projects.

## 📖 Table of Contents
- [Overview](#-overview)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
  - [origin setup](#1-origin-setup)
  - [origin init-project](#2-origin-init-project)
- [How it Works](#-how-it-works)
- [Contributing](#-contributing)

---

## 🌟 Overview

`origin` simplifies the setup of multi-agent development workflows by bridging the gap between Agent Forge's expert generation and Spec Kit's Copilot integration. 

By default, it automatically generates a `@legislator` agent responsible for architectural planning and constitution drafting, and dynamically configures GitHub Copilot commands to route specific workflows directly to this agent inside your IDE.

## ⚡ Prerequisites

Before installing `origin`, ensure you have:
- **Python 3.9+**
- **Node.js** (npm) installed for `@github/copilot`
- **uv** or **pip** installed for Python dependency management

## 🚀 Installation

To install `origin` without manually cloning the repository, you can install it directly from GitHub using `pip` (or `pipx` for global CLI tools):

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

```bash
origin setup
```
**What it does:**
- Installs `@github/copilot` globally via `npm` (required by agent-forge).
- Installs `@agent-forge-copilot/cli` globally via `npm`.
- Installs `specify-cli` globally via `uv` (falling back to `pip` if `uv` isn't found).

### 2. `origin init-project`

This command performs the "invisible magic" setup inside any project directory.

```bash
origin init-project
```
**What it does:**
1. Runs `forge init --mode analyze` to scan your repository and generate implementation agents.
2. Runs `specify init . --integration copilot` to install the base Spec Kit slash commands.
3. Automatically generates the `.github/agents/legislator.agent.md` persona.
4. Cross-wires the Spec Kit commands by creating `.specify/templates/overrides/commands/speckit.constitution.prompt.md` tied to the `@legislator` agent.
5. Injects a baseline `CONSTITUTION.md` into the project root if it does not already exist.

## 🧠 How it Works

1. Run `origin setup` once on your machine.
2. Run `origin init` in your target repository.
3. Open your project in **VS Code**.
4. Open GitHub Copilot Chat and type `/speckit.constitution` — Copilot will instantly adopt the `@legislator` persona based on the files `origin` generated for you!

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/pandaind/origin-cli/issues).
