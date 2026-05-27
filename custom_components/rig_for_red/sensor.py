from __future__ import annotations

from homeassistant.components.sensor import RestoreEntity, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import RigForRedCoordinator


async def async_setup_entry(
    _hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: RigForRedCoordinator = entry.runtime_data
    async_add_entities([RigForRedSensor(coordinator, entry)])


STATE_INACTIVE = "inactive"
STATE_ACTIVE_RED = "active_red"
STATE_DIMMING = "dimming"
STATE_RESTORING = "restoring"
STATE_RESTORED = "restored"


class RigForRedSensor(CoordinatorEntity, RestoreEntity, SensorEntity):
    _attr_has_entity_name = True
    _attr_translation_key = "state"

    def __init__(
        self,
        coordinator: RigForRedCoordinator,
        entry: ConfigEntry,
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_state"
        self._attr_should_poll = False

    def _compute_state(self) -> str:
        if not self.coordinator.is_active:
            return STATE_INACTIVE
        if self.coordinator.restoring:
            return STATE_RESTORING
        if self.coordinator.is_dimming:
            return STATE_DIMMING
        return STATE_ACTIVE_RED

    @property
    def state(self) -> str:
        return self._compute_state()

    @property
    def extra_state_attributes(self) -> dict:
        coordinator = self.coordinator
        return {
            "active_since": coordinator.active_since,
            "lights_active": coordinator.lights_active,
            "lights_tracked_off": coordinator.lights_tracked_off,
            "next_restore": coordinator.next_restore,
            "dim_step": coordinator.dim_step,
            "al_switches": coordinator.al_switches,
        }

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if (last_state := await self.async_get_last_state()) is not None:
            self._attr_native_value = last_state.state

    async def _handle_coordinator_update(self) -> None:
        self.async_write_ha_state()
