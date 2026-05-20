---
id: TASK-25
title: Devcontainer für HA Custom Component Entwicklung
status: Done
assignee: []
created_date: '2026-05-20 21:28'
labels:
  - dev
  - infra
milestone: M6 - CI und Docs
dependencies: []
priority: high
ordinal: 25000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Devcontainer-Setup für VSCode, das Home Assistant Core klont, die Integration per Symlink einbindet und eine lauffähige Entwicklungsumgebung bereitstellt. Inklusive Scripts für Setup, Dependencies und Symlinks.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 devcontainer.json existiert mit Python 3.13 image
- [ ] #2 scripts/setup-devcontainer klont HA Core (branch dev)
- [ ] #3 scripts/setup-dependencies installiert HA + test dependencies in venv
- [ ] #4 scripts/setup-symlinks bindet custom_components und tests in core/ ein
- [ ] #5 scripts/develop startet HA mit Integration
- [ ] #6 Port 8123 forwarded
- [ ] #7 VSCode Extensions: Python, Pylance, Coverage Gutters, GitHub PR
- [ ] #8 devcontainer.json postCreateCommand führt setup-devcontainer aus
<!-- AC:END -->
