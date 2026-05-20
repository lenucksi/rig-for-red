---
id: TASK-15
title: switch.py implementieren
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 20:05'
updated_date: '2026-05-20 20:38'
labels: []
milestone: M4 - Switch Entity und Services
dependencies:
  - TASK-8
priority: high
ordinal: 15000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
RigForRedSwitch Entity als Brücke zwischen HA UI und Coordinator implementieren.

Datei: custom_components/rig_for_red/switch.py

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN
from .coordinator import RigForRedCoordinator

class RigForRedSwitch(CoordinatorEntity[RigForRedCoordinator], SwitchEntity):
    _attr_has_entity_name = True
    
    def __init__(self, coordinator: RigForRedCoordinator, entry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f'{entry.entry_id}_rig_for_red'
        self._attr_name = 'Rig for Red'
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name='Rig for Red',
            manufacturer='Custom',
        )
    
    @property
    def is_on(self) -> bool:
        return self.coordinator.is_active
    
    @property
    def icon(self) -> str:
        return 'mdi:submarine' if self.is_on else 'mdi:lighthouse-on'
    
    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.async_activate()
    
    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_restore()

async def async_setup_entry(hass, entry, async_add_entities) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RigForRedSwitch(coordinator, entry)])
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 test_switch_exists: nach setup_entry → entity_id 'switch.rig_for_red' in hass entity registry
- [x] #2 test_switch_initially_off: is_on == False nach setup (coordinator.is_active=False)
- [x] #3 test_turn_on_activates: async_turn_on() → coordinator.async_activate() aufgerufen
- [x] #4 test_turn_off_restores: async_turn_off() → coordinator.async_restore() aufgerufen
- [x] #5 test_icon_changes: is_on=True → icon='mdi:submarine', is_on=False → icon='mdi:lighthouse-on'
- [x] #6 test_state_tracks_coordinator: coordinator.is_active auf True setzen → switch.is_on == True
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
switch.py mit RigForRedSwitch(CoordinatorEntity, SwitchEntity) implementiert. Icons: mdi:submarine (on) / mdi:lighthouse-on (off). is_on tracked von coordinator.is_active.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
switch.py implementiert: RigForRedSwitch als Brücke zwischen HA UI und Coordinator. async_turn_on → coordinator.async_activate(), async_turn_off → coordinator.async_restore(). Dynamische Icons je nach is_on Status.
<!-- SECTION:FINAL_SUMMARY:END -->
