---
id: TASK-34
title: 'Cleanup: Logo, Test-Struktur, Dockerfile-Optimierung'
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-21 15:23'
updated_date: '2026-05-21 15:32'
labels: []
dependencies:
  - TASK-32
priority: medium
ordinal: 33000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Abschluss-Arbeiten: Logo kopieren, alte Test-Dateien entfernen, Dockerfile.test optimieren.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 logo.png ins custom_component Verzeichnis kopiert (erstes Candidate-Bild)
- [x] #2 Alte root-level Test-Dateien gelöscht (tests/test_config_flow.py etc)
- [x] #3 Dockerfile.test optimiert (conftest-copy vereinfacht, setup.cfg includiert)
- [x] #4 Alle 34 Tests passieren nach Cleanup
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. cp openrouter-image-output.png custom_components/rig_for_red/logo.png\n2. rm tests/test_config_flow.py tests/test_coordinator.py tests/test_switch.py tests/test_init.py\n3. Dockerfile.test optimieren\n4. Tests laufen lassen zur Verifikation
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Logo kopiert (openrouter-image-output.png -> logo.png), alte root-level Test-Dateien gelöscht (tests/test_*.py -> tests/components/rig_for_red/), Dockerfile.test optimiert (ARG HA_VERSION, setup.cfg, --no-cache-dir, conftest nach root). 34 Tests passieren.
<!-- SECTION:FINAL_SUMMARY:END -->
