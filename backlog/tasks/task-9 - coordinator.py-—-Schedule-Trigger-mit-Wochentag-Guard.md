---
id: TASK-9
title: coordinator.py — Schedule-Trigger mit Wochentag-Guard
status: Done
assignee: []
created_date: '2026-05-20 20:01'
updated_date: '2026-05-20 20:37'
labels: []
milestone: M3 - Coordinator Kernlogik
dependencies:
  - TASK-7
priority: high
ordinal: 9000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Die _schedule_trigger Callback-Methode implementieren.

def _schedule_trigger(self, now: datetime) -> None:
    # Wochentag prüfen (now.strftime('%a').lower() gibt 'mon', 'tue' etc.)
    day_abbr = now.strftime('%a').lower()
    if day_abbr not in self._schedule_days:
        return
    # Doppelt-Aktivierung verhindern
    if self.is_active:
        return
    # Als Task starten (nicht await, wir sind in einem sync callback)
    self.hass.async_create_task(self.async_activate())

WICHTIG: now.strftime('%a') gibt englische Wochentag-Abkürzungen: Mon, Tue, Wed, Thu, Fri, Sat, Sun.
Diese müssen lowercase gemacht werden: 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun' — identisch mit WEEKDAYS Konstante.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 test_schedule_trigger_correct_day: _schedule_trigger mit now=Mittwoch 23:00, schedule_days=['wed'] → async_activate wird aufgerufen
- [x] #2 test_schedule_trigger_wrong_day: _schedule_trigger mit now=Donnerstag, schedule_days=['mon','tue','wed'] → async_activate wird NICHT aufgerufen
- [x] #3 test_schedule_trigger_already_active: is_active=True → async_activate wird NICHT aufgerufen
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
_schedule_trigger implementiert mit Wochentag-Guard (strftime('%a').lower()) und is_active-Doppelaktivierungsschutz.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Schedule-Trigger mit Wochentag-Guard in coordinator.py implementiert. Prüft Wochentag gegen konfigurierte schedule_days und verhindert Doppelaktivierung.
<!-- SECTION:FINAL_SUMMARY:END -->
