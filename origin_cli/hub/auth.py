import json
from pathlib import Path

CREDENTIALS_FILE = Path.home() / ".origin" / "hub_credentials.json"


def save_api_key(api_key: str) -> None:
    """Save the API key securely."""
    CREDENTIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {}
    if CREDENTIALS_FILE.exists():
        try:
            data = json.loads(CREDENTIALS_FILE.read_text())
        except Exception:
            pass
    data["api_key"] = api_key
    CREDENTIALS_FILE.write_text(json.dumps(data))
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
        try:
            data = json.loads(CREDENTIALS_FILE.read_text())
            if "api_key" in data:
                del data["api_key"]
                CREDENTIALS_FILE.write_text(json.dumps(data))
        except Exception:
            CREDENTIALS_FILE.unlink()


def save_hub_url(url: str) -> None:
    """Save the custom Hub URL."""
    CREDENTIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {}
    if CREDENTIALS_FILE.exists():
        try:
            data = json.loads(CREDENTIALS_FILE.read_text())
        except Exception:
            pass
    data["hub_url"] = url
    CREDENTIALS_FILE.write_text(json.dumps(data))


def get_hub_url() -> str | None:
    """Read the custom Hub URL."""
    if not CREDENTIALS_FILE.exists():
        return None
    try:
        data = json.loads(CREDENTIALS_FILE.read_text())
        return data.get("hub_url")
    except Exception:
        return None
