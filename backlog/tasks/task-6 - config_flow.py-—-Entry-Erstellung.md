---
id: TASK-6
title: config_flow.py — Entry-Erstellung
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 19:57'
updated_date: '2026-05-20 20:37'
labels: []
milestone: M1 - Config Flow
dependencies:
  - TASK-5
priority: high
ordinal: 6000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Nach erfolgreicher Validierung einen Config Entry erstellen.

Entry-Titel generieren: 'Rig for Red ({schedule_time} [{schedule_days_joined}])'
Beispiel: 'Rig for Red (23:00 [mon,tue,wed,thu,fri])'
Dabei schedule_days als komma-separierter String joinen.

return self.async_create_entry(title=title, data=user_input)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 test_valid_config_creates_entry: valide Eingabe → result.type == FlowResultType.CREATE_ENTRY
- [x] #2 result.title entspricht Format 'Rig for Red (HH:MM [day,day,...])'
- [x] #3 result.data enthält alle user_input Felder unverändert
- [x] #4 test_valid_config_no_al: valide Eingabe ohne adaptive_lighting_switches → Entry wird trotzdem erstellt
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Entry-Erstellung nach erfolgreicher Validierung. Titel-Format: 'Rig for Red (HH:MM [tag,tag,...])'. async_create_entry mit allen user_input Daten.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Entry-Erstellung in config_flow.py implementiert. Titel wird aus schedule_time und schedule_days generiert. async_create_entry gibt alle user_input Felder unverändert weiter.
<!-- SECTION:FINAL_SUMMARY:END -->
