from __future__ import annotations

import aiohttp
from datetime import datetime, timedelta

class OAuth2Client:
    def __init__(self, session: aiohttp.ClientSession, client_id: str,
                 client_secret: str, auth_url: str, token_url: str,
                 scopes: list[str]) -> None:
        self._session = session
        self._client_id = client_id
        self._client_secret = client_secret
        self._auth_url = auth_url
        self._token_url = token_url
        self._scopes = scopes
        self._access_token: str | None = None
        self._expires_at: datetime | None = None

    async def _fetch_token(self) -> None:
        """Token abrufen; hier z.B. Client Credentials Flow einbauen."""
        payload = {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "scope": " ".join(self._scopes),
        }
        async with self._session.post(self._token_url, data=payload) as resp:
            data = await resp.json()
        # Felder an deinen OAuth-Provider anpassen
        self._access_token = data["access_token"]
        # Optional: echte expires_in nutzen
        expires_in = data.get("expires_in", 300)
        self._expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

    async def get_access_token(self) -> str:
        """Gültiges Access Token (JWT) liefern."""
        if not self._access_token or not self._expires_at or \
           self._expires_at <= datetime.utcnow():
            await self._fetch_token()
        return self._access_token
