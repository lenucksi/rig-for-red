---
id: TASK-4
title: config_flow.py — Form-Schema
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 19:56'
updated_date: '2026-05-20 20:37'
labels: []
milestone: M1 - Config Flow
dependencies:
  - TASK-2
  - TASK-3
priority: high
ordinal: 4000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
async_step_user mit allen Konfigurationsfeldern und korrekten HA Selectors implementieren. Noch ohne Validierungslogik.

Felder:
- lights: EntitySelector(domain=light, multiple=True) - required
- schedule_days: SelectSelector(options=WEEKDAYS, multiple=True) - required  
- schedule_time: TimeSelector() - required
- dim_duration_minutes: NumberSelector(min=1, max=240, mode=box) - default 60
- restore_at_sunrise: BooleanSelector() - default True
- restore_time: TimeSelector() - optional
- adaptive_lighting_switches: EntitySelector(domain=switch, multiple=True) - optional, leer erlaubt
- min_brightness_pct: NumberSelector(min=1, max=10, mode=slider) - default 5

Imports: homeassistant.helpers.selector, homeassistant.config_entries, voluptuous
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 config_flow.py existiert unter custom_components/rig_for_red/config_flow.py
- [x] #2 RigForRedConfigFlow(config_entries.ConfigFlow, domain=DOMAIN) Klasse vorhanden
- [x] #3 async_step_user gibt async_show_form mit allen 8 Feldern zurück
- [x] #4 Alle Selectors korrekt typisiert (EntitySelector für lights und al-switches, SelectSelector für days, TimeSelector, NumberSelector, BooleanSelector)
- [x] #5 test_form_displayed: hass.config_entries flow init für DOMAIN gibt step_id='user' und data_schema zurück
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
config_flow.py mit RigForRedConfigFlow Klasse und async_step_user mit allen 8 Selectoren implementiert.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
config_flow.py Form-Schema implementiert: 8 Felder (lights EntitySelector, schedule_days SelectSelector, schedule_time TimeSelector, dim_duration NumberSelector, restore_at_sunrise BooleanSelector, restore_time TimeSelector, adaptive_lighting_switches EntitySelector, min_brightness_pct NumberSelector). Selectors korrekt typisiert und default-Werte gesetzt.
<!-- SECTION:FINAL_SUMMARY:END -->
