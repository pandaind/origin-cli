"""
Cross-platform prerequisite bootstrapper for origin setup.

Supports: macOS, Linux, Windows
"""

import shutil
import subprocess
import sys
import platform
import typer


def check_command(cmd: str) -> bool:
    """Return True if `cmd` is available on the system PATH."""
    return shutil.which(cmd) is not None


# ---------------------------------------------------------------------------
# pipx
# ---------------------------------------------------------------------------

def ensure_pipx() -> None:
    """
    Ensure pipx is installed. If missing, installs it via pip (which ships
    with Python) and runs `pipx ensurepath`.
    Works identically on Windows, Linux, and macOS.
    """
    if check_command("pipx"):
        typer.secho("  ✔ pipx is already installed.", fg=typer.colors.GREEN)
        return

    typer.secho("  ✖ pipx not found.", fg=typer.colors.YELLOW)
    confirmed = typer.confirm(
        "pipx is required to install specify-cli. Install it now via pip?",
        default=True,
    )
    if not confirmed:
        typer.secho(
            "Skipping pipx installation. You can install it manually with:\n"
            "    pip install --user pipx\n"
            "    pipx ensurepath",
            fg=typer.colors.YELLOW,
        )
        return

    typer.echo("Installing pipx via pip...")
    _run(
        [sys.executable, "-m", "pip", "install", "--user", "pipx"],
        error_msg="Failed to install pipx via pip.",
    )

    typer.echo("Running 'pipx ensurepath'...")
    _run(
        [sys.executable, "-m", "pipx", "ensurepath"],
        error_msg="pipx ensurepath failed.",
        required=False,
    )

    # After --user install on some systems the binary is in ~/.local/bin which
    # may not be in PATH yet for the current process. Try to locate it.
    if not check_command("pipx"):
        import os
        from pathlib import Path

        local_bin = Path.home() / ".local" / "bin"
        scripts_dir = Path(sys.prefix) / "Scripts"  # Windows venv path

        for candidate in (local_bin, scripts_dir):
            candidate_exe = candidate / ("pipx.exe" if sys.platform == "win32" else "pipx")
            if candidate_exe.exists():
                os.environ["PATH"] = str(candidate) + os.pathsep + os.environ.get("PATH", "")
                typer.secho(
                    f"  ✔ pipx installed at {candidate_exe}.\n"
                    "  ⚠  You may need to restart your shell for 'pipx' to be available globally.",
                    fg=typer.colors.YELLOW,
                )
                return

    if check_command("pipx"):
        typer.secho("  ✔ pipx installed successfully.", fg=typer.colors.GREEN)
    else:
        typer.secho(
            "  ✖ pipx installation succeeded but the binary was not found on PATH.\n"
            "  Please restart your shell and run 'origin setup' again.",
            fg=typer.colors.RED,
        )


# ---------------------------------------------------------------------------
# Node.js / npm
# ---------------------------------------------------------------------------

def ensure_node_npm() -> None:
    """
    Ensure node and npm are installed.
    Uses the appropriate method for the current OS:
      - macOS  : Homebrew  (installs Homebrew if needed)
      - Linux  : apt-get, dnf, yum, pacman, or zypper
      - Windows: winget    (falls back to a download URL for older Windows)
    """
    node_ok = check_command("node")
    npm_ok = check_command("npm")

    if node_ok and npm_ok:
        typer.secho("  ✔ node and npm are already installed.", fg=typer.colors.GREEN)
        return

    missing = []
    if not node_ok:
        missing.append("node")
    if not npm_ok:
        missing.append("npm")
    typer.secho(f"  ✖ Missing: {', '.join(missing)}", fg=typer.colors.YELLOW)

    os_name = platform.system()

    if os_name == "Darwin":
        _install_node_macos()
    elif os_name == "Linux":
        _install_node_linux()
    elif os_name == "Windows":
        _install_node_windows()
    else:
        typer.secho(
            f"  Unsupported platform '{os_name}'. Please install Node.js manually from https://nodejs.org",
            fg=typer.colors.RED,
        )


# ---------------------------------------------------------------------------
# macOS helpers
# ---------------------------------------------------------------------------

def _install_node_macos() -> None:
    if check_command("brew"):
        typer.echo("  Installing Node.js via Homebrew...")
        confirmed = typer.confirm("Run 'brew install node'?", default=True)
        if confirmed:
            _run(["brew", "install", "node"], error_msg="brew install node failed.")
            _verify_node()
    else:
        typer.secho("  Homebrew is not installed.", fg=typer.colors.YELLOW)
        confirmed = typer.confirm(
            "Homebrew is needed to install Node.js on macOS.\n"
            "Install Homebrew now? (Runs the official installer from https://brew.sh)",
            default=True,
        )
        if confirmed:
            typer.echo("  Installing Homebrew...")
            _run(
                [
                    "/bin/bash", "-c",
                    "curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash",
                ],
                error_msg="Homebrew installation failed.",
            )
            # After Homebrew install, brew may be in /opt/homebrew/bin (Apple Silicon) or /usr/local/bin (Intel)
            import os
            for brew_prefix in ("/opt/homebrew/bin", "/usr/local/bin"):
                if shutil.which(f"{brew_prefix}/brew") or shutil.which("brew") is None:
                    os.environ["PATH"] = brew_prefix + os.pathsep + os.environ.get("PATH", "")
                    break

            typer.echo("  Installing Node.js via Homebrew...")
            _run(["brew", "install", "node"], error_msg="brew install node failed.")
            _verify_node()
        else:
            typer.secho(
                "  Please install Homebrew manually (https://brew.sh) then run 'origin setup' again.",
                fg=typer.colors.YELLOW,
            )


# ---------------------------------------------------------------------------
# Linux helpers
# ---------------------------------------------------------------------------

def _install_node_linux() -> None:
    if check_command("apt-get"):
        pkg_manager = "apt-get"
        install_cmd = ["sudo", "apt-get", "install", "-y", "nodejs", "npm"]
    elif check_command("dnf"):
        pkg_manager = "dnf"
        install_cmd = ["sudo", "dnf", "install", "-y", "nodejs", "npm"]
    elif check_command("yum"):
        pkg_manager = "yum"
        install_cmd = ["sudo", "yum", "install", "-y", "nodejs", "npm"]
    elif check_command("pacman"):
        pkg_manager = "pacman"
        install_cmd = ["sudo", "pacman", "-S", "--noconfirm", "nodejs", "npm"]
    elif check_command("zypper"):
        pkg_manager = "zypper"
        install_cmd = ["sudo", "zypper", "install", "-y", "nodejs", "npm"]
    else:
        typer.secho(
            "  No supported package manager found (apt-get, dnf, yum, pacman, zypper).\n"
            "  Please install Node.js manually from https://nodejs.org",
            fg=typer.colors.RED,
        )
        return

    typer.echo(f"  Detected package manager: {pkg_manager}")
    confirmed = typer.confirm(
        f"Run '{' '.join(install_cmd)}'?",
        default=True,
    )
    if confirmed:
        _run(install_cmd, error_msg=f"{pkg_manager} install of nodejs/npm failed.")
        _verify_node()
    else:
        typer.secho(
            "  Skipping Node.js installation. Please install it manually from https://nodejs.org",
            fg=typer.colors.YELLOW,
        )


# ---------------------------------------------------------------------------
# Windows helpers
# ---------------------------------------------------------------------------

def _install_node_windows() -> None:
    if check_command("winget"):
        confirmed = typer.confirm(
            "Run 'winget install OpenJS.NodeJS' to install Node.js?",
            default=True,
        )
        if confirmed:
            _run(
                ["winget", "install", "--id", "OpenJS.NodeJS", "-e", "--silent"],
                error_msg="winget install of Node.js failed.",
            )
            _verify_node()
        else:
            typer.secho(
                "  Skipping Node.js installation. Download it from https://nodejs.org",
                fg=typer.colors.YELLOW,
            )
    else:
        typer.secho(
            "  winget is not available on this Windows version.\n"
            "  Please download and install Node.js manually from:\n"
            "    https://nodejs.org/en/download/",
            fg=typer.colors.YELLOW,
        )


# ---------------------------------------------------------------------------
# Shared utilities
# ---------------------------------------------------------------------------

def _verify_node() -> None:
    """Print a success or warning message after attempting node installation."""
    if check_command("node") and check_command("npm"):
        typer.secho("  ✔ node and npm installed successfully.", fg=typer.colors.GREEN)
    else:
        typer.secho(
            "  ⚠  node/npm installation may have succeeded but binaries are not on PATH yet.\n"
            "  You may need to restart your shell.",
            fg=typer.colors.YELLOW,
        )


def _run(cmd: list, error_msg: str, required: bool = True) -> None:
    """Run a subprocess command, printing a clear error on failure."""
    exe = shutil.which(cmd[0])
    if exe:
        cmd = [exe] + cmd[1:]
        
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        typer.secho(f"  ✖ {error_msg} (exit code {e.returncode})", fg=typer.colors.RED)
        if required:
            raise typer.Exit(code=e.returncode)
    except FileNotFoundError:
        typer.secho(
            f"  ✖ Command not found: '{cmd[0]}'. {error_msg}",
            fg=typer.colors.RED,
        )
        if required:
            raise typer.Exit(code=1)
