---
id: TASK-38
title: Ausgeschaltete Lampen bei Aktivierung nicht einschalten
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-21 20:51'
updated_date: '2026-05-21 21:18'
labels:
  - coordinator
  - lights
  - behavior
dependencies: []
references:
  - custom_components/rig_for_red/coordinator.py
  - custom_components/rig_for_red/switch.py
  - custom_components/rig_for_red/const.py
modified_files:
  - custom_components/rig_for_red/coordinator.py
priority: high
ordinal: 39000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Aktuell schaltet async_activate() in coordinator.py alle konfigurierten Lampen auf Rot – auch die, die physisch aus sind. Erwünschtes Verhalten: Lampe die beim Aktivierungszeitpunkt AUS ist, bleibt AUS. Schaltet der Benutzer sie später manuell ein, geht sie in Rot an. Morgens bei Restore gehen alle aktiven Rot-Lampen auf Weiß zurück. War eine Lampe vor der Umschaltzeit schon an, wird sie rot zur Umschaltzeit (bleibt erhalten).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 async_activate() prüft state jeder Lampe; nur eingeschaltete werden rot gedimmt
- [ ] #2 State-Listener registriert für ausgeschaltete Lampen während aktiver Phase
- [ ] #3 Wenn eine ursprünglich ausgeschaltete Lampe während der aktiven Phase manuell eingeschaltet wird, geht sie sofort auf Rot (ohne Dim-Verzögerung)
- [ ] #4 async_restore() stellt alle betroffenen Lampen auf Weiß zurück (ursprünglich an + nachträglich eingeschaltet)
- [ ] #5 Wenn Benutzer eine Lampe während aktiver Phase manuell ausschaltet, bleibt sie aus (wird nicht bei Restore eingeschaltet)
- [ ] #6 Bestehende Tests passen weiterhin oder werden aktualisiert
- [ ] #7 Verhalten ist dokumentiert (README oder strings.json description)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. async_activate() um State-Check ergänzen (nur eingeschaltete Lampen dimmen)\n2. State-Tracking (on_lights, off_lights) im Coordinator\n3. async_track_state_change_event für ausgeschaltete Lampen registrieren\n4. Callback: bei manuellem Einschalten sofort Rot setzen\n5. async_restore() aktualisieren (nur aktive Lampen zurücksetzen, State-Listener cleanup)\n6. Tests laufen lassen
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented TASK-38: Ausgeschaltete Lampen bei Aktivierung nicht einschalten

Changes to coordinator.py:
- Added  and  imports
- Added , ,  tracking fields
-  now separates lights into on/off groups; only on lights get dimmed to red; off lights tracked in
- State change listener  handles: off->on (apply red immediately), on->off (remove from restore list)
-  only restores  to white; resets all tracking
-  only dims currently-on lights from the restore list
-  cleans up state listeners

Implemented coordinator.py changes for TASK-38

91 Tests pass (Docker). Coordinator refactored: async_activate filtert nach on/off, State-Listener für ausgeschaltete Lampen, async_restore nur tracked lights. Coverage coordinator.py von 36% auf 86%.

100 Tests pass (Docker), coordinator coverage 95% (vorher 92%). Neue Tests für off-lights, state-listener, user-turn-off.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Refactored coordinator.py: async_activate() filters lights by on/off state (only on-lights get dimmed red). State listeners track off-lights for instant red on manual turn-on. async_restore() only restores actively controlled lights. User-turned-off lights stay off. 91/91 tests pass, coordinator coverage 36%→86%.
<!-- SECTION:FINAL_SUMMARY:END -->
