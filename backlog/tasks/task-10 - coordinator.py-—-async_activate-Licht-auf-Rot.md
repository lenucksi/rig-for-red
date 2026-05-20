---
id: TASK-10
title: coordinator.py — async_activate (Licht auf Rot)
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 20:03'
updated_date: '2026-05-20 20:38'
labels: []
milestone: M3 - Coordinator Kernlogik
dependencies:
  - TASK-9
priority: high
ordinal: 10000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
async_activate implementiert die Kernfunktion: AL deaktivieren (optional), Lichter auf Rot stellen, Dimm-Task starten.

async def async_activate(self) -> None:
    if self.is_active:
        return
    self.is_active = True
    
    # 1. Adaptive Lighting deaktivieren (nur wenn konfiguriert)
    for al_switch in self._al_switches:
        try:
            await self.hass.services.async_call('switch', 'turn_off', {'entity_id': al_switch})
        except Exception:
            pass
        try:
            await self.hass.services.async_call(
                'adaptive_lighting', 'set_manual_control',
                {'entity_id': al_switch, 'lights': self._lights, 'manual_control': True}
            )
        except Exception:  # ServiceNotFound wenn AL nicht installiert
            pass
    
    # 2. Aktuelle Helligkeit lesen (Maximum über alle Lampen, Fallback 255)
    start_brightness = 255
    for light_id in self._lights:
        state = self.hass.states.get(light_id)
        if state and state.attributes.get('brightness'):
            start_brightness = max(start_brightness, state.attributes['brightness'])
    
    # 3. Alle Lampen auf Rot setzen
    await self.hass.services.async_call('light', 'turn_on', {
        'entity_id': self._lights,
        'rgb_color': RED_RGB,
        'brightness': start_brightness,
    })
    
    # 4. Dimm-Task starten
    self._dim_task = self.hass.async_create_task(self._dim_lights(start_brightness))
    
    # 5. Sunrise-Restore registrieren (wenn konfiguriert)
    if self._restore_at_sunrise:
        self._unsub_sunrise = async_track_point_in_time(
            self.hass, self._restore_trigger, self._get_next_sunrise()
        )
    
    # 6. State publizieren
    self.async_set_updated_data({'is_active': True})

HINWEIS: self._al_switches kann eine leere Liste [] sein → Loop läuft einfach nicht. Kein None-Check nötig.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 test_activate_sets_red_light: nach async_activate → light.turn_on wurde mit rgb_color=[255,0,0] aufgerufen
- [x] #2 test_activate_is_active: nach async_activate → coordinator.is_active == True
- [x] #3 test_activate_disables_al: mit al_switches konfiguriert → switch.turn_off für AL-Switch aufgerufen
- [x] #4 test_activate_without_al: al_switches=[] → kein ServiceNotFound, kein Fehler, Licht wird trotzdem auf Rot gesetzt
- [x] #5 test_activate_idempotent: zweimal aufgerufen → zweiter Aufruf macht nichts (is_active Guard)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
async_activate implementiert: AL deaktivieren, Helligkeit lesen, Licht auf Rot, Dimm-Task starten, Sunrise-Restore-Registrierung, is_active setzen, State publish.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
async_activate in coordinator.py implementiert. Deaktiviert Adaptive Lighting (switch.turn_off + set_manual_control), liest aktuelle Helligkeit, setzt Lampen auf Rot (rgb_color=[255,0,0]), startet _dim_lights Task, registriert optional Sunrise-Restore via async_track_point_in_time.
<!-- SECTION:FINAL_SUMMARY:END -->
