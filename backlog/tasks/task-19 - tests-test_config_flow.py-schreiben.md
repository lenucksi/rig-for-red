---
id: TASK-19
title: tests/test_config_flow.py schreiben
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
ordinal: 19000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Tests für config_flow.py: Form, Validierung, Entry-Erstellung.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 test_form_displayed: flow init → result type=FORM, step_id='user', data_schema enthält alle 8 Felder
- [x] #2 test_valid_config_creates_entry: valide Daten mit AL → result type=CREATE_ENTRY, result.title wie erwartet
- [x] #3 test_valid_config_no_al: valide Daten ohne AL (leer) → CREATE_ENTRY, kein Fehler
- [x] #4 test_missing_lights_error: lights=[] → result type=FORM, errors['lights']='lights_required'
- [x] #5 test_restore_time_required: restore_at_sunrise=False, restore_time fehlt → errors['restore_time']='restore_time_required'
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
test_config_flow.py mit 5 Tests: form_displayed, valid_config, valid_no_al, missing_lights_error, restore_time_required.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
test_config_flow.py implementiert mit Tests für Form-Anzeige, Entry-Erstellung (mit/ohne AL), Validierungsfehler (lights_required, restore_time_required).
<!-- SECTION:FINAL_SUMMARY:END -->
