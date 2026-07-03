import typer
from pathlib import Path
from origin_cli.utils import run_command

def install():
    """Install @github/copilot and @agent-forge-copilot/cli globally via npm."""
    typer.echo("Installing @github/copilot globally via npm (required by agent-forge)...")
    run_command(["npm", "install", "-g", "@github/copilot"])
    
    typer.echo("Installing @agent-forge-copilot/cli globally via npm...")
    run_command(["npm", "install", "-g", "@agent-forge-copilot/cli"])

def uninstall():
    """Uninstall global npm dependencies."""
    typer.echo("Uninstalling @github/copilot and @agent-forge-copilot/cli...")
    run_command(["npm", "uninstall", "-g", "@github/copilot", "@agent-forge-copilot/cli"], check=False)

def init():
    """Run forge init."""
    typer.echo("Authenticating GitHub Copilot CLI...")
    run_command(["copilot", "login"], check=False)
    
    typer.echo("Running 'forge init --mode analyze'...")
    run_command(["forge", "init", "--mode", "analyze"])

def init_ide():
    """
    Copies Agent Forge .agent.md templates into the user's global Copilot configuration.
    Copies Agent Forge entrypoint prompts into the local project's .github/prompts directory.
    Validates YAML frontmatter on all copied templates.
    """
    import shutil
    import re
    
    source_agents_path = Path(__file__).resolve().parent.parent / "templates" / "agents"
    source_prompts_path = Path(__file__).resolve().parent.parent / "templates" / "prompts"
    
    if not source_agents_path.exists():
        typer.secho(f"Error: Templates path {source_agents_path} does not exist.", fg=typer.colors.RED)
        return
        
    copilot_agents_dir = Path.home() / ".copilot" / "agents"
    copilot_agents_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Copy agent templates
    copied_count = 0
    valid_count = 0
    typer.echo("Copying Agent Forge templates to global ~/.copilot/agents/...")
    
    for agent_file in source_agents_path.rglob("*.agent.md"):
        dest_file = copilot_agents_dir / agent_file.name
        shutil.copy2(agent_file, dest_file)
        copied_count += 1
        
        # 2. Validate YAML frontmatter
        content = dest_file.read_text(encoding="utf-8")
        frontmatter_match = re.match(r"^---\r?\n(.*?)\r?\n---", content, re.DOTALL)
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
    
    # 3. Copy local slash command prompts
    local_prompts_dir = Path(".github/prompts")
    local_prompts_dir.mkdir(parents=True, exist_ok=True)
    
    copied_prompts = 0
    if source_prompts_path.exists():
        allowed_prompts = ["forge-create.prompt.md", "forge-analyze.prompt.md"]
        for prompt_file in source_prompts_path.rglob("*.prompt.md"):
            if prompt_file.name in allowed_prompts:
                dest_file = local_prompts_dir / prompt_file.name
                shutil.copy2(prompt_file, dest_file)
                copied_prompts += 1
            
    typer.secho(f"Copied {copied_prompts} entrypoint slash commands to .github/prompts/", fg=typer.colors.GREEN)
    typer.secho("To use: Open VS Code Copilot Chat and type '/forge-create' or '/forge-analyze'.", fg=typer.colors.CYAN, bold=True)
