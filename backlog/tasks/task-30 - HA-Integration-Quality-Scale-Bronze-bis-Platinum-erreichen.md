---
id: TASK-30
title: 'HA Integration Quality Scale: Bronze bis Platinum erreichen'
status: To Do
assignee: []
created_date: '2026-05-21 13:14'
labels: []
dependencies: []
references:
  - custom_components/rig_for_red/config_flow.py
  - custom_components/rig_for_red/__init__.py
  - custom_components/rig_for_red/coordinator.py
  - custom_components/rig_for_red/switch.py
  - custom_components/rig_for_red/strings.json
  - docs/guides/doc-5
documentation:
  - guides/doc-5
priority: high
ordinal: 30000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Rig for Red auf alle vier Tiers der Integration Quality Scale bringen. Doku und Gap-Analyse in doc-5.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 common-modules: Prüfen ob Patterns aus config_flow/coordinator in shared modules ausgelagert werden können
- [ ] #2 config-flow-test-coverage: entity_not_found + alle Error-Pfade in config_flow testen
- [ ] #3 dependency-transparency: Dependencies in manifest.json + docs dokumentieren
- [ ] #4 runtime-data: entry.runtime_data statt hass.data[DOMAIN] in __init__.py + coordinator.py
- [ ] #5 test-before-configure: async_step_user testet ob Entity-Zugriff möglich ist
- [ ] #6 test-before-setup: async_setup_entry validiert coordinator Init
- [ ] #7 unique-config-entry: unique_id in config_flow setzen + _abort_if_unique_id_configured
- [ ] #8 brands: logo.png + icon.png ins Repo-Root
- [ ] #9 action-exceptions: Service-Actions werfen HomeAssistantError bei Fehlern
- [ ] #10 entity-unavailable: Switch als unavailable markieren wenn Coordinator nicht bereit
- [ ] #11 integration-owner: CODEOWNERS prüfen/aktualisieren
- [ ] #12 test-coverage: Coverage auf >95% bringen (ca. 10-15 neue Tests)
- [ ] #13 docs-configuration-parameters + docs-installation-parameters in README ergänzen
- [ ] #14 devices: Device Registry nutzen für die Integration
- [ ] #15 diagnostics: Diagnostics-Dump implementieren
- [ ] #16 entity-category: Switch als CONFIG oder DIAGNOSTIC kategorisieren
- [ ] #17 exception-translations: Fehlermeldungen via HomeAssistantError + translation_key
- [ ] #18 icon-translations: Icon via _attr_icon oder icon_translations
- [ ] #19 reconfiguration-flow: async_step_reconfigure implementieren
- [ ] #20 docs-use-cases, docs-examples, docs-troubleshooting in README
- [ ] #21 strict-typing: Vollständige Type Annotations + mypy im CI
<!-- AC:END -->
