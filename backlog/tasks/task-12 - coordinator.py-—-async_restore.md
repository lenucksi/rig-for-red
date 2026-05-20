---
id: TASK-12
title: coordinator.py — async_restore
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 20:05'
updated_date: '2026-05-20 20:40'
labels: []
milestone: M3 - Coordinator Kernlogik
dependencies:
  - TASK-11
priority: high
ordinal: 12000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
async_restore: Dimm-Task abbrechen, Weißlicht setzen, AL optional re-aktivieren, Sunrise neu planen.

async def async_restore(self) -> None:
    # 1. Dimm-Task abbrechen
    if self._dim_task and not self._dim_task.done():
        self._dim_task.cancel()
        await asyncio.gather(self._dim_task, return_exceptions=True)
        self._dim_task = None
    
    # 2. is_active ZUERST auf False → Abbruch-Flag für _dim_lights
    self.is_active = False
    
    # 3. Weißlicht setzen (WICHTIG: color_temp_kelvin, NICHT color_temp/mireds)
    await self.hass.services.async_call('light', 'turn_on', {
        'entity_id': self._lights,
        'color_temp_kelvin': WHITE_COLOR_TEMP_KELVIN,  # = 2700
        'brightness': 255,
        'transition': 2,
    })
    
    # 4. Adaptive Lighting reaktivieren (nur wenn konfiguriert)
    for al_switch in self._al_switches:
        try:
            await self.hass.services.async_call('switch', 'turn_on', {'entity_id': al_switch})
        except Exception:
            pass
        try:
            await self.hass.services.async_call(
                'adaptive_lighting', 'set_manual_control',
                {'entity_id': al_switch, 'lights': self._lights, 'manual_control': False}
            )
        except Exception:
            pass
    
    # 5. Sunrise-Listener cleanen und für nächsten Tag neu registrieren
    if self._unsub_sunrise:
        self._unsub_sunrise()
        self._unsub_sunrise = None
    if self._restore_at_sunrise:
        self._unsub_sunrise = async_track_point_in_time(
            self.hass, self._restore_trigger, self._get_next_sunrise()
        )
    
    # 6. State publizieren
    self.async_set_updated_data({'is_active': False})

_restore_trigger callback:
def _restore_trigger(self, now: datetime) -> None:
    self.hass.async_create_task(self.async_restore())
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 test_restore_sets_white: async_restore → light.turn_on mit color_temp_kelvin=2700 und brightness=255
- [x] #2 test_restore_clears_active: nach async_restore → coordinator.is_active == False
- [x] #3 test_restore_cancels_dim: Dimm-Task läuft → async_restore cancelt ihn
- [x] #4 test_restore_enables_al: al_switches konfiguriert → switch.turn_on für AL-Switch aufgerufen
- [x] #5 test_restore_without_al: al_switches=[] → kein Fehler, Weißlicht wird trotzdem gesetzt
- [x] #6 test_restore_reschedules_sunrise: restore_at_sunrise=True → _unsub_sunrise nach async_restore neu gesetzt
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
async_restore implementiert: Dimm-Task abbrechen, Weißlicht (2700K, brightness=255, transition=2), AL reaktivieren, Sunrise-Listener für nächsten Tag neu registrieren. _restore_trigger delegiert an async_restore.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
async_restore und _restore_trigger in coordinator.py implementiert. Vollständiger Restore-Zyklus: Dimm-Task-Cancel, Weißlicht-Wiederherstellung, AL-Reaktivierung, Sunrise-Rescheduling für Folgetag.
<!-- SECTION:FINAL_SUMMARY:END -->
