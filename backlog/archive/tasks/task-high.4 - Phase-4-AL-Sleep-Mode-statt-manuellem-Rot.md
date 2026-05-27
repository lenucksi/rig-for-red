---
id: TASK-HIGH.4
title: Phase 4 - AL Sleep Mode statt manuellem Rot
status: To Do
assignee: []
created_date: 2026-05-27 08:09
updated_date: 2026-05-27 08:11
labels:
  - adaptive-lighting
  - feature
dependencies: []
parent_task_id: TASK-HIGH
ordinal: 49000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Statt rgb_color: [255,0,0] selbst zu setzen: Nutze AL's sleep mode Mechanismus. Config-Option al_sleep_mode_rgb. Wenn AL installiert + Option aktiv: set_manual_control + change_switch_settings + switch.turn_on(sleep_mode). Fallback zu manuellem Rot wenn kein AL.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Config-Option al_sleep_mode_rgb in const.py + config_flow.py
- [ ] #2 async_activate() nutzt AL sleep mode wenn verfügbar + konfiguriert
- [ ] #3 set_manual_control(blocking=True) vor change_switch_settings
- [ ] #4 sleep_rgb_color wird temporär auf al_sleep_mode_rgb gesetzt (change_switch_settings)
- [ ] #5 async_restore() setzt sleep_rgb_color auf AL default [255,56,0] zurück
- [ ] #6 switch.turn_on(AL sleep mode) nach config-change
- [ ] #7 Fallback zu manuellem rgb_color: [255,0,0] wenn AL nicht installiert oder Option aus
- [ ] #8 pytest + ruff + mypy pass
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 const.py + config_flow.py implementiert
- [ ] #2 coordinator.py AL sleep mode integration
- [ ] #3 Fallback-Logik (ohne AL)
- [ ] #4 pytest grün
- [ ] #5 ruff + mypy pass
- [ ] #6 Code merged zu main (via worktree)
<!-- DOD:END -->