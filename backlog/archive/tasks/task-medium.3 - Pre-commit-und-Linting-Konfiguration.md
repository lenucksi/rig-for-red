---
id: TASK-MEDIUM.3
title: Pre-commit und Linting Konfiguration
status: Done
assignee: []
created_date: '2026-05-20 21:28'
labels:
  - dev
  - ci
milestone: M6 - CI und Docs
dependencies: []
parent_task_id: TASK-MEDIUM
ordinal: 28000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Pre-commit Hooks für Python-Code-Qualität: ruff, mypy, black, isort, check-yaml, end-of-file-fixer, trailing-whitespace. Von adaptive-lighting inspiriert.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 .pre-commit-config.yaml existiert mit ruff, mypy, check-yaml, end-of-file-fixer, trailing-whitespace, check-json
- [ ] #2 pyproject.toml mit ruff/mypy config existiert
- [ ] #3 pre-commit install funktioniert
- [ ] #4 pre-commit run --all-files schlägt nicht fehl (auf aktuellem Code)
- [ ] #5 scripts/lint existiert als convenience wrapper
<!-- AC:END -->
