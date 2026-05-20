---
id: TASK-13
title: coordinator.py — Sonnenaufgang-Restore Scheduling
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 20:05'
updated_date: '2026-05-20 20:40'
labels: []
milestone: M3 - Coordinator Kernlogik
dependencies:
  - TASK-10
priority: medium
ordinal: 13000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
_get_next_sunrise() Methode implementieren. Wird in async_activate() aufgerufen wenn restore_at_sunrise=True.

def _get_next_sunrise(self) -> datetime:
    from homeassistant.util import dt as dt_util
    try:
        sun_state = self.hass.states.get('sun.sun')
        next_rising_str = sun_state.attributes['next_rising']
        return dt_util.parse_datetime(next_rising_str)
    except Exception:
        _LOGGER.warning('sun.sun entity unavailable or next_rising not found, using +8h fallback')
        return dt_util.now() + timedelta(hours=8)

Das Attribut 'next_rising' in sun.sun enthält einen ISO 8601 Datetime-String (UTC), z.B. '2026-05-21T04:15:00+00:00'.
dt_util.parse_datetime() kann diesen parsen.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 test_get_next_sunrise_from_sun_entity: sun.sun State mit next_rising Attribut → korrekte datetime wird zurückgegeben
- [x] #2 test_get_next_sunrise_fallback: sun.sun existiert nicht (hass.states.get = None) → datetime = now() + 8h
- [ ] #3 test_sunrise_restore_fires: async_activate mit restore_at_sunrise=True, dann async_fire_time_changed zu sunrise Zeit → async_restore wird aufgerufen
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Sonnenaufgang-Restore bereits in T10 implementiert: _get_next_sunrise() liest next_rising aus sun.sun State mit Fallback now()+8h. async_track_point_in_time in async_activate registriert den Listener.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Sonnenaufgang-Restore Scheduling in T10 integriert. _get_next_sunrise() mit sun.sun State-Abfrage und 8h-Fallback. Registrierung via async_track_point_in_time bei Aktivierung.
<!-- SECTION:FINAL_SUMMARY:END -->
