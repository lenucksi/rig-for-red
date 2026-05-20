---
id: TASK-3
title: manifest.json + strings.json + translations/en.json
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 19:56'
updated_date: '2026-05-20 20:35'
labels: []
milestone: M0 - Scaffold
dependencies:
  - TASK-1
priority: high
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
manifest.json (hassfest-kompatibel), strings.json und translations/en.json mit allen i18n-Keys für den config flow anlegen.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 manifest.json enthält: domain=rig_for_red, name=Rig for Red, version=0.1.0, config_flow=true, requirements=[], dependencies=[], iot_class=local_push
- [x] #2 strings.json und translations/en.json enthalten Keys für alle config-flow-Felder: lights, schedule_days, schedule_time, dim_duration_minutes, restore_at_sunrise, restore_time, adaptive_lighting_switches, min_brightness_pct
- [x] #3 Error-Keys vorhanden: lights_required, restore_time_required, entity_not_found
- [x] #4 Beide JSON-Dateien sind valid JSON (json.loads() wirft keine Exception)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
manifest.json (hassfest-kompatibel), strings.json und translations/en.json erstellt. Alle 3 JSON-Dateien sind valide. strings.json/en.json enthalten Config-Flow Felder und Error-Keys.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
manifest.json mit domain=rig_for_red, version=0.1.0, config_flow=true, iot_class=local_push. strings.json und translations/en.json mit allen config-flow Keys (8 Felder) und 3 Error-Keys (lights_required, restore_time_required, entity_not_found).
<!-- SECTION:FINAL_SUMMARY:END -->
