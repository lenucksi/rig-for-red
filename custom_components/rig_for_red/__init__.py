import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, VERSION
from .coordinator import RigForRedCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor", "switch"]


async def async_trigger_rig(coordinator):
    async def handler(_call):
        await coordinator.async_activate()

    return handler


async def async_restore_lights(coordinator):
    async def handler(_call):
        await coordinator.async_restore()

    return handler


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.info("Setting up Rig-for-Red integration (version %s)", VERSION)
    coordinator = RigForRedCoordinator(hass, entry)
    await coordinator.async_setup()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    hass.services.async_register(DOMAIN, "trigger_rig", await async_trigger_rig(coordinator))
    hass.services.async_register(DOMAIN, "restore_lights", await async_restore_lights(coordinator))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    await coordinator.async_unload()
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    hass.services.async_remove(DOMAIN, "trigger_rig")
    hass.services.async_remove(DOMAIN, "restore_lights")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
