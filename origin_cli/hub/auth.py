import json
from pathlib import Path

CREDENTIALS_FILE = Path.home() / ".origin" / "hub_credentials.json"


def save_api_key(api_key: str) -> None:
    """Save the API key securely."""
    CREDENTIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
    CREDENTIALS_FILE.write_text(json.dumps({"api_key": api_key}))
    # Ensure it's only readable by the owner
    CREDENTIALS_FILE.chmod(0o600)


def get_api_key() -> str | None:
    """Read the API key."""
    if not CREDENTIALS_FILE.exists():
        return None
    try:
        data = json.loads(CREDENTIALS_FILE.read_text())
        return data.get("api_key")
    except Exception:
        return None


def delete_api_key() -> None:
    """Remove the API key."""
    if CREDENTIALS_FILE.exists():
        CREDENTIALS_FILE.unlink()
