---
id: TASK-18
title: tests/test_init.py schreiben
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
ordinal: 18000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Tests für __init__.py: Entry-Setup, Teardown, Services.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 test_async_setup_entry_success: entry setup → coordinator in hass.data['rig_for_red'][entry.entry_id], Type RigForRedCoordinator
- [x] #2 test_async_unload_entry: unload nach setup → hass.data['rig_for_red'] hat entry_id nicht mehr
- [x] #3 test_services_registered: nach setup → hass.services.has_service('rig_for_red', 'trigger_rig') und 'restore_lights' beide True
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
test_init.py mit 3 Tests: async_setup_entry_success, async_unload_entry, services_registered.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
test_init.py implementiert mit Tests für Entry-Setup (Coordinator-Instanziierung), Entry-Teardown (Cleanup) und Service-Registrierung.
<!-- SECTION:FINAL_SUMMARY:END -->
