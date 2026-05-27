---
id: TASK-HIGH.3
title: Phase 5 - blocking=True für set_manual_control Service Calls
status: To Do
assignee: []
created_date: 2026-05-27 08:09
updated_date: 2026-05-27 08:10
labels:
  - race-condition
  - fix
dependencies: []
parent_task_id: TASK-HIGH
ordinal: 46000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Fix Race-Condition zwischen rig-for-red und adaptive-lighting: blocking=True bei allen hass.services.async_call für adaptive_lighting.set_manual_control. Sicherstellen dass set_manual_control durch ist bevor light.turn_on feuert.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 async_activate() ruft set_manual_control mit blocking=True
- [ ] #2 async_restore() ruft set_manual_control mit blocking=True
- [ ] #3 Kein sichtbares Verhalten geändert, nur Race-Condition-Fenster geschlossen
- [ ] #4 pytest + ruff + mypy pass
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 blocking=True in async_activate
- [ ] #2 blocking=True in async_restore
- [ ] #3 pytest grün
- [ ] #4 ruff + mypy pass
- [ ] #5 Code merged zu main (via worktree)
<!-- DOD:END -->