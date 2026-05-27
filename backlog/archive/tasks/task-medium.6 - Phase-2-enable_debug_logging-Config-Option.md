---
id: TASK-MEDIUM.6
title: Phase 2 - enable_debug_logging Config Option
status: To Do
assignee: []
created_date: 2026-05-27 08:09
updated_date: 2026-05-27 08:11
labels:
  - config-flow
  - logging
dependencies: []
parent_task_id: TASK-MEDIUM
ordinal: 47000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Toggle enable_debug_logging im Config-Flow. Wenn aktiv: coordinator.py setzt _LOGGER.setLevel(logging.DEBUG). Erlaubt UI-basiertes Debugging ohne configuration.yaml Edit.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Neues Config-Feld CONF_ENABLE_DEBUG_LOGGING in const.py
- [ ] #2 Config-Flow zeigt bool toggle in async_step_init/reconfigure
- [ ] #3 coordinator.py setzt log level bei setup + config_entry update
- [ ] #4 strings.json DE/EN Übersetzung
- [ ] #5 pytest + ruff + mypy pass
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 const.py + config_flow.py implementiert
- [ ] #2 coordinator.py log level handling
- [ ] #3 strings.json DE/EN translations
- [ ] #4 pytest grün
- [ ] #5 ruff + mypy pass
- [ ] #6 Code merged zu main (via worktree)
<!-- DOD:END -->