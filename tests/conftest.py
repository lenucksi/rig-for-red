from datetime import datetime, timedelta

import pytest
from homeassistant.config_entries import MockConfigEntry
from homeassistant.const import STATE_ON

from custom_components.rig_for_red.const import (
    CONF_ADAPTIVE_LIGHTING_SWITCHES,
    CONF_DIM_DURATION_MINUTES,
    CONF_LIGHTS,
    CONF_MIN_BRIGHTNESS_PCT,
    CONF_RESTORE_AT_SUNRISE,
    CONF_RESTORE_TIME,
    CONF_SCHEDULE_DAYS,
    CONF_SCHEDULE_TIME,
    DEFAULT_DIM_DURATION_MINUTES,
    DEFAULT_MIN_BRIGHTNESS_PCT,
    DEFAULT_RESTORE_AT_SUNRISE,
    DOMAIN,
)


@pytest.fixture
def mock_config_entry_data():
    return {
        CONF_LIGHTS: ["light.bedroom", "light.living_room"],
        CONF_SCHEDULE_DAYS: ["mon", "tue", "wed", "thu", "fri"],
        CONF_SCHEDULE_TIME: "23:00",
        CONF_DIM_DURATION_MINUTES: DEFAULT_DIM_DURATION_MINUTES,
        CONF_RESTORE_AT_SUNRISE: DEFAULT_RESTORE_AT_SUNRISE,
        CONF_RESTORE_TIME: None,
        CONF_ADAPTIVE_LIGHTING_SWITCHES: ["switch.adaptive_lighting"],
        CONF_MIN_BRIGHTNESS_PCT: DEFAULT_MIN_BRIGHTNESS_PCT,
    }


@pytest.fixture
def mock_config_entry(mock_config_entry_data):
    return MockConfigEntry(
        domain=DOMAIN,
        data=mock_config_entry_data,
        entry_id="test_entry_id",
    )


@pytest.fixture
def mock_config_entry_no_al(mock_config_entry_data):
    data = dict(mock_config_entry_data)
    data[CONF_ADAPTIVE_LIGHTING_SWITCHES] = []
    return MockConfigEntry(
        domain=DOMAIN,
        data=data,
        entry_id="test_entry_no_al",
    )


@pytest.fixture
def mock_light_states(hass):
    hass.states.async_set("light.bedroom", STATE_ON, {
        "brightness": 200,
        "rgb_color": (255, 200, 100),
    })
    hass.states.async_set("light.living_room", STATE_ON, {
        "brightness": 180,
        "rgb_color": (100, 200, 255),
    })


@pytest.fixture
def mock_sun_state(hass):
    next_rising = (datetime.utcnow() + timedelta(hours=2)).isoformat()
    hass.states.async_set("sun.sun", "above_horizon", {
        "next_rising": next_rising,
        "next_setting": datetime.utcnow().isoformat(),
    })


@pytest.fixture
async def setup_integration(hass, mock_config_entry):
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    return mock_config_entry
