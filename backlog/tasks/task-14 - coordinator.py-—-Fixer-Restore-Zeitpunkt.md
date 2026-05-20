---
id: TASK-14
title: coordinator.py — Fixer Restore-Zeitpunkt
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 20:05'
updated_date: '2026-05-20 20:37'
labels: []
milestone: M3 - Coordinator Kernlogik
dependencies:
  - TASK-7
priority: medium
ordinal: 14000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Fixer Restore-Zeitpunkt wenn restore_at_sunrise=False. Bereits in TASK-007 (async_setup) wird der Listener registriert.

Sicherstellen dass:
1. async_setup() nur registriert wenn restore_at_sunrise=False UND restore_time nicht None
2. _restore_trigger wird aufgerufen → ruft async_restore() auf  
3. Der Listener läuft dauerhaft (täglich), nicht nur einmal

Kein neuer Code nötig über TASK-007 hinaus — aber separate Tests erforderlich.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 test_restore_time_trigger: restore_at_sunrise=False, restore_time='07:00' → async_fire_time_changed zu 07:00 → async_restore aufgerufen
- [x] #2 test_no_restore_listener_when_sunrise: restore_at_sunrise=True → kein _unsub_restore gesetzt nach async_setup
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Fixer Restore-Zeitpunkt bereits durch T7 abgedeckt: async_setup registriert Listener nur wenn restore_at_sunrise=False und restore_time gesetzt.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Fixer Restore-Zeitpunkt bereits in T7 implementiert. async_setup registriert async_track_time_change für restore_time nur wenn restore_at_sunrise=False und restore_time not None.
<!-- SECTION:FINAL_SUMMARY:END -->
