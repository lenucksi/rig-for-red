---
id: TASK-39
title: >-
  prek.toml + pyproject.toml aufräumen (trailing-whitespace, ruff-format,
  CPY/COM812)
status: In Progress
assignee:
  - '@agent-k'
created_date: '2026-05-21 21:49'
updated_date: '2026-05-21 21:49'
labels: []
dependencies: []
modified_files:
  - prek.toml
  - pyproject.toml
ordinal: 40000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Fix prek CI failures: exclude backlog/ von trailing-whitespace, exclude backlog/ von ruff-format, CPY aus select entfernen, COM812 in ignore in pyproject.toml. Falls nötig auch ruff files-Filter in prek.toml ergänzen.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 prek CI läuft ohne Fehler auf push zu main
- [ ] #2 Keine trailing-whitespace Fehler mehr in backlog/-Dateien
- [ ] #3 Keine CPY/COM812 Warnings mehr
<!-- AC:END -->
