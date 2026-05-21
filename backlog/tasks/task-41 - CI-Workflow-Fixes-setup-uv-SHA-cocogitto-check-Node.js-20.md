---
id: TASK-41
title: 'CI-Workflow-Fixes (setup-uv SHA, cocogitto check, Node.js 20)'
status: To Do
assignee: []
created_date: '2026-05-21 21:49'
labels: []
dependencies: []
modified_files:
  - .github/workflows/pytest.yaml
  - .github/workflows/conventional-commits.yml
  - .github/workflows/prek.yml
  - .github/workflows/release-please.yml
  - .github/workflows/hassfest.yml
  - .github/workflows/validate.yml
ordinal: 42000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Drei Probleme in CI-Workflows: 1) astral-sh/setup-uv@<sha> existiert nicht — auf @v5 umstellen, 2) cog check prüft alle Commits seit Projektbeginn — auf --from-latest-tag umstellen, 3) actions/checkout@v4 läuft auf Node.js 20 (deprecated ab Juni 2026) — FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true setzen in allen Workflows.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 pytest Core-Dev Job läuft durch
- [ ] #2 cocogitto check passiert
- [ ] #3 Keine Node.js 20 Deprecation Warnings mehr
<!-- AC:END -->
