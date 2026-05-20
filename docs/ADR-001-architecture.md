# Architecture Decision Records — Rig for Red

> All central architecture decisions of the `rig_for_red` integration.

---

## ADR-001: Coordinator Pattern as Central Orchestrator

**Status:** Accepted

### Context

The integration needs to manage schedule listeners, dimming tasks, sunrise tracking, and light state. These state objects must be cleaned up properly when the config entry is unloaded. Without a central class, state would be scattered across `__init__.py` and several helper modules.

### Decision

`RigForRedCoordinator(DataUpdateCoordinator)` is the central class. It holds all runtime state variables (`is_active`, `_unsub_schedule`, `_unsub_restore`, `_unsub_sunrise`, `_dim_task`) and implements `async_setup()` and `async_unload()`. `__init__.py` only instantiates the coordinator and delegates everything to it.

### Consequences

- HA's `async_unload_entry` calls `coordinator.async_unload()` — clean teardown guaranteed, no task leaks possible
- Switch entity inherits via `CoordinatorEntity` and automatically reacts to state updates
- No manual listener management in `__init__.py` required
- Easier to test: coordinator can be instantiated directly without full HA entry lifecycle

---

## ADR-002: Staged Dimming Instead of Single Long Transition

**Status:** Accepted

### Context

HA's `light.turn_on` has a `transition` parameter for smooth transitions. A single call with `transition=dim_duration_minutes*60` (e.g. 3600 seconds) would be technically possible, but is not interruptible: HA does not provide an API to cancel a running transition.

### Decision

10 discrete `light.turn_on` calls (constant `DIM_STEPS=10`) with `transition=interval` for smoothing between steps. `asyncio.sleep(interval)` between steps with abort flag check (`if not self.is_active: return`) and `asyncio.CancelledError` handling.

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

- **Pro:** Interruptible at any time via `is_active=False` flag or `_dim_task.cancel()`
- **Pro:** Future features (pause, resume, dynamic step count) possible
- **Con:** 10 service calls instead of 1 — negligible on local HA instance
- `asyncio.CancelledError` must be caught in `_dim_lights`, otherwise exception propagation

---

## ADR-003: HA Event Helpers — No APScheduler

**Status:** Accepted

### Context

For time-based triggers in Python applications, libraries like APScheduler or `schedule` are common. An HA integration could include these as pip dependencies. Alternatively, HA provides its own event helper functions.

### Decision

Exclusively use HA's built-in event helpers with no external dependencies:

- `async_track_time_change(hass, callback, hour=H, minute=M, second=0)` for daily schedule and restore triggers
- `async_track_point_in_time(hass, callback, point_in_time)` for one-time sunrise trigger

`manifest.json` thus remains `"requirements": []`.

### Consequences

- **Pro:** Zero additional pip dependencies — simpler HACS setup, no version conflicts
- **Pro:** Correct timezone and DST handling via HA's own `dt_util`
- **Pro:** Cancellable via the callable returned by the functions
- **IMPORTANT:** Always call `async_track_time_change` with `second=0` — without this parameter the callback fires every second within the target minute
- Sunrise tracker must be re-registered after each restore (one-time `point_in_time` trigger)

---

## ADR-004: Adaptive Lighting Is Fully Optional

**Status:** Accepted

### Context

The primary user uses `adaptive_lighting` (HACS plugin) for automatic color temperature adjustment. The integration should pause AL on activation and re-enable it on restore. Other users may not have AL installed — a hard dependency would make the integration unusable for them.

### Decision

- `adaptive_lighting_switches` config field is optional: empty list `[]` is valid
- `dependencies: []` in `manifest.json` — no hard dependency
- All AL service calls (`adaptive_lighting.set_manual_control`, `switch.turn_on/off` for AL switches) are wrapped in `try/except Exception`
- On error: log `_LOGGER.warning(...)` and continue execution
- Restore order when AL is configured: first `adaptive_lighting.set_manual_control(manual_control=False)`, then `switch.turn_on` as fallback

### Consequences

- Integration works fully without AL (white light restore via `color_temp_kelvin` still active)
- Users with AL: configure `switch.adaptive_lighting_*` entity IDs manually in config
- AL integration can be added/removed at any time without restarting rig_for_red
- Tests need two fixture variants: with and without AL switches (`mock_config_entry` vs. `mock_config_entry_no_al`)

---

## ADR-005: Test Strategy with pytest-homeassistant-custom-component

**Status:** Accepted

### Context

HA integrations have specific testing requirements: async event loop, state machine, config entry lifecycle. Standard pytest without HA-specific fixtures cannot simulate HA internals correctly. Target is strict coverage ≥80%.

### Decision

- **Harness:** `pytest-homeassistant-custom-component` (official, daily updates, in sync with HA Core)
- **Time mocking:** `freezegun` for `datetime.now()` + `async_fire_time_changed` for HA scheduler events
- **Coverage:** `pytest-cov` with `--cov-fail-under=80` in CI (fails build if coverage drops below threshold)
- **CI requirements:** hassfest (manifest validation) + HACS validate + pytest — all three must pass
- `asyncio_mode = auto` in `pytest.ini` (no `@pytest.mark.asyncio` decorator needed)

### Consequences

- Real HA instance in tests: high test fidelity, no mock/production divergence
- Tests are slightly slower than pure unit tests (event loop overhead)
- Time-based tests require `freeze_time` + `async_fire_time_changed` combination — both needed because HA internally uses `hass.loop.time()` and Python's `datetime` in parallel
- See `docs/ADR-002-testing-strategy.md` for concrete code examples
