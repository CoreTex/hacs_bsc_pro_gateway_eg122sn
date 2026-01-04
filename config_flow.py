from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_NAME
from .const import (
    DOMAIN,
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_AUTH_URL,
    CONF_TOKEN_URL,
    CONF_API_BASE_URL,
    CONF_DEVICE_ID,
)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default="BSC-Pro Gateway EG122SN Restart"): str,
        vol.Required(CONF_CLIENT_ID): str,
        vol.Required(CONF_CLIENT_SECRET): str,
        vol.Required(CONF_AUTH_URL): str,
        vol.Required(CONF_TOKEN_URL): str,
        vol.Required(CONF_API_BASE_URL): str,
        vol.Required(CONF_DEVICE_ID): str,
    }
)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for BSC-Pro Gateway EG122SN."""

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input,
            )

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)
