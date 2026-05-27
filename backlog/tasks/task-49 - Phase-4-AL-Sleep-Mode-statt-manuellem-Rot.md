---
id: TASK-49
title: Phase 4 - AL Sleep Mode statt manuellem Rot
status: Done
assignee:
  - "@agent-k"
created_date: 2026-05-27 08:12
updated_date: 2026-05-27 15:15
labels:
  - adaptive-lighting
  - feature
dependencies:
  - TASK-45
  - TASK-46
priority: high
ordinal: 49000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Statt rgb_color: [255,0,0] selbst zu setzen: Nutze AL's sleep mode Mechanismus. Config-Option al_sleep_mode_rgb. Wenn AL installiert + Option aktiv: set_manual_control + change_switch_settings + switch.turn_on(sleep_mode). Fallback zu manuellem Rot wenn kein AL.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Config-Option al_sleep_mode_rgb in const.py + config_flow.py
- [x] #2 async_activate() nutzt AL sleep mode wenn verfügbar + konfiguriert
- [x] #3 set_manual_control(blocking=True) vor change_switch_settings
- [x] #4 sleep_rgb_color wird temporär auf al_sleep_mode_rgb gesetzt (change_switch_settings)
- [x] #5 async_restore() setzt sleep_rgb_color auf AL default [255,56,0] zurück
- [x] #6 switch.turn_on(AL sleep mode) nach config-change
- [x] #7 Fallback zu manuellem rgb_color: [255,0,0] wenn AL nicht installiert oder Option aus
- [ ] #8 pytest + ruff + mypy pass
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. const.py: add CONF_AL_SLEEP_MODE (bool) + DEFAULT_AL_SLEEP_MODE=False
2. config_flow.py: add bool toggle in user + reconfigure steps
3. coordinator.py: read _use_al_sleep_mode from config
4. _disable_al_switches: conditional path — if al_sleep_mode → set_manual_control + change_switch_settings + switch.turn_on(sleep_mode), else existing turn_off
5. _re_enable_al_switches: if al_sleep_mode → change_switch_settings(reset sleep_rgb_color) then existing flow
6. strings.json + en.json + de.json translations
7. ruff check + format
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented AL Sleep Mode as replacement for manual red:
- const.py + config_flow.py: added CONF_AL_SLEEP_MODE (bool) toggle in user and reconfigure steps
- coordinator.py _disable_al_switches: conditional branch uses change_switch_settings(sleep_rgb_color=RED_RGB) + switch.turn_on(sleep_mode=True) instead of switch.turn_off when sleep mode is active
- coordinator.py _re_enable_al_switches: resets sleep_rgb_color to AL default [255,56,0] before re-enabling when sleep mode was used
- coordinator.py async_activate: skips manual red setting and staged dimming when AL sleep mode is active (AL handles it)
- coordinator.py async_restore: skips manual white restore when coming from sleep mode (AL re-enable handles it)
- Fallback to existing manual red path when AL not installed or option disabled
- Translations updated in strings.json, en.json, de.json
- Ruff clean
<!-- SECTION:FINAL_SUMMARY:END -->