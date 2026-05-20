---
id: TASK-MEDIUM.2
title: Erweiterte GitHub Actions Workflows
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 21:02'
updated_date: '2026-05-20 21:05'
labels:
  - ci
  - infra
milestone: M6 - CI und Docs
dependencies: []
modified_files:
  - .github/workflows/pre-commit.yml
  - .github/workflows/release-drafter.yml
  - .github/workflows/labeler.yml
  - .github/workflows/stale.yml
  - .github/CODEOWNERS
  - .github/ISSUE_TEMPLATE/
parent_task_id: TASK-MEDIUM
ordinal: 27000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Von adaptive-lighting inspirierte CI-Workflows: pre-commit, release-drafter, labeler, stale-management, Codeowners.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 pre-commit.yml existiert für PR-Linting
- [x] #2 release-drafter.yml existiert für automatische Release-Notes
- [x] #3 labeler.yml existiert für automatische PR-Labeling
- [x] #4 stale.yml existiert für Issue/PR-Stale-Management
- [x] #5 CODEOWNERS existiert
- [x] #6 config.yml (FUNDING) existiert
- [x] #7 Issue-Templates existieren (.github/ISSUE_TEMPLATE)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Extended CI Workflows erstellt: pre-commit, release-drafter (+config), labeler (+config), stale, CODEOWNERS, FUNDING, ISSUE_TEMPLATE (bug, feature, config).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Erweiterte GitHub Actions Infrastruktur: pre-commit Workflow, Release Drafter mit Kategorien, Labeler für Auto-Labeling, Stale-Management, Issue-Templates für Bug Reports und Feature Requests, CODEOWNERS.
<!-- SECTION:FINAL_SUMMARY:END -->
