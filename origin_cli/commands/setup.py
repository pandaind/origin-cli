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
    """
    typer.secho("\nWelcome to Origin Setup! Let's bootstrap your machine dependencies.", fg=typer.colors.CYAN, bold=True)
    
    # ── Workflow Selection ───────────────────────────────────────────────
    if spec is None:
        typer.secho("\nSelect your primary development mode:", fg=typer.colors.CYAN, bold=True)
        typer.echo("  [1] Spec-driven (SDD)  — Full Agent Forge + Spec Kit orchestration")
        typer.echo("  [2] Agent-driven (ADD) — Agent orchestration only\n")

        while True:
            choice = typer.prompt("Enter your choice", default="1")
            if choice in ("1", "2"):
                break
            typer.secho("  Please enter 1 or 2.", fg=typer.colors.RED)

        spec = choice == "1"

    if spec:
        typer.secho("\nMode: Spec-driven (SDD)", fg=typer.colors.GREEN)
        typer.secho("Checking prerequisites for SDD...", fg=typer.colors.CYAN)
        ensure_node_npm()
        ensure_pipx()
        agent_forge.install()
        speckit.install()
    else:
        typer.secho("\nMode: Agent-driven (ADD)", fg=typer.colors.GREEN)
        typer.secho("\nSelect your ADD workflow:", fg=typer.colors.CYAN, bold=True)
        typer.echo("  [1] agent-forge CLI  (Requires global npm installation)")
        typer.echo("  [2] ide-only         (For Claude/Cursor - no global installation needed)\n")
        
        while True:
            add_choice = typer.prompt("Enter your choice", default="2")
            if add_choice in ("1", "2"):
                break
            typer.secho("  Please enter 1 or 2.", fg=typer.colors.RED)
            
        if add_choice == "1":
            typer.secho("\nChecking prerequisites for agent-forge CLI...", fg=typer.colors.CYAN)
            ensure_node_npm()
            agent_forge.install()
        else:
            typer.secho("\n✔ No global dependencies required for ide-only ADD workflow.", fg=typer.colors.GREEN)

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

