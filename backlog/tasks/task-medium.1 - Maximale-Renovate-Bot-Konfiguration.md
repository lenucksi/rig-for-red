---
id: TASK-MEDIUM.1
title: Maximale Renovate Bot Konfiguration
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 21:02'
updated_date: '2026-05-20 21:05'
labels:
  - infra
  - ci
milestone: M6 - CI und Docs
dependencies: []
modified_files:
  - .github/renovate.json
  - .github/workflows/renovate.yml
parent_task_id: TASK-MEDIUM
ordinal: 26000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Renovate Bot Setup mit CI-Anbindung für automatische Dependency-Updates: GitHub Actions, pip/pypi, pre-commit hooks. Automerges für Minor/Patch, Dependency Dashboard, Scheduled Runs.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 .github/renovate.json existiert mit config:recommended
- [x] #2 Renovate GitHub Action Workflow existiert (scheduled, workflow_dispatch)
- [x] #3 Auto-merge für Minor/Patch Updates aktiviert
- [x] #4 Dependency Dashboard aktiviert
- [x] #5 Pin GitHub Action Digests (Sicherheit)
- [x] #6 Labels pro Manager-Typ (github-actions, pip, pre-commit)
- [x] #7 Minimum Release Age (3 Tage) für PyPI
- [x] #8 Group-Update für dev-dependencies
- [x] #9 Separate PRs für Major-Updates (kein automerge)
- [x] #10 Schedule: täglich 3:00 UTC
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Renovate Bot Konfiguration fertig. renovate.json mit: config:recommended, Pin-Actions-Digests, Auto-Merge für GHA/pre-commit minor/patch, Group für dev-deps, MinimumReleaseAge 3d, Schedule täglich. Renovate GitHub Action Workflow.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Maximales Renovate Setup: renovate.json mit allen PackageRules, Security-Vulnerability-Alerts, regexManager für HA Core Versions-Updates. Renovate-GitHub-Action mit daily schedule und manuellem Trigger.
<!-- SECTION:FINAL_SUMMARY:END -->
