from __future__ import annotations

import aiohttp
from homeassistant.components.button import ButtonEntity
from homeassistant.components.persistent_notification import async_create
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import (
    DOMAIN,
    CONF_IP_ADDRESS,
    CONF_LOGIN_HASH,
    DEFAULT_PORT,
    LOGIN_ENDPOINT,
    RESTART_ENDPOINT,
)
from .bsc_client import BSCProClient

async def async_setup_entry(
    hass: HomeAssistant,
    entry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    data = entry.data
    session = aiohttp.ClientSession()

    button = BSCProRestartButton(
        hass=hass,
        name=entry.title,
        ip_address=data[CONF_IP_ADDRESS],
        login_hash=data[CONF_LOGIN_HASH],
        session=session,
    )
    async_add_entities([button])

class BSCProRestartButton(ButtonEntity):
    """Button für BSC-Pro EG122SN Restart (Login → JWT → Restart)."""

    _attr_has_entity_name = True
    _attr_name = "restart EG122SN"

    def __init__(self, hass: HomeAssistant, name: str, ip_address: str, login_hash: str, session: aiohttp.ClientSession):
        self._hass = hass
        self._attr_unique_id = f"bsc_eg122sn_restart_{ip_address.replace('.', '_')}"
        self._ip_address = ip_address
        self._login_hash = login_hash
        self._session = session
        self._client: BSCProClient | None = None

    async def async_added_to_hass(self) -> None:
        self._client = BSCProClient(
            session=self._session,
            base_url=f"http://{self._ip_address}",
            login_hash=self._login_hash,
        )

    async def async_press(self) -> None:
        """1. Login → JWT Token, 2. Restart Call."""
        if not self._client:
            return

        # Schritt 1: Login
        if not await self._client.login():
            async_create(
                self._hass,"Login fehlgeschlagen", title="BSC-Pro EG122SN"
            )
            return

        # Schritt 2: Restart mit JWT
        if await self._client.restart():
            async_create(
                self._hass,"EG122SN Restart ausgeführt", title="✅ Erfolg"
            )
        else:
            async_create(
                self._hass,"Restart fehlgeschlagen", title="❌ Fehler"
            )

    async def async_will_remove_from_hass(self) -> None:
        if self._client:
            await self._client.close()
