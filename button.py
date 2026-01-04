from __future__ import annotations

import aiohttp
from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import (
    DOMAIN,
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_AUTH_URL,
    CONF_TOKEN_URL,
    CONF_API_BASE_URL,
    CONF_DEVICE_ID,
    OAUTH2_SCOPES,
)
from .oauth_client import OAuth2Client

async def async_setup_entry(
    hass: HomeAssistant,
    entry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup from config entry."""
    data = entry.data
    session = aiohttp.ClientSession()

    oauth_client = OAuth2Client(
        session=session,
        client_id=data[CONF_CLIENT_ID],
        client_secret=data[CONF_CLIENT_SECRET],
        auth_url=data[CONF_AUTH_URL],
        token_url=data[CONF_TOKEN_URL],
        scopes=OAUTH2_SCOPES,
    )

    button = BSCProGatewayButton(
        hass=hass,
        name=entry.title,
        oauth_client=oauth_client,
        api_base_url=data[CONF_API_BASE_URL],
        device_id=data[CONF_DEVICE_ID],
    )

    async_add_entities([button])

class BSCProGatewayButton(ButtonEntity):
    """Button for BSC-Pro Gateway EG122SN restart."""

    _attr_has_entity_name = True
    _attr_name = "restart device"

    def __init__(
        self,
        hass: HomeAssistant,
        name: str,
        oauth_client: OAuth2Client,
        api_base_url: str,
        device_id: str,
    ) -> None:
        self._hass = hass
        self._attr_unique_id = f"bsc_pro_gateway_eg122sn_restart_{device_id}"
        self._oauth_client = oauth_client
        self._api_base_url = api_base_url.rstrip("/")
        self._device_id = device_id

    async def async_press(self) -> None:
        """Handle button press."""
        token = await self._oauth_client.get_access_token()
        # Hier deine konkrete Business-Logik / URL einfügen:
        # Beispiel: POST https://api.bsc-pro.com/devices/<id>/restart
        url = f"{self._api_base_url}/devices/{self._device_id}/restart"

        headers = {
            "Authorization": f"Bearer {token}",  # JWT-Token
            "Content-Type": "application/json",
        }

        # Optional: Body anpassen
        payload = {
            "reason": "manual_restart_from_home_assistant"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                # Bei Bedarf Fehlerbehandlung / Logging ergänzen
                _ = await resp.text()
