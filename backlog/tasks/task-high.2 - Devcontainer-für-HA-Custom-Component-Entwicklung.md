---
id: TASK-HIGH.2
title: Devcontainer für HA Custom Component Entwicklung
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 21:02'
updated_date: '2026-05-20 21:04'
labels:
  - dev
  - infra
milestone: M6 - CI und Docs
dependencies: []
modified_files:
  - .devcontainer.json
  - scripts/setup-devcontainer
  - scripts/setup-dependencies
  - scripts/setup-symlinks
  - scripts/develop
parent_task_id: TASK-HIGH
ordinal: 25000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Devcontainer-Setup für VSCode, das Home Assistant Core klont, die Integration per Symlink einbindet und eine lauffähige Entwicklungsumgebung bereitstellt. Inklusive Scripts für Setup, Dependencies und Symlinks.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 devcontainer.json existiert mit Python 3.13 image
- [x] #2 scripts/setup-devcontainer klont HA Core (branch dev)
- [x] #3 scripts/setup-dependencies installiert HA + test dependencies in venv
- [x] #4 scripts/setup-symlinks bindet custom_components und tests in core/ ein
- [x] #5 scripts/develop startet HA mit Integration
- [x] #6 Port 8123 forwarded
- [x] #7 VSCode Extensions: Python, Pylance, Coverage Gutters, GitHub PR
- [x] #8 devcontainer.json postCreateCommand führt setup-devcontainer aus
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Devcontainer-Setup fertig: devcontainer.json mit Dockerfile, scripts/setup-devcontainer, scripts/setup-dependencies, scripts/setup-symlinks, scripts/develop. Port 8123 forwarded. VSCode Extensions eingerichtet.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Devcontainer für HA Custom Component Entwicklung erstellt. Basiert auf mcr.microsoft.com/devcontainers/python:3-3.13. Klont HA Core, erstellt venv mit allen Dependencies, bindet Integration per Symlink ein. Port 8123 forwarded. Scripts für Setup, Develop und Lint.
<!-- SECTION:FINAL_SUMMARY:END -->
