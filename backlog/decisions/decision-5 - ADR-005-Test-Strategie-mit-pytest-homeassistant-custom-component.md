---
id: decision-5
title: 'ADR-005: Test-Strategie mit pytest-homeassistant-custom-component'
date: '2026-05-20 20:16'
status: accepted
---
## Context

HA-Integrationen haben spezifische Test-Anforderungen: async Event Loop, State Machine, Config Entry Lifecycle. Standard-pytest ohne HA-spezifische Fixtures kann HA-Internals nicht korrekt simulieren. Ziel ist strikte Coverage ≥80%.

## Decision

- **Harness**: `pytest-homeassistant-custom-component` (offiziell, tägliche Updates, synchron mit HA-Core)
- **Zeit-Mocking**: `freezegun` für `datetime.now()` + `async_fire_time_changed` für HA-Scheduler-Events
- **Coverage**: `pytest-cov` mit `--cov-fail-under=80` im CI (bricht Build bei Unterschreitung ab)
- **CI-Pflicht**: hassfest (manifest-Validierung) + HACS validate + pytest — alle drei müssen grün sein
- `asyncio_mode = auto` in `pytest.ini` (kein `@pytest.mark.asyncio` Decorator nötig)

## Consequences

- Echte HA-Instanz in Tests: hohe Test-Fidelity, keine Mock/Prod-Divergenz
- Tests sind etwas langsamer als reine Unit-Tests (Event Loop Overhead)
- Zeit-basierte Tests erfordern `freeze_time` + `async_fire_time_changed` Kombination — beide nötig, da HA intern `hass.loop.time()` und Python's `datetime` parallel nutzt
- Referenz: `doc-3` (Testing Strategy) mit konkreten Code-Beispielen für Zeit-Tests und Service-Call-Verifikation
