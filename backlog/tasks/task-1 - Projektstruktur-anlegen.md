---
id: TASK-1
title: Projektstruktur anlegen
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 19:56'
updated_date: '2026-05-20 20:35'
labels: []
milestone: M0 - Scaffold
dependencies: []
priority: high
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Alle Verzeichnisse und leere __init__.py Dateien anlegen. Basis-Konfigurationsdateien erstellen.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 custom_components/rig_for_red/__init__.py existiert
- [x] #2 custom_components/rig_for_red/manifest.json existiert (noch leer/minimal)
- [x] #3 tests/__init__.py existiert
- [x] #4 docs/ Verzeichnis existiert
- [x] #5 .github/workflows/ Verzeichnis existiert
- [x] #6 hacs.json existiert mit {"name": "Rig for Red", "render_readme": true}
- [x] #7 requirements_test.txt existiert mit: pytest, pytest-homeassistant-custom-component, pytest-asyncio, pytest-cov, freezegun
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Alle custom_components/rig_for_red/ Verzeichnisse anlegen\n2. __init__.py (leer/minimal) in allen Komponenten-Verzeichnissen\n3. tests/ __init__.py anlegen\n4. hacs.json schreiben\n5. .github/workflows/ Verzeichnis anlegen\n6. requirements_test.txt schreiben
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Verzeichnisstruktur angelegt: custom_components/rig_for_red/, tests/, docs/, .github/workflows/. Basis-Dateien erstellt: __init__.py (leer), hacs.json, requirements_test.txt
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Projektstruktur für Rig for Red Custom Component angelegt. Alle Verzeichnisse und leeren __init__.py-Dateien erstellt. hacs.json und requirements_test.txt mit den benötigten Test-Abhängigkeiten angelegt. docs/ und .github/workflows/ als Vorbereitung für spätere Meilensteine.
<!-- SECTION:FINAL_SUMMARY:END -->
