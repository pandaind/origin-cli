# Installation

## Prerequisites

- **Python 3.9+**

> **Note:** Node.js/npm and pipx are also required by `origin setup`, but the CLI will detect and offer to install them automatically when you run that command. You only need Python to get started.

---

## Steps

### 1. Install pipx

`pipx` manages isolated environments for CLI tools and exposes their commands globally.

**macOS**
```bash
brew install pipx
pipx ensurepath
```

**Linux**
```bash
pip install --user pipx
pipx ensurepath
```

**Windows**
```powershell
pip install --user pipx
pipx ensurepath
```

After running `pipx ensurepath`, open a new terminal (or `source ~/.zshrc` / restart PowerShell) so the updated `PATH` takes effect.

---

### 2. Install origin-cli

**From PyPI** *(once published)*:
```bash
pipx install origin-cli
```

**From GitHub**:
```bash
pipx install git+https://github.com/pandaind/origin-cli.git
```

**For local development** — from the root of this repository:
```bash
pipx install --editable .
```

The `--editable` flag means changes to the source are reflected immediately without reinstalling.

---

### 3. Run setup

Bootstrap your machine with the required AI development tools:

```bash
origin setup
```

`origin setup` walks you through three steps interactively:

**Step 1 — Methodology**
```
Select your primary development methodology:
  [1] Spec Driven Development (SDD) - Architect-first workflow using Spec Kit
  [2] Agent Driven Development (ADD) - Agent-first workflow using Agent Forge

Enter your choice [1]:
```

**Step 2 — Execution Environment**
```
Select your execution environment:
  [1] CLI Toolchains - Global Node/Python packages (specify-cli, agent-forge-copilot)
  [2] IDE Native - Zero global dependencies (directly scaffolds rules into .github/.cursor)

Enter your choice [1]:
```

Based on your selection, it will orchestrate the installation of the required global tools or verify that your local environment is ready for native templating.

**Step 3 — Headroom-AI prompt compression** *(optional)*
```
Enable prompt compression via headroom-ai?
  (Wraps copilot + forge to compress file reads, tool outputs,
   and every LLM call. Typically 60-95% token reduction.) [Y/n]:
```

When enabled, `headroom wrap` intercepts every API call made by your tools
and compresses the full context window before it hits the model — including file reads,
tool outputs, and prior turns. Originals are cached locally; the model can retrieve
them on demand. No code changes required.

---

**Non-interactive flags — run fully silent:**

| Flag | Effect |
|------|--------|
| `--spec` / `--no-spec` | Force spec-driven or agent-driven mode |
| `--copilot` / `--no-copilot` | Install or skip GitHub Copilot CLI + Agent Forge |
| `--headroom` / `--no-headroom` | Enable or skip headroom-ai prompt compression |

Example — fully automated spec-driven setup with compression:
```bash
origin setup --spec --copilot --headroom
```

---

### 4. Verify

```bash
origin --help
```

---

## Uninstall

```bash
# 1. Remove all global components (Copilot CLI, Spec Kit, Headroom, etc.)
origin reset

# 2. Uninstall the Origin CLI itself
pipx uninstall origin-cli
```
