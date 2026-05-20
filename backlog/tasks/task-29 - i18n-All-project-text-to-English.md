---
id: TASK-29
title: 'i18n: All project text to English'
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 21:28'
updated_date: '2026-05-20 21:37'
labels:
  - docs
  - i18n
milestone: M6 - CI und Docs
dependencies: []
priority: medium
ordinal: 29000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Sämtlicher benutzersichtiger Text (strings.json, Dokumentation, README, ADRs) wird auf Englisch umgestellt. Home Assistant Custom Components haben strings.json als Fallback — das muss Englisch sein.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 strings.json: config flow title/description/data/error keys alle auf Englisch
- [ ] #2 translations/en.json aktualisiert oder entfernt
- [x] #3 README.md vollständig auf Englisch
- [x] #4 docs/ADR-001-architecture.md auf Englisch
- [x] #5 docs/ADR-002-testing-strategy.md auf Englisch
- [x] #6 docs/reference-links.md Titel/Beschreibungen auf Englisch
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Alle Texte auf Englisch umgestellt: strings.json (neu = translations/en.json), README.md, ADRs, reference-links. translations/en.json ist jetzt redundant (identisch mit strings.json) — kann später entfernt werden.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
i18n: Complete project translation from German to English. strings.json serves as the HA fallback (English). README, all ADRs, reference-links fully translated. English log messages verified (already were English).
<!-- SECTION:FINAL_SUMMARY:END -->
