---
id: TASK-46
title: Phase 5 - blocking=True für set_manual_control Service Calls
status: Done
assignee:
  - "@agent-k"
created_date: 2026-05-27 08:12
updated_date: 2026-05-27 10:06
labels:
  - race-condition
  - fix
dependencies: []
priority: high
ordinal: 46000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Fix Race-Condition zwischen rig-for-red und adaptive-lighting: blocking=True bei allen hass.services.async_call für adaptive_lighting.set_manual_control. Sicherstellen dass set_manual_control durch ist bevor light.turn_on feuert.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 async_activate() ruft set_manual_control mit blocking=True
- [x] #2 async_restore() ruft set_manual_control mit blocking=True
- [x] #3 Kein sichtbares Verhalten geändert, nur Race-Condition-Fenster geschlossen
- [x] #4 pytest + ruff + mypy pass
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Verified: set_manual_control(blocking=True) was already correctly implemented in TASK-43. No changes needed.
<!-- SECTION:FINAL_SUMMARY:END -->