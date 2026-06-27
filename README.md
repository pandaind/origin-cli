# 🪐 Origin CLI

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> A unified AI Orchestrator CLI that seamlessly integrates **Agent Forge** and **Spec Kit** to establish a powerful "Coordinator-Worker" AI pattern directly in your VS Code Copilot environment.

## 📖 Table of Contents
- [Overview](#-overview)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
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

```bash
origin setup
```
**What it does:**
- Installs `@github/copilot` globally via `npm` (required by agent-forge).
- Installs `@agent-forge-copilot/cli` globally via `npm`.
- Installs `specify-cli` globally via `uv` (falling back to `pip` if `uv` isn't found).

**Options:**
- `--no-copilot`: Skip the NPM installations of GitHub Copilot CLI and Agent Forge if you already have them or prefer to manage them manually. You will be prompted interactively by default if you do not supply this flag.

### 2. `origin init`

This command performs the "invisible magic" setup inside any project directory to initialize the AI workspace.

```bash
origin init
```
**What it does:**
1. Runs `forge init --mode analyze` to scan your repository and generate implementation agents.
2. Runs `specify init . --integration copilot` to install the base Spec Kit slash commands.

**IDE-Only Mode:**
```bash
origin init --ide
```
If you prefer not to rely on the underlying NPM CLI tools to initialize your workspace, the `--ide` (or `-i`) flag bypasses them entirely. Instead, it:
1. Deploys a bundled fleet of Agent Forge personas (e.g. `@forge-brownfield-orchestrator`) directly into your global `~/.copilot/agents/` configuration.
2. Injects the highly-capable `/forge-create` and `/forge-analyze` entrypoint slash commands directly into your project's `.github/prompts/` folder.

## 🧠 How it Works

1. Run `origin setup` once on your machine.
2. Run `origin init` (or `origin init --ide`) in your target repository.
3. Open your project in **VS Code**.
4. Open GitHub Copilot Chat and type `/forge-analyze` (or `/speckit.constitution`) — Copilot will instantly adopt the configured personas and automate the entire project scaffolding process based on the generated instructions!

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/pandaind/origin-cli/issues).
