---
id: TASK-50
title: Phase 6 - README + CHANGELOG Update
status: Done
assignee:
  - "@agent-k"
created_date: 2026-05-27 08:12
updated_date: 2026-05-27 15:49
labels:
  - docs
dependencies:
  - TASK-45
  - TASK-46
  - TASK-47
  - TASK-48
  - TASK-49
priority: low
ordinal: 50000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
README.md und CHANGELOG.md aktualisieren: Neue Config-Optionen dokumentieren, AL-Empfehlungen (detect_non_ha_changes, autoreset_control_seconds), AL Logger debug config, Sensor-Entity.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 README.md enthält neue Optionen (enable_debug_logging, al_sleep_mode_rgb)
- [x] #2 README.md: AL detect_non_ha_changes:true + autoreset_control_seconds:0 Empfehlung
- [x] #3 README.md: AL Logger debug config Beispiel
- [x] #4 README.md: Sensor-Entity dokumentiert
- [x] #5 CHANGELOG.md v0.3.0 Eintrag mit allen Änderungen
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Read current README.md + CHANGELOG.md\n2. Add enable_debug_logging + al_sleep_mode to README config section\n3. Add AL recommendations section (detect_non_ha_changes, autoreset_control_seconds, logger debug config)\n4. Add sensor entity documentation\n5. Update CHANGELOG.md with v0.3.0
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
README + CHANGELOG v0.3.0: added enable_debug_logging + al_sleep_mode to config table; AL recommendations (detect_non_ha_changes, autoreset_control_seconds, logger debug config); Sensor Entity section; v0.3.0 changelog with features and fixes.
<!-- SECTION:FINAL_SUMMARY:END -->