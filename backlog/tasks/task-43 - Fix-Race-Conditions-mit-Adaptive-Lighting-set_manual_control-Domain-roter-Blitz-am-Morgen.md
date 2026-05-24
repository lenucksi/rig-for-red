---
id: TASK-43
title: >-
  Fix: Race Conditions mit Adaptive Lighting (set_manual_control Domain + roter
  Blitz am Morgen)
status: Done
assignee: []
created_date: '2026-05-24 11:05'
updated_date: '2026-05-24 12:25'
labels:
  - coordinator
  - adaptive_lighting
  - bug
dependencies: []
references:
  - custom_components/rig_for_red/coordinator.py
  - >-
    /home/jo/kit/homeass/adaptive-lighting/custom_components/adaptive_lighting/switch.py
modified_files:
  - custom_components/rig_for_red/coordinator.py
priority: high
ordinal: 44000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Zwei Race-Condition-Bugs in der AL-Interaktion von async_activate und _on_tracked_light_change:
1. set_manual_control wird auf falscher Domain (switch statt adaptive_lighting) aufgerufen + lights-Parameter fehlt → schlägt immer feil → AL-Interval-Rest-Tasks überschreiben Rot nach async_activate
2. _on_tracked_light_change setzt Licht kurz vor Sonnenaufgang auf Rot → direkt danach async_restore → warmweiß → AL überschreibt auf kaltweiß → user sieht roten Blitz
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 set_manual_control wird mit korrekter Domain 'adaptive_lighting' (statt 'switch') aufgerufen
- [x] #2 set_manual_control enthält den lights-Parameter mit self._lights
- [x] #3 set_manual_control mit manual_control=True wird VOR switch.turn_off aufgerufen (damit AL-Interceptor Lights sofort skippt)
- [x] #4 set_manual_control mit manual_control=False wird NACH Light-Restore und VOR switch.turn_on aufgerufen
- [x] #5 Optionaler asyncio.sleep(0.5) flusht AL-Event-Loop-Reste vor dem Rot-Setzen
- [x] #6 _on_tracked_light_change prüft ob Restore-Zeit (Sonnenaufgang/fixed) innerhalb 10 Minuten liegt → dann kein Rot
- [x] #7 Bei nahendem Restore wird das Licht trotzdem zu _lights_to_restore hinzugefügt
- [x] #8 Alle bestehenden Tests passieren
- [x] #9 Neue Tests für: set_manual_control korrekte Domain, imminent-restore check in _on_tracked_light_change
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. In async_activate(): set_manual_control auf 'adaptive_lighting' Domain fixen + 'lights': self._lights Parameter hinzufügen. Aufruf VOR switch.turn_off. Danach asyncio.sleep(0.5) um AL-Rest-Tasks aus Event-Queue zu flushen.

2. In async_restore(): set_manual_control Domain fixen + lights Parameter. Aufruf NACH light-restore (2700K) und VOR switch.turn_on. manual_control=False → AL resetet manual_control + adaptiert sofort beim turn_on.

3. In _on_tracked_light_change(): neuen Check einbauen: wenn entity_id in _lights_waiting_for_red, prüfe ob restore_time oder next_sunrise innerhalb 10 Minuten liegt. Wenn ja: Licht in _lights_to_restore aufnehmen (damit restore es erwischt) aber KEIN Rot setzen.

4. Neue Methode _is_restore_imminent() im Coordinator: prüft self._restore_at_sunrise + self._restore_time gegen current time mit 10-Minuten-Toleranz.

5. Tests ergänzen: test_activate_set_manual_control_correct_domain, test_tracked_light_no_red_when_restore_imminent, test_is_restore_imminent_true/false
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Two race-condition bugs in Adaptive Lighting interaction fixed:

1. set_manual_control called with wrong domain 'switch' instead of 'adaptive_lighting' + missing 'lights' param → silently failed. Fixed in both async_activate and async_restore. Reordered AL sequence: set_manual_control(manual_control=True) now runs BEFORE switch.turn_off, so AL's service interceptor skips Rig-for-Red's lights immediately. Added asyncio.sleep(0.5) after turn_off to flush any remaining AL tasks from event loop.

2. Red flash in morning: _on_tracked_light_change set lights to red even when restore was imminent. Fixed by adding _is_restore_imminent() check: if sunrise or fixed restore time is within 10 min, the light is added to _lights_to_restore but NOT set to red.

New tests: test_off_light_no_red_when_sunrise_imminent, test_off_light_no_red_when_restore_time_imminent.

102 tests pass (Docker), coordinator.py coverage 94%.
<!-- SECTION:FINAL_SUMMARY:END -->
