---
id: TASK-MEDIUM.7
title: Phase 3 - Diagnose-Sensor Entity
status: To Do
assignee: []
created_date: 2026-05-27 08:09
updated_date: 2026-05-27 08:11
labels:
  - sensor
  - diagnostics
dependencies: []
parent_task_id: TASK-MEDIUM
ordinal: 48000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Neue sensor.py mit sensor.rig_for_red_{entry_id}_state. States: inactive | active_red | dimming_N_of_M | restoring | restored. Attributes mit aktiven Lichtern, next_restore, dimming progress etc.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 sensor.py existiert mit SensorEntity (extends RestoreEntity)
- [ ] #2 State wird korrekt aktualisiert bei jedem relevanten Event
- [ ] #3 Attributes include: active_since, lights_active, lights_tracked_off, next_restore, dim_step, al_switches, config (sanitized)
- [ ] #4 coordinator.py pushed state updates via async_write_ha_state
- [ ] #5 __init__.py registriert sensor platform
- [ ] #6 strings.json state translations
- [ ] #7 pytest + ruff + mypy pass
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 sensor.py implementiert (SensorEntity)
- [ ] #2 coordinator.py pushed state updates
- [ ] #3 __init__.py registriert sensor platform
- [ ] #4 strings.json translations
- [ ] #5 pytest grün
- [ ] #6 ruff + mypy pass
- [ ] #7 Code merged zu main (via worktree)
<!-- DOD:END -->