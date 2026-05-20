# Architecture Decision Records — Rig for Red

> Alle zentralen Architekturentscheidungen der `rig_for_red` Integration.

---

## ADR-001: Coordinator-Pattern als zentrale Orchestrierung

**Status:** Accepted

### Context

Die Integration muss Schedule-Listener, Dimm-Tasks, Sunrise-Tracking und Licht-State verwalten. Diese State-Objekte müssen beim Unload der Config Entry sauber abgebaut werden. Ohne zentrale Klasse würde sich State über `__init__.py` und mehrere Helfer-Module verteilen.

### Decision

`RigForRedCoordinator(DataUpdateCoordinator)` ist die zentrale Klasse. Sie hält alle Runtime-State-Variablen (`is_active`, `_unsub_schedule`, `_unsub_restore`, `_unsub_sunrise`, `_dim_task`) und implementiert `async_setup()` und `async_unload()`. `__init__.py` instanziiert nur den Coordinator und delegiert alles an ihn.

### Consequences

- HA's `async_unload_entry` ruft `coordinator.async_unload()` auf — sauberer Teardown garantiert, kein Task-Leak möglich
- Switch Entity erbt via `CoordinatorEntity` und reagiert automatisch auf State-Updates
- Kein manuelles Listener-Management in `__init__.py` nötig
- Einfacher zu testen: Coordinator direkt instanziierbar ohne vollständigen HA-Entry-Lifecycle

---

## ADR-002: Gestufte Dimmung statt einzelner langer Transition

**Status:** Accepted

### Context

HA's `light.turn_on` hat einen `transition` Parameter für sanfte Übergänge. Ein einziger Aufruf mit `transition=dim_duration_minutes*60` (z.B. 3600 Sekunden) wäre technisch möglich, ist aber nicht unterbrechbar: HA bietet keine API um eine laufende Transition abzubrechen.

### Decision

10 diskrete `light.turn_on` Aufrufe (Konstante `DIM_STEPS=10`) mit jeweils `transition=interval` für Glättung zwischen den Schritten. `asyncio.sleep(interval)` zwischen Steps mit Abbruch-Flag-Check (`if not self.is_active: return`) und `asyncio.CancelledError` Handling.

```python
interval = (dim_duration_minutes * 60) / DIM_STEPS
for i in range(1, DIM_STEPS + 1):
    if not self.is_active:
        return
    brightness = int(start - (start - target) * i / DIM_STEPS)
    await hass.services.async_call("light", "turn_on", {
        "rgb_color": RED_RGB, "brightness": brightness, "transition": interval
    })
    await asyncio.sleep(interval)
```

### Consequences

- **Pro:** Jederzeit abbrechbar via `is_active=False` Flag oder `_dim_task.cancel()`
- **Pro:** Zukünftige Features (Pause, Resume, dynamische Step-Anzahl) möglich
- **Con:** 10 Service-Calls statt 1 — bei lokaler HA-Instanz vernachlässigbar
- `asyncio.CancelledError` muss in `_dim_lights` gefangen werden, sonst Exception-Propagation

---

## ADR-003: HA Event Helpers — kein APScheduler

**Status:** Accepted

### Context

Für zeitbasierte Trigger in Python-Anwendungen sind Bibliotheken wie APScheduler oder `schedule` üblich. Eine HA-Integration könnte diese als pip-Dependency einbinden. Alternativ bietet HA eigene Event-Helper-Funktionen.

### Decision

Ausschließlich HA-eigene Event Helpers ohne externe Dependencies:

- `async_track_time_change(hass, callback, hour=H, minute=M, second=0)` für tägliche Schedule- und Restore-Trigger
- `async_track_point_in_time(hass, callback, point_in_time)` für einmaligen Sunrise-Trigger

`manifest.json` bleibt damit `"requirements": []`.

### Consequences

- **Pro:** Zero additional pip dependencies — einfacheres HACS-Setup, keine Versions-Konflikte
- **Pro:** Korrekte Timezone- und DST-Behandlung durch HA's eigene `dt_util`
- **Pro:** Cancellable via den von den Funktionen zurückgegebenen callable
- **WICHTIG:** `async_track_time_change` immer mit `second=0` aufrufen — ohne diesen Parameter feuert der Callback jede Sekunde innerhalb der Ziel-Minute
- Sunrise-Tracker muss nach jedem Restore neu registriert werden (einmaliger `point_in_time` Trigger)

---

## ADR-004: Adaptive Lighting ist vollständig optional

**Status:** Accepted

### Context

Der primäre Nutzer verwendet `adaptive_lighting` (HACS-Plugin) zur automatischen Lichttemperatur-Anpassung. Die Integration soll AL beim Aktivieren pausieren und beim Restore reaktivieren. Andere Nutzer könnten AL nicht installiert haben — ein hard dependency würde die Integration für sie unbrauchbar machen.

### Decision

- `adaptive_lighting_switches` Konfigurationsfeld ist optional: leere Liste `[]` ist valide
- `dependencies: []` in `manifest.json` — kein hard dependency
- Alle AL-Service-Calls (`adaptive_lighting.set_manual_control`, `switch.turn_on/off` für AL-Switches) werden in `try/except Exception` gewrapped
- Bei Fehler: `_LOGGER.warning(...)` ausgeben, aber Ausführung fortsetzen
- Restore-Reihenfolge wenn AL konfiguriert: erst `adaptive_lighting.set_manual_control(manual_control=False)`, dann `switch.turn_on` als Fallback

### Consequences

- Integration funktioniert vollständig ohne AL (Weißlicht-Restore via `color_temp_kelvin` weiterhin aktiv)
- Nutzer mit AL: konfigurieren `switch.adaptive_lighting_*` Entity-IDs manuell in der Config
- AL-Integration kann jederzeit ohne Neustart der rig_for_red Integration hinzugefügt/entfernt werden
- Tests brauchen zwei Fixture-Varianten: mit und ohne AL-Switches (`mock_config_entry` vs. `mock_config_entry_no_al`)

---

## ADR-005: Test-Strategie mit pytest-homeassistant-custom-component

**Status:** Accepted

### Context

HA-Integrationen haben spezifische Test-Anforderungen: async Event Loop, State Machine, Config Entry Lifecycle. Standard-pytest ohne HA-spezifische Fixtures kann HA-Internals nicht korrekt simulieren. Ziel ist strikte Coverage ≥80%.

### Decision

- **Harness:** `pytest-homeassistant-custom-component` (offiziell, tägliche Updates, synchron mit HA-Core)
- **Zeit-Mocking:** `freezegun` für `datetime.now()` + `async_fire_time_changed` für HA-Scheduler-Events
- **Coverage:** `pytest-cov` mit `--cov-fail-under=80` im CI (bricht Build bei Unterschreitung ab)
- **CI-Pflicht:** hassfest (manifest-Validierung) + HACS validate + pytest — alle drei müssen grün sein
- `asyncio_mode = auto` in `pytest.ini` (kein `@pytest.mark.asyncio` Decorator nötig)

### Consequences

- Echte HA-Instanz in Tests: hohe Test-Fidelity, keine Mock/Prod-Divergenz
- Tests sind etwas langsamer als reine Unit-Tests (Event Loop Overhead)
- Zeit-basierte Tests erfordern `freeze_time` + `async_fire_time_changed` Kombination — beide nötig, da HA intern `hass.loop.time()` und Python's `datetime` parallel nutzt
- Siehe `docs/ADR-002-testing-strategy.md` für konkrete Code-Beispiele
