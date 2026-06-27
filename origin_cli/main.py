import typer
from origin_cli.commands.setup import setup_command
from origin_cli.commands.init import init_command

app = typer.Typer(help="Unified AI Orchestrator CLI")

app.command(name="setup")(setup_command)
app.command(name="init")(init_command)

if __name__ == "__main__":
    app()
