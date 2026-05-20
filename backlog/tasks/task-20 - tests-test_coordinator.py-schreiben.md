---
id: TASK-20
title: tests/test_coordinator.py schreiben
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 20:08'
updated_date: '2026-05-20 20:44'
labels: []
milestone: M5 - Tests
dependencies:
  - TASK-17
priority: high
ordinal: 20000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Tests für coordinator.py Kernlogik. Nutzt freezegun und async_fire_time_changed.

Teststruktur für Zeit-basierte Tests:
from freezegun import freeze_time
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import async_fire_time_changed

# Beispiel:
async def test_schedule_trigger_correct_day(hass, setup_integration):
    with freeze_time('2026-05-20 23:00:00'):  # Mittwoch
        async_fire_time_changed(hass, dt_util.now())
        await hass.async_block_till_done()
    coordinator = hass.data['rig_for_red'][setup_integration.entry_id]
    assert coordinator.is_active
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 test_schedule_trigger_correct_day: Zeit 23:00 Mittwoch, schedule_days=['wed',...] → is_active=True
- [x] #2 test_schedule_trigger_wrong_day: Zeit 23:00 Samstag, schedule_days=['mon',...,'fri'] → is_active=False
- [x] #3 test_activate_sets_red: nach async_activate → call_args für light.turn_on enthält rgb_color=[255,0,0]
- [x] #4 test_activate_without_al: al_switches=[] → kein Exception, is_active=True
- [x] #5 test_dim_brightness_decreases: nach 10 Schritten → letzte brightness < erste brightness
- [x] #6 test_dim_aborted: async_restore() während Dimmen → Dimm-Loop stoppt
- [x] #7 test_restore_white_light: async_restore → light.turn_on mit color_temp_kelvin=2700
- [x] #8 test_restore_enables_al: al_switches konfiguriert → switch.turn_on für AL aufgerufen
- [x] #9 test_sunrise_restore: mock sun.sun, async_activate, fire_time_changed → async_restore aufgerufen
- [x] #10 test_restore_time_trigger: restore_at_sunrise=False, fire time → async_restore aufgerufen
- [x] #11 test_sunrise_fallback: sun.sun unavailable → _get_next_sunrise gibt now+8h zurück, kein Exception
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
test_coordinator.py mit 11 Tests: schedule_trigger (correct/wrong day), activate (red/without AL), dim (decrease/abort), restore (white/AL/sunrise/restore_time), sunrise_fallback.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
test_coordinator.py mit 11 Tests für die gesamte Coordinator-Kernlogik: Schedule-Guard, Aktivierung, Dimmung, Restore, Sunrise-Scheduling und Fallback.
<!-- SECTION:FINAL_SUMMARY:END -->
