import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx

from origin_cli.hub.auth import get_api_key, get_hub_url

DEFAULT_HUB_URL = get_hub_url() or os.environ.get("ORIGIN_HUB_URL", "http://127.0.0.1:8000")


class HubAuthError(Exception):
    pass


class HubNotFoundError(Exception):
    pass


class HubServerError(Exception):
    pass


class HubClient:
    def __init__(self, base_url: str = DEFAULT_HUB_URL):
        self.base_url = base_url.rstrip("/")
        self.api_key = get_api_key()

    def _get_headers(self) -> Dict[str, str]:
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _handle_response(self, response: httpx.Response) -> Any:
        if response.status_code == 401:
            raise HubAuthError("Unauthorized. Please log in.")
        if response.status_code == 404:
            raise HubNotFoundError("Resource not found on Hub.")
        if response.status_code >= 500:
            raise HubServerError(f"Hub server error: {response.text}")
        if response.status_code >= 400:
            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text
            raise Exception(f"Hub Error ({response.status_code}): {detail}")
        
        # for downloading binary files, we won't call json()
        if response.headers.get("content-type") == "application/gzip":
            return response.content

        return response.json()

    def register_and_login(self, username: str, email: str) -> Dict[str, str]:
        """Call POST /auth/register to get a new API key."""
        with httpx.Client() as client:
            resp = client.post(
                f"{self.base_url}/auth/register",
                json={"username": username, "email": email}
            )
            return self._handle_response(resp)

    def whoami(self) -> Dict[str, Any]:
        with httpx.Client() as client:
            resp = client.get(f"{self.base_url}/auth/me", headers=self._get_headers())
            return self._handle_response(resp)

    def search(self, query: str = "", limit: int = 20) -> Dict[str, Any]:
        with httpx.Client() as client:
            resp = client.get(
                f"{self.base_url}/assets",
                params={"q": query, "limit": limit},
                headers=self._get_headers()
            )
            return self._handle_response(resp)

    def recommend(self, tech_tags: List[str], limit: int = 10) -> Dict[str, Any]:
        """Fetches asset recommendations based on tech tags."""
        with httpx.Client() as client:
            resp = client.get(
                f"{self.base_url}/assets/recommend",
                params={"tech": ",".join(tech_tags), "limit": limit},
                headers=self._get_headers()
            )
            return self._handle_response(resp)

    def publish(self, bundle_path: str, name: str, version: str) -> Dict[str, Any]:
        """Uploads an .originpkg file to the Hub."""
        with httpx.Client() as client:
            with open(bundle_path, "rb") as f:
                resp = client.post(
                    f"{self.base_url}/assets/{name}/{version}",
                    files={"file": (Path(bundle_path).name, f, "application/gzip")},
                    headers=self._get_headers(),
                    timeout=30.0  # Uploads might take time
                )
            return self._handle_response(resp)

    def get_asset(self, name: str) -> Dict[str, Any]:
        """Fetches metadata for a specific asset."""
        with httpx.Client() as client:
            resp = client.get(f"{self.base_url}/assets/{name}", headers=self._get_headers())
            return self._handle_response(resp)

    def download_bundle(self, name: str, version: str) -> bytes:
        """Downloads the .originpkg bundle."""
        with httpx.Client() as client:
            resp = client.get(
                f"{self.base_url}/assets/{name}/{version}/bundle",
                headers=self._get_headers(),
                timeout=60.0
            )
            return self._handle_response(resp)
