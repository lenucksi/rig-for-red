---
id: TASK-16
title: Custom Services registrieren
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 20:07'
updated_date: '2026-05-20 20:38'
labels: []
milestone: M4 - Switch Entity und Services
dependencies:
  - TASK-8
priority: medium
ordinal: 16000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Zwei Custom Services für die Integration registrieren. Ermöglicht Aufruf per HA-Skript oder Zigbee-Button-Automation.

In async_setup_entry (__init__.py) hinzufügen:
    async def handle_trigger_rig(call):
        coordinator = hass.data[DOMAIN][entry.entry_id]
        await coordinator.async_activate()
    
    async def handle_restore_lights(call):
        coordinator = hass.data[DOMAIN][entry.entry_id]
        await coordinator.async_restore()
    
    hass.services.async_register(DOMAIN, 'trigger_rig', handle_trigger_rig)
    hass.services.async_register(DOMAIN, 'restore_lights', handle_restore_lights)

Datei services.yaml in custom_components/rig_for_red/:
    trigger_rig:
      name: Trigger Rig for Red
      description: Aktiviert sofort den Rig for Red Modus (Rotlicht + Dimmen)
    restore_lights:
      name: Lichter wiederherstellen  
      description: Stellt Weißlicht wieder her und reaktiviert Adaptive Lighting (falls konfiguriert)

Verwendungsbeispiel in HA-Automation (für Zigbee-Button):
    service: rig_for_red.trigger_rig
    # Kein target nötig
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 test_services_registered: nach setup_entry → hass.services.has_service(DOMAIN, 'trigger_rig') == True
- [x] #2 test_services_registered: hass.services.has_service(DOMAIN, 'restore_lights') == True
- [x] #3 test_trigger_rig_service: service call 'trigger_rig' → coordinator.async_activate() aufgerufen
- [x] #4 test_restore_lights_service: service call 'restore_lights' → coordinator.async_restore() aufgerufen
- [x] #5 services.yaml existiert mit beiden Services dokumentiert
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
trigger_rig und restore_lights Services in __init__.py registriert. services.yaml erstellt.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Custom Services trigger_rig und restore_lights in __init__.py registriert (async_register/async_remove). services.yaml mit beiden Service-Definitionen erstellt.
<!-- SECTION:FINAL_SUMMARY:END -->
