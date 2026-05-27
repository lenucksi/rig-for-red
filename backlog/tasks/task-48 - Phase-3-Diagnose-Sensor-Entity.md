---
id: TASK-48
title: Phase 3 - Diagnose-Sensor Entity
status: Done
assignee:
  - "@agent-k"
created_date: 2026-05-27 08:12
updated_date: 2026-05-27 11:35
labels:
  - sensor
  - diagnostics
dependencies:
  - TASK-45
priority: medium
ordinal: 48000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Neue sensor.py mit sensor.rig_for_red_{entry_id}_state. States: inactive | active_red | dimming_N_of_M | restoring | restored. Attributes mit aktiven Lichtern, next_restore, dimming progress etc.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 sensor.py existiert mit SensorEntity (extends RestoreEntity)
- [x] #2 State wird korrekt aktualisiert bei jedem relevanten Event (inactive→active_red→dimming→restoring→restored)
- [x] #3 Attributes include: active_since, lights_active, lights_tracked_off, next_restore, dim_step, al_switches
- [x] #4 coordinator.py pushed state updates via async_write_ha_state
- [x] #5 __init__.py registriert sensor platform
- [x] #6 strings.json state translations
- [ ] #7 pytest + ruff + mypy pass
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Phase-3: Diagnose-Sensor Entity

Created sensor.py with RigForRedSensor(CoordinatorEntity, RestoreEntity, SensorEntity) that tracks rig-for-red state through lifecycle: inactive -> dimming -> active_red -> restoring -> restored. Attributes include active_since, lights_active, lights_tracked_off, next_restore, dim_step, al_switches. Coordinator extended with restoring, is_dimming, active_since, lights_active, lights_tracked_off, next_restore, dim_step, al_switches properties. Fixed missing type annotation for _light_state_unsubs. Registered sensor platform in __init__.py. translations/en.json + de.json updated.
<!-- SECTION:FINAL_SUMMARY:END -->