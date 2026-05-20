# Testing Strategy — Rig for Red

> Testing strategy for the `rig_for_red` Home Assistant Custom Component.

## Goal

Strict test coverage ≥80% for all production files under `custom_components/rig_for_red/`.

## Technology Stack

| Tool | Purpose |
|------|---------|
| `pytest-homeassistant-custom-component` | HA instance in tests, MockConfigEntry, async_fire_time_changed |
| `freezegun` | Freeze `datetime.now()` and `time.time()` for deterministic time control |
| `pytest-cov` | Coverage measurement and reporting |
| `pytest-asyncio` (via asyncio_mode=auto) | Async test functions without `@pytest.mark.asyncio` decorator |

## File Structure

```
tests/
├── __init__.py          # empty
├── conftest.py          # shared fixtures
├── test_init.py         # async_setup_entry, async_unload_entry, services
├── test_config_flow.py  # Form, validation, entry creation
├── test_coordinator.py  # Schedule, activate, dim, restore, sunrise
└── test_switch.py       # Switch entity state, turn_on/off
```

## Fixture Design

- **`mock_config_entry`**: Standard config with AL switches
- **`mock_config_entry_no_al`**: Config without AL (empty list) — tests optional path
- **`mock_light_states`**: Sets realistic HA states for light.test_light_1/2
- **`mock_sun_state`**: Sets sun.sun with next_rising attribute
- **`setup_integration`**: Full setup including add_to_hass + async_setup

## Time-Based Tests

```python
from freezegun import freeze_time
from pytest_homeassistant_custom_component.common import async_fire_time_changed
from homeassistant.util import dt as dt_util

async def test_schedule_fires(hass, setup_integration):
    # Freeze at Wednesday 23:00
    with freeze_time('2026-05-21 23:00:00'):  # 2026-05-21 is a Wednesday
        async_fire_time_changed(hass, dt_util.now())
        await hass.async_block_till_done()
    coordinator = hass.data['rig_for_red'][setup_integration.entry_id]
    assert coordinator.is_active
```

## Service Call Verification

```python
from unittest.mock import patch, AsyncMock

async def test_activate_calls_light(hass, setup_integration):
    with patch.object(hass.services, 'async_call', new_callable=AsyncMock) as mock_call:
        coordinator = hass.data['rig_for_red'][setup_integration.entry_id]
        await coordinator.async_activate()
        # Verify light.turn_on was called with rgb_color
        light_calls = [c for c in mock_call.call_args_list if c[0] == ('light', 'turn_on')]
        assert any(c[1].get('rgb_color') == [255, 0, 0] for c in light_calls)
```

## Coverage Targets

| File | Target |
|------|--------|
| `coordinator.py` | ≥85% |
| `config_flow.py` | ≥90% |
| `switch.py` | ≥90% |
| `__init__.py` | ≥80% |
| `const.py` | 100% (constants only) |

## CI Configuration

```bash
pytest tests/ \
  --cov=custom_components/rig_for_red \
  --cov-report=xml \
  --cov-fail-under=80
```

CI fails at `< 80%` coverage (`--cov-fail-under=80`).

## What Is Mocked vs. What Is Real

| Mocked | Real |
|--------|------|
| `hass.services.async_call` (for verification) | HA event loop |
| `sun.sun` state (via `hass.states.async_set`) | Coordinator lifecycle |
| Light entity states | Config entry system |
| Time (via freezegun) | DataUpdateCoordinator |

## Test Pyramid

```
     /\
    /  \         Manual / E2E tests (rare)
   /    \
  /------\       Integration tests (test_coordinator.py)
 /        \
/----------\     Unit tests (config_flow, switch, const)
```

- **Unit tests:** Config validation, switch state transitions, constants
- **Integration tests:** Coordinator lifecycle, dim logic, schedule triggers, sunrise restore
- **E2E:** Not automated — manual validation with real HA instance
