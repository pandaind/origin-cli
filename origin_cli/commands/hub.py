from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from origin_cli.hub.auth import delete_api_key, save_api_key, save_hub_url
from origin_cli.hub.client import HubClient, HubAuthError, HubNotFoundError
from origin_cli.hub.packager import create_asset_bundle, PackagerError
from origin_cli.hub.installer import install_asset_bundle, InstallerError

app = typer.Typer(help="Publish and discover assets on the Origin Hub")
console = Console()


@app.command(name="set-url")
def set_url(url: str = typer.Argument(..., help="The full URL of the Hub Registry server")):
    """Configure a persistent custom Hub URL."""
    url = url.rstrip("/")
    if not url.startswith("http"):
        typer.secho("URL must start with http:// or https://", fg=typer.colors.RED)
        raise typer.Exit(1)
        
    save_hub_url(url)
    typer.secho(f"Hub URL permanently set to: {url}", fg=typer.colors.GREEN)


@app.command()
def login(
    username: str = typer.Option(..., prompt=True),
    email: str = typer.Option(..., prompt=True)
):
    """Register and authenticate with the Origin Hub."""
    client = HubClient()
    try:
        with console.status(f"Registering {username}..."):
            response = client.register_and_login(username, email)
        
        api_key = response.get("api_key")
        if not api_key:
            typer.secho("Failed to receive API key from server.", fg=typer.colors.RED)
            raise typer.Exit(1)
            
        save_api_key(api_key)
        typer.secho(f"Successfully logged in as {username}!", fg=typer.colors.GREEN)
        
    except Exception as e:
        typer.secho(f"Login failed: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)


@app.command()
def logout():
    """Remove stored Hub credentials."""
    delete_api_key()
    typer.secho("Logged out.", fg=typer.colors.GREEN)


@app.command()
def whoami():
    """Show the currently authenticated user."""
    client = HubClient()
    try:
        user = client.whoami()
        typer.secho(f"Logged in as: {user.get('username')} ({user.get('email')})", fg=typer.colors.CYAN)
    except HubAuthError as e:
        typer.secho(str(e), fg=typer.colors.RED)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)


@app.command()
def search(query: str = typer.Argument(default="")):
    """Search the Hub for assets."""
    client = HubClient()
    try:
        results = client.search(query=query)
        items = results.get("items", [])
        
        if not items:
            typer.secho(f"No assets found matching '{query}'.", fg=typer.colors.YELLOW)
            return

        table = Table(title=f"Hub Search Results" if not query else f"Search Results for '{query}'")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Type", style="magenta")
        table.add_column("Description", style="white")
        table.add_column("Author", style="blue")
        table.add_column("Downloads", justify="right", style="green")

        for item in items:
            table.add_row(
                item.get("name"),
                item.get("type"),
                (item.get("description") or "")[:50] + ("..." if len(item.get("description") or "") > 50 else ""),
                item.get("author") or "unknown",
                str(item.get("download_count", 0))
            )
            
        console.print(table)
        
    except Exception as e:
        typer.secho(f"Search failed: {e}", fg=typer.colors.RED)


@app.command()
def publish(path: str = typer.Argument(..., help="Path to the directory containing hub-manifest.json")):
    """Package and publish an asset to the Hub."""
    source_dir = Path(path).resolve()
    
    try:
        # 1. Package
        typer.echo(f"Packaging {source_dir}...")
        bundle_path, manifest = create_asset_bundle(source_dir)
        name = manifest["name"]
        version = manifest["version"]
        
        # 2. Upload
        client = HubClient()
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description=f"Publishing {name} v{version}...", total=None)
            client.publish(str(bundle_path), name, version)
            
        typer.secho(f"✔ Successfully published {name} v{version}!", fg=typer.colors.GREEN)
        
    except PackagerError as e:
        typer.secho(f"Packaging Error: {e}", fg=typer.colors.RED)
    except HubAuthError as e:
        typer.secho(str(e), fg=typer.colors.RED)
    except Exception as e:
        typer.secho(f"Publish failed: {e}", fg=typer.colors.RED)
    finally:
        # Cleanup temp bundle
        if 'bundle_path' in locals() and bundle_path.exists():
            bundle_path.unlink()


@app.command()
def install(
    name: str = typer.Argument(..., help="Name of the asset (e.g. forge-frontend-expert)"),
    version: Optional[str] = typer.Option(None, help="Specific version to install (defaults to latest)")
):
    """Download and install an asset from the Hub."""
    client = HubClient()
    
    try:
        # 1. Resolve version
        if not version:
            with console.status(f"Fetching metadata for {name}..."):
                meta = client.get_asset(name)
                latest = meta.get("latest_version")
                if not latest:
                    typer.secho(f"Asset '{name}' has no active versions.", fg=typer.colors.RED)
                    raise typer.Exit(1)
                version = latest.get("version")
        
        # 2. Download
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description=f"Downloading {name} v{version}...", total=None)
            bundle_bytes = client.download_bundle(name, version)
            
        # 3. Install
        typer.echo(f"Installing {name}...")
        install_asset_bundle(bundle_bytes, target_project_dir=Path.cwd())
        
        typer.secho(f"✔ Successfully installed {name} v{version}!", fg=typer.colors.GREEN)
        
    except HubNotFoundError:
        typer.secho(f"Asset '{name}' not found on the Hub.", fg=typer.colors.RED)
    except InstallerError as e:
        typer.secho(f"Installation Error: {e}", fg=typer.colors.RED)
    except Exception as e:
        typer.secho(f"Install failed: {e}", fg=typer.colors.RED)


@app.command()
def discover():
    """Scan the project and auto-install recommended assets."""
    from origin_cli.hub.discovery import detect_tech_stack
    
    project_dir = Path.cwd()
    
    with console.status("Scanning project tech stack..."):
        tech_tags = detect_tech_stack(project_dir)
        
    if not tech_tags:
        typer.secho("No recognizable tech stack found. Cannot make recommendations.", fg=typer.colors.YELLOW)
        return
        
    typer.secho(f"Detected stack: {', '.join(tech_tags)}", fg=typer.colors.CYAN, bold=True)
    
    client = HubClient()
    with console.status("Fetching recommendations..."):
        try:
            results = client.recommend(tech_tags)
        except Exception as e:
            typer.secho(f"Failed to fetch recommendations: {e}", fg=typer.colors.RED)
            return
            
    items = results.get("items", [])
    if not items:
        typer.secho("No matching assets found on the Hub for your stack.", fg=typer.colors.YELLOW)
        return
        
    table = Table(title="Recommended Assets")
    table.add_column("No.", style="bold cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Type", style="white")
    table.add_column("Description", style="blue")
    
    for idx, item in enumerate(items, 1):
        desc = (item.get("description") or "")[:50]
        table.add_row(str(idx), item.get("name"), item.get("type"), desc)
        
    console.print(table)
    typer.echo()
    
    choices = typer.prompt("Enter asset numbers to install (comma-separated), or press Enter to skip", default="")
    if not choices.strip():
        typer.secho("Skipping installation.", fg=typer.colors.YELLOW)
        return
        
    selected_indices = []
    for c in choices.split(","):
        c = c.strip()
        if c.isdigit():
            idx = int(c) - 1
            if 0 <= idx < len(items):
                selected_indices.append(idx)
                
    if not selected_indices:
        typer.secho("No valid selections.", fg=typer.colors.YELLOW)
        return
        
    for idx in selected_indices:
        asset = items[idx]
        name = asset["name"]
        version = asset.get("latest_version", {}).get("version")
        
        if not version:
            typer.secho(f"Asset '{name}' has no active version. Skipping.", fg=typer.colors.RED)
            continue
            
        try:
            typer.echo(f"\nInstalling [cyan]{name}[/cyan]...")
            bundle_bytes = client.download_bundle(name, version)
            install_asset_bundle(bundle_bytes, target_project_dir=project_dir)
            typer.secho(f"✔ Successfully installed {name}", fg=typer.colors.GREEN)
        except Exception as e:
            typer.secho(f"Failed to install {name}: {e}", fg=typer.colors.RED)

