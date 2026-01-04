from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_NAME, CONF_HOST
from homeassistant.helpers import config_validation as cv
from .const import (
    DOMAIN,
    CONF_IP_ADDRESS,
    CONF_LOGIN_HASH,
)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default="BSC-Pro EG122SN Restart"): str,
        vol.Required(CONF_IP_ADDRESS, description={'suggested_value': '192.168.1.100'}): cv.string,
        vol.Required(CONF_LOGIN_HASH, description={'suggested_value': '6691F8B01DBF3E770D51492F3AAD71AA30193397E20607A695639E866E31CCAE'}): cv.string,
    }
)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for BSC-Pro Gateway EG122SN."""

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Test Connection
            if not await self._test_connection(user_input):
                return self.async_show_form(
                    step_id="user",
                    data_schema=DATA_SCHEMA,
                    errors={"base": "connection"}
                )
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input,
            )
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)

    async def _test_connection(self, user_input):
        # Hier Connection-Test implementieren
        return True
