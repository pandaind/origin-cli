"""
origin check — Validate .agent.md, .instructions.md, and .prompt.md files.
Designed to work as a CI/CD step in GitHub Actions (exits 1 on failure).
"""
import sys
import re
import typer
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.table import Table

app_console = Console()


def check_command(
    path: Optional[Path] = typer.Argument(
        None,
        help="Directory to check. Defaults to current working directory.",
        exists=False,
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        "-s",
        help="Fail on warnings in addition to errors.",
    ),
):
    """
    Validate Agent Forge files (.agent.md, .instructions.md, .prompt.md).
    Exits with code 1 if any validation errors are found.
    """
    root = Path(path) if path else Path.cwd()

    if not root.exists():
        typer.secho(f"Path does not exist: {root}", fg=typer.colors.RED)
        raise typer.Exit(1)

    patterns = ["**/*.agent.md", "**/*.instructions.md", "**/*.prompt.md"]
    ignore_dirs = {".venv", "node_modules", ".git", "__pycache__"}

    files = []
    for pattern in patterns:
        for f in root.rglob(pattern.lstrip("**/")):
            # Skip ignored directories
            if any(part in ignore_dirs for part in f.parts):
                continue
            files.append(f)

    if not files:
        typer.secho("No Agent Forge files found to validate.", fg=typer.colors.YELLOW)
        raise typer.Exit(0)

    table = Table(title=f"Origin Check — {len(files)} file(s)", show_lines=True)
    table.add_column("File", style="cyan", no_wrap=False)
    table.add_column("Status", justify="center")
    table.add_column("Issues", style="yellow")

    errors = 0
    warnings = 0
    seen_names: dict[str, str] = {}  # name -> first file that defined it

    for file in sorted(files):
        rel = file.relative_to(root)
        content = file.read_text(encoding="utf-8")
        issues = []

        # 1. Check for frontmatter
        fm_match = re.match(r"^---\r?\n(.*?)\r?\n---", content, re.DOTALL)
        if not fm_match:
            issues.append(("ERROR", "Missing YAML frontmatter (--- block)"))
        else:
            fm = fm_match.group(1)

            # 2. Required: name field
            name_match = re.search(r"^name:\s*(.+)", fm, re.MULTILINE)
            if not name_match:
                issues.append(("ERROR", "Missing required 'name:' field in frontmatter"))
            else:
                name_val = name_match.group(1).strip().strip("\"'")
                # 3. Check for duplicate slash command names across prompt files
                if file.name.endswith(".prompt.md"):
                    if name_val in seen_names:
                        issues.append(("ERROR", f"Duplicate name '{name_val}' (also in {seen_names[name_val]})"))
                    else:
                        seen_names[name_val] = str(rel)

            # 4. Required: description field
            if not re.search(r"^description:\s*.+", fm, re.MULTILINE):
                issues.append(("WARN", "Missing 'description:' field in frontmatter"))

            # 5. Validate 'model' field if present
            model_match = re.search(r"^model:\s*(.+)", fm, re.MULTILINE)
            if model_match:
                model_val = model_match.group(1).strip().strip("\"'")
                valid_models = {
                    "gpt-4", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo",
                    "claude-3-5-sonnet", "claude-3-opus", "claude-3-haiku",
                    "gemini-2.0-flash", "gemini-1.5-pro",
                    "o1", "o3-mini",
                }
                if model_val not in valid_models:
                    issues.append(("WARN", f"Unrecognized model '{model_val}'"))

        # Determine status
        has_errors = any(lvl == "ERROR" for lvl, _ in issues)
        has_warnings = any(lvl == "WARN" for lvl, _ in issues)

        if has_errors:
            errors += 1
            status = "[red]✖ ERROR[/red]"
        elif has_warnings:
            warnings += 1
            status = "[yellow]⚠ WARN[/yellow]"
        else:
            status = "[green]✔ OK[/green]"

        issue_text = "\n".join(f"[{lvl}] {msg}" for lvl, msg in issues) if issues else "—"
        table.add_row(str(rel), status, issue_text)

    app_console.print(table)

    total_failures = errors + (warnings if strict else 0)
    if total_failures > 0:
        typer.secho(
            f"\n✖ {errors} error(s), {warnings} warning(s). Check failed.",
            fg=typer.colors.RED, bold=True
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"\n✔ {len(files)} file(s) validated successfully. {warnings} warning(s).",
            fg=typer.colors.GREEN, bold=True
        )
