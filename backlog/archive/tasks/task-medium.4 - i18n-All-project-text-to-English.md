---
id: TASK-MEDIUM.4
title: 'i18n: All project text to English'
status: To Do
assignee: []
created_date: '2026-05-20 21:28'
labels:
  - docs
  - i18n
milestone: M6 - CI und Docs
dependencies: []
parent_task_id: TASK-MEDIUM
ordinal: 29000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Sämtlicher benutzersichtiger Text (strings.json, Dokumentation, README, ADRs) wird auf Englisch umgestellt. Home Assistant Custom Components haben strings.json als Fallback — das muss Englisch sein.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 strings.json: config flow title/description/data/error keys alle auf Englisch
- [ ] #2 translations/en.json aktualisiert (oder überflüssig wenn strings.json == English)
- [ ] #3 README.md vollständig auf Englisch (Titel, Features, Install, Config, Dev)
- [ ] #4 docs/ADR-001-architecture.md auf Englisch
- [ ] #5 docs/ADR-002-testing-strategy.md auf Englisch
- [ ] #6 docs/reference-links.md Titel/Beschreibungen auf Englisch
- [ ] #7 Alle _LOGGER-Nachrichten in Python-Code auf Englisch (bereits der Fall — verifizieren)
<!-- AC:END -->
