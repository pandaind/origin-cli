import typer
from origin_cli.integrations import agent_forge, speckit
from origin_cli.integrations.prerequisites import ensure_node_npm, ensure_pipx

def setup_command(
    copilot: bool = typer.Option(None, "--copilot/--no-copilot", help="Install GitHub Copilot CLI and Agent Forge globally via npm"),
    headroom: bool = typer.Option(None, "--headroom/--no-headroom", help="Enable prompt compression via headroom-ai (wraps copilot + forge on every LLM call)"),
):
    """
    Bootstraps your machine with the AI development dependencies.
    Acts as a global capabilities menu for origin CLI.
    """
    typer.secho("\nWelcome to Origin Setup! Let's bootstrap your machine dependencies.", fg=typer.colors.CYAN, bold=True)
    
    # ── Agent Forge & Spec Kit (Copilot Integrations) ────────────────────────
    if copilot is None:
        typer.secho("\n1. GitHub Copilot & VS Code Integrations", fg=typer.colors.MAGENTA, bold=True)
        typer.echo("   Installs the Agent Forge (npm) and Spec Kit (pipx) CLIs globally.")
        typer.echo("   (Required if you plan to use GitHub Copilot or VS Code for any project)")
        copilot = typer.confirm("   Install?", default=True)

    if copilot:
        typer.secho("\nChecking prerequisites for Copilot integrations...", fg=typer.colors.CYAN)
        ensure_node_npm()
        ensure_pipx()
        agent_forge.install()
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

