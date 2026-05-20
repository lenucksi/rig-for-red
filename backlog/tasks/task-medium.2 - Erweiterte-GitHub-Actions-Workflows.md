---
id: TASK-MEDIUM.2
title: Erweiterte GitHub Actions Workflows
status: To Do
assignee: []
created_date: '2026-05-20 21:02'
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
- [ ] #1 pre-commit.yml existiert für PR-Linting
- [ ] #2 release-drafter.yml existiert für automatische Release-Notes
- [ ] #3 labeler.yml existiert für automatische PR-Labeling
- [ ] #4 stale.yml existiert für Issue/PR-Stale-Management
- [ ] #5 CODEOWNERS existiert
- [ ] #6 config.yml (FUNDING) existiert
- [ ] #7 Issue-Templates existieren (.github/ISSUE_TEMPLATE)
<!-- AC:END -->
