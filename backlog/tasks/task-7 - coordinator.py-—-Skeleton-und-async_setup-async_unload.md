---
id: TASK-7
title: coordinator.py — Skeleton und async_setup/async_unload
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 19:58'
updated_date: '2026-05-20 20:37'
labels: []
milestone: M2 - Coordinator Setup
dependencies:
  - TASK-2
priority: high
ordinal: 7000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
RigForRedCoordinator(DataUpdateCoordinator) Klasse mit Setup und Teardown implementieren.

Datei: custom_components/rig_for_red/coordinator.py

Imports benötigt:
- from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
- from homeassistant.helpers.event import async_track_time_change, async_track_point_in_time
- from homeassistant.core import HomeAssistant
- from homeassistant.config_entries import ConfigEntry
- import asyncio, logging
- from .const import *

Klassen-Struktur:
class RigForRedCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(hass, _LOGGER, name=DOMAIN)
        self._entry = entry
        self.is_active: bool = False
        self._unsub_schedule = None
        self._unsub_restore = None  
        self._unsub_sunrise = None
        self._dim_task: asyncio.Task | None = None
        # Config aus entry.data lesen
        self._lights = entry.data[CONF_LIGHTS]
        self._schedule_days = entry.data[CONF_SCHEDULE_DAYS]
        self._schedule_time = entry.data[CONF_SCHEDULE_TIME]  # 'HH:MM'
        self._dim_duration = entry.data.get(CONF_DIM_DURATION_MINUTES, DEFAULT_DIM_DURATION_MINUTES)
        self._restore_at_sunrise = entry.data.get(CONF_RESTORE_AT_SUNRISE, DEFAULT_RESTORE_AT_SUNRISE)
        self._restore_time = entry.data.get(CONF_RESTORE_TIME)
        self._al_switches = entry.data.get(CONF_ADAPTIVE_LIGHTING_SWITCHES, [])
        self._min_brightness_pct = entry.data.get(CONF_MIN_BRIGHTNESS_PCT, DEFAULT_MIN_BRIGHTNESS_PCT)

    async def async_setup(self) -> None:
        hour, minute = [int(x) for x in self._schedule_time.split(':')]
        self._unsub_schedule = async_track_time_change(
            self.hass, self._schedule_trigger, hour=hour, minute=minute, second=0
        )
        if not self._restore_at_sunrise and self._restore_time:
            rh, rm = [int(x) for x in self._restore_time.split(':')]
            self._unsub_restore = async_track_time_change(
                self.hass, self._restore_trigger, hour=rh, minute=rm, second=0
            )

    async def async_unload(self) -> None:
        if self._unsub_schedule:
            self._unsub_schedule()
        if self._unsub_restore:
            self._unsub_restore()
        if self._unsub_sunrise:
            self._unsub_sunrise()
        if self._dim_task and not self._dim_task.done():
            self._dim_task.cancel()
            await asyncio.gather(self._dim_task, return_exceptions=True)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 coordinator.py existiert mit RigForRedCoordinator Klasse
- [x] #2 async_setup() registriert async_track_time_change für schedule_time
- [x] #3 async_setup() registriert async_track_time_change für restore_time NUR wenn restore_at_sunrise=False
- [x] #4 async_unload() ruft alle _unsub_* callbacks auf und cancelt _dim_task
- [x] #5 is_active ist False nach Instanziierung
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
RigForRedCoordinator(DataUpdateCoordinator) implementiert. async_setup registriert Zeit-Listener, async_unload räumt auf. is_active=False nach Init. Stub-Methoden für spätere Tasks.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Coordinator Skeleton implementiert. RigForRedCoordinator mit __init__ (alle config-Felder), async_setup (async_track_time_change für schedule_time und bedingt restore_time), async_unload (Cleanup). Stub-Methoden für _schedule_trigger, _restore_trigger, async_activate, async_restore, _dim_lights.
<!-- SECTION:FINAL_SUMMARY:END -->
