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

def install_ide():
    """
    Copies Agent Forge .agent.md templates directly into the user's global Copilot configuration.
    Validates YAML frontmatter on all copied templates.
    """
    import shutil
    import re
    
    source_path = Path("/Users/cpanda/OSS/agent-forge/src/cli")
    if not source_path.exists():
        typer.secho(f"Error: Source path {source_path} does not exist.", fg=typer.colors.RED)
        return
        
    copilot_agents_dir = Path.home() / ".copilot" / "agents"
    copilot_prompts_dir = Path.home() / ".copilot" / "prompts"
    
    copilot_agents_dir.mkdir(parents=True, exist_ok=True)
    copilot_prompts_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Copy agent templates
    copied_count = 0
    valid_count = 0
    typer.echo("Copying Agent Forge templates to global ~/.copilot/agents/...")
    
    for agent_file in source_path.rglob("*.agent.md"):
        dest_file = copilot_agents_dir / agent_file.name
        shutil.copy2(agent_file, dest_file)
        copied_count += 1
        
        # 2. Validate YAML frontmatter
        content = dest_file.read_text()
        frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            # check if it contains name: "..." or name: something
            if re.search(r"^name:\s*.+", frontmatter, re.MULTILINE):
                valid_count += 1
            else:
                typer.secho(f"Warning: {agent_file.name} is missing a 'name:' field in its frontmatter.", fg=typer.colors.YELLOW)
        else:
            typer.secho(f"Warning: {agent_file.name} is missing valid YAML frontmatter.", fg=typer.colors.YELLOW)
            
    typer.secho(f"Copied {copied_count} templates ({valid_count} validated).", fg=typer.colors.GREEN)
    
    # 3. Generate global slash command prompt
    forge_setup_prompt = copilot_prompts_dir / "forge-setup.prompt.md"
    prompt_content = (
        "---\n"
        "name: forge-setup\n"
        "description: Setup Agent Forge configurations for this project\n"
        "agent: forge-brownfield-orchestrator\n"
        "---\n"
        "Please generate the complete Agent Forge setup for this repository.\n"
    )
    forge_setup_prompt.write_text(prompt_content)
    typer.secho(f"Created global slash command at ~/.copilot/prompts/forge-setup.prompt.md", fg=typer.colors.GREEN)
    typer.secho("To use: Open VS Code Copilot Chat and type '/forge-setup'.", fg=typer.colors.CYAN, bold=True)
