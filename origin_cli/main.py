import typer
from origin_cli.commands.setup import setup_command
from origin_cli.commands.reset import reset_command
from origin_cli.commands.check import check_command
from origin_cli.commands.init import init_command
from origin_cli.commands.extension import app as extension_app
from origin_cli.commands.preset import app as preset_app
from origin_cli.commands.hub import app as hub_app

from origin_cli.commands.migrate import migrate_command

app = typer.Typer(help="Unified AI Orchestrator CLI")

app.command(name="setup")(setup_command)
app.command(name="reset")(reset_command)
app.command(name="check")(check_command)
app.command(name="init")(init_command)
app.command(name="migrate")(migrate_command)
app.add_typer(extension_app, name="extension", help="Manage Origin extensions")
app.add_typer(preset_app, name="preset", help="Manage Origin presets")
app.add_typer(hub_app, name="hub", help="Manage Origin hubs")

if __name__ == "__main__":
    app()
