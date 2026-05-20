---
id: doc-3
title: Testing Strategy
type: guide
created_date: '2026-05-20 20:10'
---

# Testing Strategy

## Ziel

Strikte Test-Coverage ≥80% für alle Produktionsdateien unter `custom_components/rig_for_red/`.

## Technologie-Stack

| Tool | Zweck |
|------|-------|
| `pytest-homeassistant-custom-component` | HA-Instanz in Tests, MockConfigEntry, async_fire_time_changed |
| `freezegun` | `datetime.now()` und `time.time()` einfrieren für deterministische Zeitsteuerung |
| `pytest-cov` | Coverage-Messung und -Report |
| `pytest-asyncio` (via asyncio_mode=auto) | Async-Testfunktionen ohne `@pytest.mark.asyncio` Decorator |

## Datei-Struktur

```
tests/
├── __init__.py          # leer
├── conftest.py          # gemeinsame Fixtures
├── test_init.py         # async_setup_entry, async_unload_entry, services
├── test_config_flow.py  # Form, Validierung, Entry-Erstellung
├── test_coordinator.py  # Schedule, Activate, Dim, Restore, Sunrise
└── test_switch.py       # Switch Entity State, turn_on/off
```

## Fixture-Design

- **`mock_config_entry`**: Standard-Config mit AL-Switches
- **`mock_config_entry_no_al`**: Config ohne AL (leere Liste) — testet Optional-Pfad
- **`mock_light_states`**: Setzt realistische HA-States für light.test_light_1/2
- **`mock_sun_state`**: Setzt sun.sun mit next_rising Attribut
- **`setup_integration`**: Vollständiger Setup inkl. add_to_hass + async_setup

## Zeit-basierte Tests

```python
from freezegun import freeze_time
from pytest_homeassistant_custom_component.common import async_fire_time_changed
from homeassistant.util import dt as dt_util

async def test_schedule_fires(hass, setup_integration):
    # Mittwoch 23:00 einfrieren
    with freeze_time('2026-05-21 23:00:00'):  # 2026-05-21 ist ein Mittwoch
        async_fire_time_changed(hass, dt_util.now())
        await hass.async_block_till_done()
    coordinator = hass.data['rig_for_red'][setup_integration.entry_id]
    assert coordinator.is_active
```

## Service-Call Verification

```python
from unittest.mock import patch, AsyncMock

async def test_activate_calls_light(hass, setup_integration):
    with patch.object(hass.services, 'async_call', new_callable=AsyncMock) as mock_call:
        coordinator = hass.data['rig_for_red'][setup_integration.entry_id]
        await coordinator.async_activate()
        # Prüfen ob light.turn_on mit rgb_color aufgerufen wurde
        light_calls = [c for c in mock_call.call_args_list if c[0] == ('light', 'turn_on')]
        assert any(c[1].get('rgb_color') == [255, 0, 0] for c in light_calls)
```

## Coverage-Ziele

| Datei | Ziel |
|-------|------|
| `coordinator.py` | ≥85% |
| `config_flow.py` | ≥90% |
| `switch.py` | ≥90% |
| `__init__.py` | ≥80% |
| `const.py` | 100% (nur Konstanten) |

## CI-Konfiguration

```bash
pytest tests/ \
  --cov=custom_components/rig_for_red \
  --cov-report=xml \
  --cov-fail-under=80
```

CI bricht bei `< 80%` Coverage ab (`--cov-fail-under=80`).

## Was wird gemockt vs. was ist real

| Gemockt | Real |
|---------|------|
| `hass.services.async_call` (für Verifikation) | HA Event Loop |
| `sun.sun` State (via `hass.states.async_set`) | Coordinator Lifecycle |
| Light entity States | Config Entry System |
| Zeit (via freezegun) | DataUpdateCoordinator |
