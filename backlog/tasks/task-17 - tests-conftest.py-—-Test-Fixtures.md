---
id: TASK-17
title: tests/conftest.py — Test-Fixtures
status: Done
assignee:
  - '@agent-k'
created_date: '2026-05-20 20:07'
updated_date: '2026-05-20 20:42'
labels: []
milestone: M5 - Tests
dependencies:
  - TASK-8
  - TASK-15
priority: high
ordinal: 17000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Alle gemeinsamen Test-Fixtures in tests/conftest.py anlegen.

Benötigte Imports:
from pytest_homeassistant_custom_component.common import MockConfigEntry
import pytest
from homeassistant.core import HomeAssistant

Fixtures:

@pytest.fixture
def mock_config_entry_data():
    return {
        'lights': ['light.test_light_1', 'light.test_light_2'],
        'schedule_days': ['mon', 'tue', 'wed', 'thu', 'fri'],
        'schedule_time': '23:00',
        'dim_duration_minutes': 60,
        'restore_at_sunrise': True,
        'restore_time': None,
        'adaptive_lighting_switches': ['switch.adaptive_lighting_test'],
        'min_brightness_pct': 5,
    }

@pytest.fixture
def mock_config_entry(mock_config_entry_data):
    return MockConfigEntry(
        domain='rig_for_red',
        data=mock_config_entry_data,
        title='Rig for Red (23:00 [mon,tue,wed,thu,fri])',
    )

@pytest.fixture
def mock_config_entry_no_al(mock_config_entry_data):
    data = {**mock_config_entry_data, 'adaptive_lighting_switches': []}
    return MockConfigEntry(domain='rig_for_red', data=data, title='Rig for Red (23:00 [...])')

@pytest.fixture
async def mock_light_states(hass: HomeAssistant):
    # Mock light entities mit realistischen Attributen
    hass.states.async_set('light.test_light_1', 'on', {
        'brightness': 200, 'rgb_color': (255, 255, 255),
        'color_temp_kelvin': 4000, 'supported_color_modes': ['color_temp', 'rgb']
    })
    hass.states.async_set('light.test_light_2', 'on', {
        'brightness': 180, 'rgb_color': (255, 255, 255),
        'color_temp_kelvin': 4000, 'supported_color_modes': ['color_temp', 'rgb']
    })

@pytest.fixture
async def mock_sun_state(hass: HomeAssistant):
    from homeassistant.util import dt as dt_util
    next_rising = (dt_util.now().replace(hour=6, minute=0, second=0)).isoformat()
    hass.states.async_set('sun.sun', 'above_horizon', {'next_rising': next_rising})

@pytest.fixture
async def setup_integration(hass, mock_config_entry, mock_light_states):
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    return mock_config_entry

pytest.ini oder setup.cfg:
[pytest]
asyncio_mode = auto
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 pytest tests/ läuft ohne ImportError oder Fixture-Fehler
- [x] #2 conftest.py enthält alle 6 Fixtures: mock_config_entry_data, mock_config_entry, mock_config_entry_no_al, mock_light_states, mock_sun_state, setup_integration
- [x] #3 pytest.ini oder setup.cfg oder pyproject.toml enthält asyncio_mode = auto
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
conftest.py mit 6 Fixtures (mock_config_entry_data, mock_config_entry, mock_config_entry_no_al, mock_light_states, mock_sun_state, setup_integration) erstellt. setup.cfg mit asyncio_mode=auto.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
tests/conftest.py implementiert mit allen 6 Fixtures für HA-Komponententests. setup.cfg mit asyncio_mode=auto für pytest-asyncio.
<!-- SECTION:FINAL_SUMMARY:END -->
