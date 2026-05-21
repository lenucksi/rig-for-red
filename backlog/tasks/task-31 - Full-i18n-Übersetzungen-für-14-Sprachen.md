---
id: TASK-31
title: 'Full i18n: Übersetzungen für 14 Sprachen'
status: Done
assignee: []
created_date: '2026-05-21 13:14'
updated_date: '2026-05-21 15:48'
labels: []
dependencies: []
references:
  - custom_components/rig_for_red/strings.json
  - custom_components/rig_for_red/translations/
  - custom_components/rig_for_red/config_flow.py
documentation:
  - guides/doc-4
priority: medium
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Alle user-facing Strings der Integration in 14 Sprachen übersetzen: config flow fields/errors, selector options (Wochentage), entity name. Grundlage ist strings.json (English). Übersetzungen in translations/*.json ablegen.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 translations/de.json: Alle Keys auf Deutsch übersetzen
- [x] #2 translations/fr.json: Alle Keys auf Französisch übersetzen
- [x] #3 translations/es.json: Alle Keys auf Spanisch übersetzen
- [x] #4 translations/it.json: Alle Keys auf Italienisch übersetzen
- [x] #5 translations/pt.json: Alle Keys auf Portugiesisch übersetzen
- [x] #6 translations/nl.json: Alle Keys auf Niederländisch übersetzen
- [x] #7 translations/da.json: Alle Keys auf Dänisch übersetzen
- [x] #8 translations/sv.json: Alle Keys auf Schwedisch übersetzen
- [x] #9 translations/nb.json: Alle Keys auf Norwegisch (Bokmål) übersetzen
- [x] #10 translations/fi.json: Alle Keys auf Finnisch übersetzen
- [x] #11 translations/pl.json: Alle Keys auf Polnisch übersetzen
- [x] #12 translations/zh-TW.json: Alle Keys auf Traditionelles Chinesisch (ROC) übersetzen
- [x] #13 translations/hi.json: Alle Keys auf Hindi übersetzen
- [x] #14 translations/ta.json: Alle Keys auf Tamil übersetzen
- [x] #15 Test: Übersetzungen laden via async_get_translations und prüfen ob alle Keys vorhanden sind
- [x] #16 Test: Fallback-Verhalten prüfen (fehlende Keys fallen auf strings.json zurück)
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Alle 14 Übersetzungsdateien komplett (29/29 Keys). translations/en.json recreated (config-only — selector/entity in en.json würden component loading brechen). 3 Test-Kategorien (config, selector, entity) × 15 Sprachen + Fallback-Test. 91 Tests passieren insgesamt.
<!-- SECTION:FINAL_SUMMARY:END -->
