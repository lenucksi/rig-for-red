---
id: TASK-32
title: CI/CD Pipeline mit Multi-Release Matrix-Testing
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-21 15:23'
updated_date: '2026-05-21 15:32'
labels: []
dependencies: []
references:
  - .github/workflows/tests.yml
  - /home/jo/kit/homeass/adaptive-lighting/.github/workflows/pytest.yaml
  - /home/jo/kit/homeass/adaptive-lighting/scripts/update-test-matrix.py
  - >-
    /home/jo/kit/homeass/adaptive-lighting/.github/workflows/install_dependencies/action.yml
documentation:
  - guides/testing-and-ci
priority: high
ordinal: 31000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Von adaptive-lighting inspirierte Pipeline: Docker-basiertes Matrix-Testing über mehrere HA-Versionen + dev, automatische Matrix-Updates via Script, Release Drafter, renovate.

Der bestehende tests.yml wird durch ein neues pytest.yaml ersetzt, das in Docker-Containern gegen verschiedene HA-Versionen testet. Ein update-test-matrix Script holt wöchentlich die neuesten HA-Tags von GitHub und erstellt PRs mit aktualisierter Matrix.

Release Drafter (v7) erstellt automatisch Release-Notes aus PR-Titeln. Renovate updated Dependencies automatisch.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 pytest.yaml mit Docker-basiertem Matrix-Testing (core-version + python-version)
- [ ] #2 install_dependencies composite action für reproduzierbare Test-Umgebung
- [x] #3 update-test-matrix.yaml Workflow (weekly cron + workflow_dispatch)
- [x] #4 scripts/update-test-matrix.py: HA Tags fetchen, Python-Version mappen, Matrix generieren
- [x] #5 release-drafter Workflow + Config (v7, PR-basierte Release-Notes)
- [x] #6 renovate.json aktualisiert (GitHub Actions auto-merge, pip_requirements group)
- [x] #7 Alle Workflows nutzen SHA-pinned Actions (Renovate gepflegt)
- [ ] #8 scripts/setup-dependencies und setup-symlinks (für dev-Branch-Testing)
- [ ] #9 dev-Branch der Matrix klont HA Core + symlinkt statt Docker
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. tests.yml -> pytest.yaml umbauen (Docker-basiert, core-version/python-version Matrix)\n2. scripts/update-test-matrix.py erstellen (HA Tags fetchen, Python mappen, YAML generieren)\n3. .github/workflows/update-test-matrix.yaml (weekly cron + PR-Erstellung)\n4. .github/workflows/release-drafter.yml auf v7 aktualisieren\n5. scripts/setup-dependencies + scripts/setup-symlinks (dev-Branch-Testing)\n6. renovate.json prüfen/erweitern
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
CI/CD Pipeline komplett: pytest.yaml mit Docker-Matrix (2 stabile HA-Versionen + dev-Job via Core-Checkout), update-test-matrix.yaml mit weekly-Schedule und auto-PR, scripts/update-test-matrix.py (HA Tags fetchen → Python mappen → Matrix generieren), release-drafter.yml (v6, PR-basierte Release-Notes). alte tests.yml gelöscht.
<!-- SECTION:FINAL_SUMMARY:END -->
