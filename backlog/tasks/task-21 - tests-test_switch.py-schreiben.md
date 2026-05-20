---
id: TASK-21
title: tests/test_switch.py schreiben
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
ordinal: 21000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Tests für switch.py Entity.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 test_switch_exists: nach setup_integration → entity_id 'switch.rig_for_red' in hass.states
- [x] #2 test_switch_initially_off: hass.states.get('switch.rig_for_red').state == 'off'
- [x] #3 test_turn_on: hass.services.async_call('switch', 'turn_on', {'entity_id': 'switch.rig_for_red'}) → coordinator.is_active == True
- [x] #4 test_turn_off: is_active=True, dann switch turn_off → coordinator.is_active == False
- [x] #5 test_icon_submarine_when_on: nach activation → icon attribute == 'mdi:submarine'
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
test_switch.py mit 5 Tests: switch_exists, initially_off, turn_on, turn_off, icon_submarine.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
test_switch.py implementiert mit Tests für Switch-Entity-Existenz, Initialzustand, Ein/Aus-Schalten und Icon-Wechsel.
<!-- SECTION:FINAL_SUMMARY:END -->
