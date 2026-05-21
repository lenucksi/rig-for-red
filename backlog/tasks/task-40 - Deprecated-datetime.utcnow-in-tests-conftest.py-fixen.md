---
id: TASK-40
title: Deprecated datetime.utcnow() in tests/conftest.py fixen
status: To Do
assignee: []
created_date: '2026-05-21 21:49'
labels: []
dependencies: []
modified_files:
  - tests/conftest.py
ordinal: 41000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Ersetze datetime.utcnow() mit datetime.now(UTC) in tests/conftest.py Zeilen 110 und 113. Der prek ruff-Hook schlägt wegen DTZ003 fehl.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Kein DTZ003 Fehler mehr von ruff
- [ ] #2 Alle 100 Tests passen weiterhin
<!-- AC:END -->
