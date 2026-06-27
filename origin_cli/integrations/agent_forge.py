import typer
from pathlib import Path
from origin_cli.utils import run_command
from origin_cli.constants import LEGISLATOR_AGENT_PROMPT

def install():
    """Install @github/copilot and @agent-forge-copilot/cli globally via npm."""
    typer.echo("Installing @github/copilot globally via npm (required by agent-forge)...")
    run_command(["npm", "install", "-g", "@github/copilot"])
    
    typer.echo("Installing @agent-forge-copilot/cli globally via npm...")
    run_command(["npm", "install", "-g", "@agent-forge-copilot/cli"])

def init():
    """Run forge init."""
    typer.echo("Authenticating GitHub Copilot CLI...")
    run_command(["copilot", "login"], check=False)
    
    typer.echo("Running 'forge init --mode analyze'...")
    run_command(["forge", "init", "--mode", "analyze"])

def generate_legislator_agent():
    """Create the @legislator persona file."""
    typer.echo("Generating @legislator agent prompt...")
    agents_dir = Path(".github/agents")
    agents_dir.mkdir(parents=True, exist_ok=True)
    legislator_agent_file = agents_dir / "legislator.agent.md"
    legislator_agent_file.write_text(LEGISLATOR_AGENT_PROMPT)
