---
id: TASK-2
title: const.py implementieren
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
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Alle Konstanten für die Integration in custom_components/rig_for_red/const.py definieren. Keine Logik, nur Konstanten.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 DOMAIN = "rig_for_red"
- [x] #2 Alle CONF_* Konstanten vorhanden: CONF_LIGHTS, CONF_SCHEDULE_DAYS, CONF_SCHEDULE_TIME, CONF_DIM_DURATION_MINUTES, CONF_RESTORE_AT_SUNRISE, CONF_RESTORE_TIME, CONF_ADAPTIVE_LIGHTING_SWITCHES, CONF_MIN_BRIGHTNESS_PCT
- [x] #3 DEFAULT_DIM_DURATION_MINUTES = 60, DEFAULT_MIN_BRIGHTNESS_PCT = 5, DEFAULT_RESTORE_AT_SUNRISE = True
- [x] #4 DIM_STEPS = 10, RED_RGB = [255, 0, 0], WHITE_COLOR_TEMP_KELVIN = 2700
- [x] #5 WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
- [x] #6 from custom_components.rig_for_red.const import DOMAIN funktioniert ohne Fehler
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
const.py mit allen CONF_-Konstanten, Defaults (DEFAULT_DIM_DURATION_MINUTES=60, DEFAULT_MIN_BRIGHTNESS_PCT=5, DEFAULT_RESTORE_AT_SUNRISE=True), DIM_STEPS=10, RED_RGB=[255,0,0], WHITE_COLOR_TEMP_KELVIN=2700 und WEEKDAYS-Liste implementiert. Import-Test bestanden.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
const.py implementiert mit allen benötigten Konstanten für die Integration: DOMAIN, 8 CONF_-Konstanten, 3 Defaults, Dimm-Konfiguration, Farbwerte und Wochentagsliste.
<!-- SECTION:FINAL_SUMMARY:END -->
