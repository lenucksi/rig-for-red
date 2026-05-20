---
id: TASK-22
title: GitHub Actions CI einrichten
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 20:08'
updated_date: '2026-05-20 20:44'
labels: []
milestone: M6 - CI und Docs
dependencies:
  - TASK-17
priority: medium
ordinal: 22000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Drei GitHub Actions Workflows anlegen.

.github/workflows/tests.yml:
name: Tests
on: [push, pull_request]
jobs:
  pytest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r requirements_test.txt
      - run: pytest tests/ --cov=custom_components/rig_for_red --cov-report=xml --cov-fail-under=80
      - uses: codecov/codecov-action@v4
        if: always()

.github/workflows/hassfest.yml:
name: Hassfest
on: [push, pull_request, schedule: [{cron: '0 0 * * *'}]]
jobs:
  hassfest:
    uses: 'home-assistant/actions/.github/workflows/hassfest.yaml@main'

.github/workflows/validate.yml:
name: HACS Validation
on: [push, pull_request]
jobs:
  validate:
    uses: 'hacs/action/.github/workflows/validate.yaml@main'
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 .github/workflows/tests.yml existiert und ist valid YAML
- [x] #2 .github/workflows/hassfest.yml existiert und ist valid YAML
- [x] #3 .github/workflows/validate.yml existiert und ist valid YAML
- [x] #4 tests.yml läuft pytest mit --cov-fail-under=80
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
3 GitHub Actions Workflows erstellt: tests.yml (pytest + coverage 80%), hassfest.yml (HA-Validierung), validate.yml (HACS-Validierung).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
GitHub Actions CI eingerichtet: tests.yml mit pytest und --cov-fail-under=80, hassfest.yml für HA-Validator, validate.yml für HACS-Validator.
<!-- SECTION:FINAL_SUMMARY:END -->
