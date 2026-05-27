---
id: TASK-LOW.1
title: Phase 6 - README + CHANGELOG Update
status: To Do
assignee: []
created_date: 2026-05-27 08:09
updated_date: 2026-05-27 08:11
labels:
  - docs
dependencies: []
parent_task_id: TASK-LOW
ordinal: 50000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
README.md und CHANGELOG.md aktualisieren: Neue Config-Optionen dokumentieren, AL-Empfehlungen (detect_non_ha_changes, autoreset_control_seconds), AL Logger debug config, Sensor-Entity.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 README.md enthält neue Optionen (enable_debug_logging, al_sleep_mode_rgb)
- [ ] #2 README.md: AL detect_non_ha_changes:true + autoreset_control_seconds:0 Empfehlung
- [ ] #3 README.md: AL Logger debug config Beispiel
- [ ] #4 README.md: Sensor-Entity dokumentiert
- [ ] #5 CHANGELOG.md v0.3.0 Eintrag mit allen Änderungen
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 README.md updated (neue Optionen, AL-Empfehlungen)
- [ ] #2 CHANGELOG.md v0.3.0 Eintrag
- [ ] #3 Code merged zu main (via worktree)
<!-- DOD:END -->