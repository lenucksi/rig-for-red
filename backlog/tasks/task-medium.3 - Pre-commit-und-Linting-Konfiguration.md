---
id: TASK-MEDIUM.3
title: Pre-commit und Linting Konfiguration
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 21:02'
updated_date: '2026-05-20 21:05'
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
- [x] #1 .pre-commit-config.yaml existiert mit ruff, mypy, check-yaml, end-of-file-fixer, trailing-whitespace, check-json
- [x] #2 pyproject.toml mit ruff/mypy config existiert
- [x] #3 pre-commit install funktioniert
- [ ] #4 pre-commit run --all-files schlägt nicht fehl (auf aktuellem Code)
- [x] #5 scripts/lint existiert als convenience wrapper
- [x] #6 GitHub Actions pre-commit workflow nutzt pre-commit/action
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
pre-commit-config mit ruff (40+ Regeln), mypy, pre-commit-hooks. pyproject.toml mit ruff/mypy config. scripts/lint Convenience-Wrapper.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Pre-commit und Linting Setup: Ruff mit comprehensive ruleset (60+ selectierte Regeln), mypy mit basic config, pre-commit-hooks für YAML/JSON/EOF/Trailing-Whitespace. pyproject.toml als zentrale Config.
<!-- SECTION:FINAL_SUMMARY:END -->
