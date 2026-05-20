---
id: TASK-5
title: config_flow.py — Validierungslogik
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 19:57'
updated_date: '2026-05-20 20:37'
labels: []
milestone: M1 - Config Flow
dependencies:
  - TASK-4
priority: high
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Eingabe-Validierung in async_step_user implementieren. Bei Fehler: Form neu anzeigen mit errors dict.

Validierungsregeln:
1. user_input[CONF_LIGHTS] darf nicht leer sein → errors['lights'] = 'lights_required'
2. Wenn user_input[CONF_RESTORE_AT_SUNRISE] == False und CONF_RESTORE_TIME fehlt/leer → errors['restore_time'] = 'restore_time_required'  
3. Jede Entity-ID in CONF_LIGHTS muss als light.* State in hass.states existieren → errors['lights'] = 'entity_not_found'

Wenn errors nicht leer: return self.async_show_form(step_id='user', data_schema=..., errors=errors)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 test_missing_lights_shows_error: leere lights-Liste → error key 'lights_required' in Rückgabe
- [x] #2 test_restore_time_required: restore_at_sunrise=False ohne restore_time → error key 'restore_time_required'
- [x] #3 test_invalid_entity: nicht-existente entity_id in lights → error key 'entity_not_found'
- [x] #4 Bei gültigen Daten ohne AL-Switches (leer): kein Fehler
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Validierungslogik in async_step_user integriert: leere lights, restore_time erforderlich wenn restore_at_sunrise=False, entity_not_found Prüfung.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Eingabe-Validierung in config_flow.py implementiert. Drei Fehlerfälle: lights_required (leere Liste), restore_time_required (restore ohne Zeit), entity_not_found (unbekannte entity_id). Form wird bei Fehlern mit errors-dict neu angezeigt.
<!-- SECTION:FINAL_SUMMARY:END -->
