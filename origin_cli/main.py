import typer
from origin_cli.commands.setup import setup_command
from origin_cli.commands.init_project import init_project_command

app = typer.Typer(help="Unified AI Orchestrator CLI")

app.command(name="setup")(setup_command)
app.command(name="init-project")(init_project_command)

if __name__ == "__main__":
    app()
