---
id: TASK-MEDIUM.3
title: Pre-commit und Linting Konfiguration
status: To Do
assignee: []
created_date: '2026-05-20 21:02'
labels:
  - dev
  - ci
milestone: M6 - CI und Docs
dependencies: []
modified_files:
  - .pre-commit-config.yaml
  - pyproject.toml
  - scripts/lint
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
- [ ] #6 GitHub Actions pre-commit workflow nutzt pre-commit/action
<!-- AC:END -->
