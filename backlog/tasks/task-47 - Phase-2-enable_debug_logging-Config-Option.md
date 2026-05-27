---
id: TASK-47
title: Phase 2 - enable_debug_logging Config Option
status: Done
assignee:
  - "@agent-k"
created_date: 2026-05-27 08:12
updated_date: 2026-05-27 10:54
labels:
  - config-flow
  - logging
dependencies:
  - TASK-45
priority: medium
ordinal: 47000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Toggle enable_debug_logging im Config-Flow. Wenn aktiv: coordinator.py setzt _LOGGER.setLevel(logging.DEBUG). Erlaubt UI-basiertes Debugging ohne configuration.yaml Edit.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Neues Config-Feld CONF_ENABLE_DEBUG_LOGGING in const.py
- [x] #2 Config-Flow zeigt bool toggle in async_step_init/reconfigure
- [x] #3 coordinator.py setzt log level bei setup + config_entry update
- [x] #4 strings.json DE/EN Übersetzung
- [ ] #5 pytest + ruff + mypy pass
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Phase-2: Config option enable_debug_logging

Added a boolean toggle in the config flow (async_step_user + async_step_reconfigure) and stored as CONF_ENABLE_DEBUG_LOGGING in const.py. The coordinator reads the option in __init__ and calls _LOGGER.setLevel(logging.DEBUG) during async_setup if enabled.

- const.py: CONF_ENABLE_DEBUG_LOGGING const + default False
- config_flow.py: BooleanSelector in both init and reconfigure steps
- coordinator.py: applies log level in async_setup, logs confirmation
- strings.json + translations/en.json + translations/de.json updated
- ruff check + format pass cleanly
<!-- SECTION:FINAL_SUMMARY:END -->