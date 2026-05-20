---
id: TASK-11
title: coordinator.py — _dim_lights Hintergrundtask
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 20:03'
updated_date: '2026-05-20 20:39'
labels: []
milestone: M3 - Coordinator Kernlogik
dependencies:
  - TASK-10
priority: high
ordinal: 11000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Gestufte Dimmschleife als async Coroutine implementieren. Wird als asyncio.Task im Hintergrund ausgeführt.

async def _dim_lights(self, start_brightness: int) -> None:
    target = max(1, int(self._min_brightness_pct / 100 * 255))
    interval = (self._dim_duration * 60) / DIM_STEPS
    
    for i in range(1, DIM_STEPS + 1):
        if not self.is_active:  # Abbruch-Flag (gesetzt durch async_restore)
            return
        brightness = int(start_brightness - (start_brightness - target) * i / DIM_STEPS)
        await self.hass.services.async_call('light', 'turn_on', {
            'entity_id': self._lights,
            'rgb_color': RED_RGB,
            'brightness': max(1, brightness),
            'transition': interval,  # sanfter Übergang zwischen Steps
        })
        try:
            await asyncio.sleep(interval)
        except asyncio.CancelledError:
            return  # Task wurde gecancelt

WICHTIG: asyncio.CancelledError MUSS gefangen werden, sonst wird die Exception propagiert und als unhandled gilt.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 test_dim_reduces_brightness: nach Ablauf aller Steps → letzter light.turn_on Call hat brightness <= start_brightness * 0.1
- [x] #2 test_dim_stays_red: alle light.turn_on Calls während Dimming haben rgb_color=[255,0,0]
- [x] #3 test_dim_aborted_by_restore: is_active=False setzen während Dimming → Loop bricht ab, kein weiterer light.turn_on
- [x] #4 test_dim_cancelled: task.cancel() → kein asyncio.CancelledError propagiert
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
_dim_lights implementiert: gestufte Dimmung in DIM_STEPS=10 Schritten. Lineare Interpolation von start_brightness zu target (min_brightness_pct% von 255). CancelledError beim sleep gefangen. is_active-Guard in jedem Step.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
_dim_lights Hintergrundtask implementiert. Gestufte Dimmung mit konfigurierbarer Dauer und Zielhelligkeit. Abbruch bei is_active=False oder CancelledError. Jeder Schritt setzt rgb_color=[255,0,0] mit Transition.
<!-- SECTION:FINAL_SUMMARY:END -->
