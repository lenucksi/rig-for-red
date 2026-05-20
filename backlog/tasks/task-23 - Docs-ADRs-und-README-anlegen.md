---
id: TASK-23
title: 'Docs, ADRs und README anlegen'
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 20:08'
updated_date: '2026-05-20 20:42'
labels: []
milestone: M6 - CI und Docs
dependencies:
  - TASK-1
priority: medium
ordinal: 23000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Dokumentation anlegen: ADR-Dateien, Referenz-Links und README.

docs/ADR-001-architecture.md:
- ADR-001: Coordinator-Pattern (Status: Accepted)
- ADR-002: Gestufte Dimmung statt einzelner Transition
- ADR-003: HA Event Helpers, kein APScheduler
- ADR-004: Adaptive Lighting ist optional (kein hard dependency)
- ADR-005: Test-Strategie (pytest-homeassistant-custom-component + freezegun)
Jeder ADR: Context, Decision, Consequences Sections

docs/ADR-002-testing-strategy.md:
- Test-Pyramide: unit/integration/E2E
- Was gemockt wird vs. was real ist
- Coverage-Ziel: >=80%
- CI-Anforderungen

docs/reference-links.md:
Alle Links aus dem Plan (HA Dev Docs, AL GitHub, pytest-ha, HACS, usw.)

README.md:
- Kurzbeschreibung: 'Rig for Red - submarine night mode for Home Assistant'
- Voraussetzungen (HA Version >= 2025.3.0, optional: adaptive_lighting)
- Installation via HACS
- Konfigurationsfelder als Tabelle
- Zigbee-Button Integration (Verwendungsbeispiel mit service call)
- adaptive_lighting Hinweis: optional, wird erkannt und deaktiviert/reaktiviert wenn konfiguriert
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 docs/ADR-001-architecture.md existiert mit allen 5 ADRs
- [x] #2 docs/ADR-002-testing-strategy.md existiert
- [x] #3 docs/reference-links.md existiert mit min. 10 Links
- [x] #4 README.md existiert mit Installations- und Konfigurationsabschnitt
- [x] #5 README.md enthält Hinweis dass adaptive_lighting optional ist
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Dokumentation erstellt: ADR-001-architecture.md (5 ADRs), ADR-002-testing-strategy.md, reference-links.md (21 Links), README.md mit Installations/Konfigurationsabschnitt.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Dokumentation angelegt: ADR-001 mit 5 Architektur-Entscheidungen, ADR-002 Test-Strategie, reference-links.md mit 21 HA/HACS-Links, README.md mit Beschreibung, Installation, Konfigurationstabelle und Zigbee-Beispiel.
<!-- SECTION:FINAL_SUMMARY:END -->
