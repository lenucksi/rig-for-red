---
id: TASK-33
title: Testing & CI Development Guide
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-21 15:23'
updated_date: '2026-05-21 15:32'
labels: []
dependencies: []
documentation:
  - guides/testing-and-ci
priority: medium
ordinal: 32000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Ausführliches backlog doc (guides/testing-and-ci) das die gesamte Test- und CI-Infrastruktur dokumentiert: lokal mit Docker vs Core-Venv, Multi-Release-Matrix-Testing, CI/CD in GitHub Actions.

Ziel: Das Doc muss für Menschen verständlich sein (auch ohne HA-Erfahrung) und als Template für zukünftige HA Custom Components dienen.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Doc erklärt lokale Entwicklung (Docker: schnell, PyPI-basiert vs Core-Venv: aufwändig, volle Kontrolle)
- [ ] #2 Doc erklärt Multi-Release-Matrix-Strategie (welche Versionen, warum)
- [ ] #3 Doc erklärt CI/CD Pipeline (alle Workflows, Matrix-Auto-Update, Renovate)
- [ ] #4 Doc erklärt Release Drafter + Release-Prozess
- [ ] #5 Doc enthält Reusability-Template (Checkliste für neue HA Addons)
- [ ] #6 Doc enthält Troubleshooting-Sektion (StateMachine, ServiceNotFound, ConfigEntry)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inhalt sammeln (aus TASK-32 Implementation, adaptive-lighting Referenzen)\n2. backlog doc erstellen via CLI\n3. Sektionen: Overview, Lokal (Docker+Core-Venv), Multi-Release, CI/CD, Release, Reusability, Troubleshooting
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Testing & CI Guide als backlog doc (doc-6, 468 Zeilen) erstellt: lokale Entwicklung (Docker + Core-Venv), Multi-Release-Matrix, CI/CD-Workflows, Release-Prozess, Reusability-Template, Troubleshooting.
<!-- SECTION:FINAL_SUMMARY:END -->
