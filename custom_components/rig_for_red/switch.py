from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import RigForRedCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: RigForRedCoordinator = entry.runtime_data
    async_add_entities([RigForRedSwitch(coordinator, entry)])


class RigForRedSwitch(CoordinatorEntity, SwitchEntity):

    _attr_has_entity_name = True
    _attr_translation_key = "rig_for_red"

    def __init__(
        self,
        coordinator: RigForRedCoordinator,
        entry: ConfigEntry,
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = entry.entry_id

    @property
    def icon(self) -> str:
        return "mdi:submarine" if self.is_on else "mdi:lighthouse-on"

    @property
    def is_on(self) -> bool:
        return self.coordinator.is_active

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.async_activate()

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_restore()
