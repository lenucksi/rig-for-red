---
id: decision-1
title: 'ADR-001: Coordinator-Pattern als zentrale Orchestrierung'
date: '2026-05-20 20:16'
status: accepted
---
## Context

Die Integration muss Schedule-Listener, Dimm-Tasks, Sunrise-Tracking und Licht-State verwalten. Diese State-Objekte müssen beim Unload der Config Entry sauber abgebaut werden. Ohne zentrale Klasse würde sich State über `__init__.py` und mehrere Helfer-Module verteilen.

## Decision

`RigForRedCoordinator(DataUpdateCoordinator)` ist die zentrale Klasse. Sie hält alle Runtime-State-Variablen (`is_active`, `_unsub_schedule`, `_unsub_restore`, `_unsub_sunrise`, `_dim_task`) und implementiert `async_setup()` und `async_unload()`. `__init__.py` instanziiert nur den Coordinator und delegiert alles an ihn.

## Consequences

- HA's `async_unload_entry` ruft `coordinator.async_unload()` auf — sauberer Teardown garantiert, kein Task-Leak möglich
- Switch Entity erbt via `CoordinatorEntity` und reagiert automatisch auf State-Updates
- Kein manuelles Listener-Management in `__init__.py` nötig
- Einfacher zu testen: Coordinator direkt instanziierbar ohne vollständigen HA-Entry-Lifecycle
