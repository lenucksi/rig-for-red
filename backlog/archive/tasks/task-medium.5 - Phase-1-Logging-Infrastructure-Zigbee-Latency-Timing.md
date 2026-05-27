---
id: TASK-MEDIUM.5
title: Phase 1 - Logging Infrastructure + Zigbee Latency Timing
status: To Do
assignee: []
created_date: 2026-05-27 08:09
updated_date: 2026-05-27 08:10
labels:
  - logging
  - diagnostics
dependencies: []
parent_task_id: TASK-MEDIUM
ordinal: 45000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Baue umfassendes Logging in coordinator.py ein: ~30 Statements auf INFO/DEBUG/WARNING. Aktivierung, Dimming, Restore, Light-Tracking, AL-Fehler. Zusätzlich Zigbee-Latenzmessung per time.monotonic() vor/nach light.turn_on.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 30 neue Log-Statements in coordinator.py (INFO/DEBUG/WARNING)
- [ ] #2 Aktivierung loggt: trigger source, day-of-week pass/fail, light count (on/off)
- [ ] #3 Dimming loggt: step index, brightness alt→neu, skipped entities, cancel
- [ ] #4 Restore loggt: trigger reason (sunrise/time), restored/skipped entities
- [ ] #5 Light-Tracking Events loggen (off→on, on→off während night mode)
- [ ] #6 Zigbee-Latenz in ms per time.monotonic() um light.turn_on messen
- [ ] #7 AL service call Fehler auf WARNING statt ERROR
- [ ] #8 pytest + ruff + mypy pass
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Alle Log-Statements eingebaut (coordinator.py)
- [ ] #2 Code review: keine secrets in Logs, konsistente Formatierung
- [ ] #3 pytest grün
- [ ] #4 ruff + mypy pass
- [ ] #5 Code merged zu main (via worktree)
<!-- DOD:END -->