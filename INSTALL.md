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

You will be prompted to choose a development mode:

```
Select your development mode:
  [1] Spec-driven  — Agent Forge + Spec Kit (recommended for full workflows)
  [2] Agent-driven — Agent Forge only (no Spec Kit)

Enter your choice [1]:
```

`origin setup` will then automatically detect and install any missing prerequisites
(`node`, `npm`, and `pipx` if not already present) for the selected mode.

**Non-interactive flags:**

| Flag | Effect |
|------|--------|
| `--spec` | Force spec-driven mode (no prompt) |
| `--no-spec` | Force agent-driven mode (no prompt) |
| `--copilot` | Always install GitHub Copilot CLI + Agent Forge |
| `--no-copilot` | Skip GitHub Copilot CLI + Agent Forge install |

---

### 4. Verify

```bash
origin --help
```

---

## Uninstall

```bash
pipx uninstall origin-cli
```
