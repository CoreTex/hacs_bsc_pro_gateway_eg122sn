from __future__ import annotations

import aiohttp
import asyncio
from typing import Dict, Any

class BSCProClient:
    def __init__(self, session: aiohttp.ClientSession, base_url: str, login_hash: str):
        self._session = session
        self._base_url = base_url.rstrip('/')
        self._login_hash = login_hash
        self._auth_token: str | None = None

    async def login(self) -> bool:
        """Erster Call: Login mit exaktem Header/Payload."""
        url = f"{self._base_url}{LOGIN_ENDPOINT}"

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'text/plain',
            'Cookie': 'lang=en',
            'DNT': '1',
            'Origin': self._base_url,
            'Pragma': 'no-cache',
            'Referer': f"{self._base_url}/login",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
            # Initial X-Auth-Token aus Config oder leer lassen
            'X-Auth-Token': '',  
        }

        payload = self._login_hash  # Der Hex-String

        try:
            async with self._session.post(url, headers=headers, data=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    self._auth_token = data.get('token')
                    return True
        except:
            pass
        return False

    async def restart(self) -> bool:
        """Zweiter Call: Restart mit erhaltenem JWT Token."""
        if not self._auth_token:
            return False

        url = f"{self._base_url}{RESTART_ENDPOINT}"

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Cookie': 'lang=en',
            'DNT': '1',
            'Origin': self._base_url,
            'Pragma': 'no-cache',
            'Referer': f"{self._base_url}/system/status",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
            'X-Auth-Token': self._auth_token,  # JWT aus Login
        }

        try:
            async with self._session.post(url, headers=headers) as resp:
                return resp.status in (200, 204)
        except:
            return False

    async def close(self):
        if self._session:
            await self._session.close()
