import typer
from origin_cli.integrations import agent_forge, speckit
from origin_cli.integrations.prerequisites import ensure_node_npm, ensure_pipx

def setup_command(
    copilot: bool = typer.Option(None, "--copilot/--no-copilot", help="Install GitHub Copilot CLI and Agent Forge globally via npm"),
    spec: bool = typer.Option(None, "--spec/--no-spec", help="Install Spec Kit (specify-cli) for spec-driven development"),
    headroom: bool = typer.Option(None, "--headroom/--no-headroom", help="Enable prompt compression via headroom-ai (wraps copilot + forge on every LLM call)"),
):
    """
    Bootstraps your machine with the AI development dependencies.
    Acts as a global capabilities menu for origin CLI.
    """
    typer.secho("\nWelcome to Origin Setup! Let's bootstrap your machine dependencies.", fg=typer.colors.CYAN, bold=True)
    
    # ── Agent Forge & Spec Kit (Copilot Integrations) ────────────────────────
    typer.secho("\n1. GitHub Copilot & VS Code Integrations", fg=typer.colors.MAGENTA, bold=True)
    if copilot is None:
        typer.echo("   (Required if you plan to use GitHub Copilot or VS Code for any project)")
        copilot = typer.confirm("   Install Copilot toolchain?", default=True)

    if copilot:
        if spec is None:
            typer.secho("\n   Select your Copilot development mode:", fg=typer.colors.CYAN, bold=True)
            typer.echo("     [1] Spec-driven (SDD)  — Agent Forge + Spec Kit (recommended)")
            typer.echo("     [2] Agent-driven (ADD) — Agent Forge only\n")

            while True:
                choice = typer.prompt("   Enter your choice", default="1")
                if choice in ("1", "2"):
                    break
                typer.secho("     Please enter 1 or 2.", fg=typer.colors.RED)

            spec = choice == "1"

        typer.secho("\nChecking prerequisites for Copilot integrations...", fg=typer.colors.CYAN)
        ensure_node_npm()
        if spec:
            ensure_pipx()
            
        agent_forge.install()
        if spec:
            speckit.install()
    else:
        typer.secho("Skipping GitHub Copilot integrations.", fg=typer.colors.YELLOW)

    # ── Headroom prompt compression ─────────────────────────────────────────
    if headroom is None:
        typer.secho("\n2. Headroom AI Token Compression", fg=typer.colors.MAGENTA, bold=True)
        typer.echo("   Wraps Copilot/Forge to compress LLM tokens by 60-95%.")
        headroom = typer.confirm("   Install?", default=True)

    if headroom:
        from origin_cli.integrations import headroom as hr
        typer.secho("\nSetting up headroom-ai...", fg=typer.colors.CYAN)
        if not hr.is_installed():
            ensure_pipx()   # headroom-ai installs via pipx
            hr.install()
        else:
            typer.secho("  ✔ headroom-ai is already installed.", fg=typer.colors.GREEN)
        hr.wrap_agents()
    else:
        typer.secho("Skipping headroom-ai installation.", fg=typer.colors.YELLOW)

    typer.secho("\nSetup complete! Dependencies are installed.", fg=typer.colors.GREEN, bold=True)

