---
id: decision-3
title: 'ADR-003: HA Event Helpers — kein APScheduler'
date: '2026-05-20 20:16'
status: accepted
---
## Context

Für zeitbasierte Trigger in Python-Anwendungen sind Bibliotheken wie APScheduler oder `schedule` üblich. Eine HA-Integration könnte diese als pip-Dependency einbinden. Alternativ bietet HA eigene Event-Helper-Funktionen.

## Decision

Ausschließlich HA-eigene Event Helpers ohne externe Dependencies:
- `async_track_time_change(hass, callback, hour=H, minute=M, second=0)` für tägliche Schedule- und Restore-Trigger
- `async_track_point_in_time(hass, callback, point_in_time)` für einmaligen Sunrise-Trigger

`manifest.json` bleibt damit `"requirements": []`.

## Consequences

- **Pro**: Zero additional pip dependencies — einfacheres HACS-Setup, keine Versions-Konflikte
- **Pro**: Korrekte Timezone- und DST-Behandlung durch HA's eigene `dt_util`
- **Pro**: Cancellable via den von den Funktionen zurückgegebenen callable
- **WICHTIG**: `async_track_time_change` immer mit `second=0` aufrufen — ohne diesen Parameter feuert der Callback jede Sekunde innerhalb der Ziel-Minute
- Sunrise-Tracker muss nach jedem Restore neu registriert werden (einmaliger `point_in_time` Trigger)
