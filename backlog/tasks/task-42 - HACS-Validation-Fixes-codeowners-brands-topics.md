---
id: TASK-42
title: 'HACS-Validation-Fixes (codeowners, brands, topics)'
status: To Do
assignee: []
created_date: '2026-05-21 21:49'
labels: []
dependencies: []
modified_files:
  - custom_components/rig_for_red/manifest.json
  - custom_components/rig_for_red/brand/icon.png
ordinal: 43000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
HACS Validation hat 3/8 Checks failed: 1) manifest.json fehlt codeowners, 2) brand/icon.png fehlt, 3) keine GitHub Topics. Zusätzlich schlägt hassfest mit KeyError: codeowners fehl.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 HACS Validation 8/8 bestanden
- [ ] #2 hassfest passiert
<!-- AC:END -->
