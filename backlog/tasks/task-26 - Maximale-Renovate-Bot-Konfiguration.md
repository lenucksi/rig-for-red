---
id: TASK-26
title: Maximale Renovate Bot Konfiguration
status: Done
assignee: []
created_date: '2026-05-20 21:28'
labels:
  - infra
  - ci
milestone: M6 - CI und Docs
dependencies: []
priority: medium
ordinal: 26000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Renovate Bot Setup mit CI-Anbindung für automatische Dependency-Updates: GitHub Actions, pip/pypi, pre-commit hooks. Automerges für Minor/Patch, Dependency Dashboard, Scheduled Runs.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 .github/renovate.json existiert mit config:recommended
- [ ] #2 Renovate GitHub Action Workflow existiert (scheduled, workflow_dispatch)
- [ ] #3 Auto-merge für Minor/Patch Updates aktiviert
- [ ] #4 Dependency Dashboard aktiviert
- [ ] #5 Pin GitHub Action Digests (Sicherheit)
- [ ] #6 Labels pro Manager-Typ (github-actions, pip, pre-commit)
- [ ] #7 Minimum Release Age (3 Tage) für PyPI
- [ ] #8 Group-Update für dev-dependencies
- [ ] #9 Separate PRs für Major-Updates (kein automerge)
- [ ] #10 Schedule: täglich 3:00 UTC
<!-- AC:END -->
