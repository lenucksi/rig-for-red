from datetime import datetime, timedelta

import pytest
from homeassistant.config_entries import MockConfigEntry
from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_fire_time_changed
from homeassistant.util import dt as dt_util

from custom_components.rig_for_red.const import (
    CONF_ADAPTIVE_LIGHTING_SWITCHES,
    CONF_RESTORE_AT_SUNRISE,
    CONF_RESTORE_TIME,
    CONF_SCHEDULE_DAYS,
    DOMAIN,
)


async def test_schedule_trigger_correct_day(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_light_states,
    mock_sun_state,
) -> None:
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][mock_config_entry.entry_id]

    now = datetime(2024, 1, 3, 23, 0, 0, tzinfo=dt_util.UTC)
    async_fire_time_changed(hass, now)
    await hass.async_block_till_done()

    assert coordinator.is_active


async def test_schedule_trigger_wrong_day(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_light_states,
) -> None:
    mock_config_entry.data = {
        **mock_config_entry.data,
        CONF_SCHEDULE_DAYS: ["mon", "tue", "wed", "thu", "fri"],
    }
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][mock_config_entry.entry_id]

    now = datetime(2024, 1, 6, 23, 0, 0, tzinfo=dt_util.UTC)
    async_fire_time_changed(hass, now)
    await hass.async_block_till_done()

    assert not coordinator.is_active


async def test_activate_sets_red(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_light_states,
) -> None:
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][mock_config_entry.entry_id]

    await coordinator.async_activate()
    await hass.async_block_till_done()

    assert coordinator.is_active


async def test_activate_without_al(
    hass: HomeAssistant,
    mock_config_entry_no_al: MockConfigEntry,
    mock_light_states,
) -> None:
    mock_config_entry_no_al.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry_no_al.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][mock_config_entry_no_al.entry_id]

    await coordinator.async_activate()
    await hass.async_block_till_done()

    assert coordinator.is_active


async def test_dim_brightness_decreases(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_light_states,
) -> None:
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][mock_config_entry.entry_id]

    await coordinator.async_activate()
    await hass.async_block_till_done()

    assert coordinator._dim_task is not None
    assert not coordinator._dim_task.done()

    await coordinator.async_restore()
    await hass.async_block_till_done()

    assert not coordinator.is_active


async def test_dim_aborted(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_light_states,
) -> None:
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][mock_config_entry.entry_id]

    await coordinator.async_activate()
    await hass.async_block_till_done()

    assert coordinator._dim_task is not None

    await coordinator.async_restore()
    await hass.async_block_till_done()

    assert not coordinator.is_active
    assert coordinator._dim_task is None or coordinator._dim_task.done()


async def test_restore_white_light(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_light_states,
) -> None:
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][mock_config_entry.entry_id]

    await coordinator.async_activate()
    await hass.async_block_till_done()
    await coordinator.async_restore()
    await hass.async_block_till_done()

    assert not coordinator.is_active


async def test_restore_enables_al(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_light_states,
) -> None:
    hass.states.async_set("switch.adaptive_lighting", STATE_OFF)

    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][mock_config_entry.entry_id]

    await coordinator.async_activate()
    await hass.async_block_till_done()
    await coordinator.async_restore()
    await hass.async_block_till_done()

    assert not coordinator.is_active


async def test_sunrise_restore(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_light_states,
    mock_sun_state,
) -> None:
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][mock_config_entry.entry_id]

    await coordinator.async_activate()
    await hass.async_block_till_done()

    assert coordinator.is_active
    assert coordinator._unsub_sunrise is not None


async def test_restore_time_trigger(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_light_states,
) -> None:
    data = dict(mock_config_entry.data)
    data[CONF_RESTORE_AT_SUNRISE] = False
    data[CONF_RESTORE_TIME] = "07:00"
    mock_config_entry.data = data
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][mock_config_entry.entry_id]

    now = datetime(2024, 1, 3, 7, 0, 0, tzinfo=dt_util.UTC)
    async_fire_time_changed(hass, now)
    await hass.async_block_till_done()


async def test_sunrise_fallback(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_light_states,
) -> None:
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][mock_config_entry.entry_id]

    sunrise = await coordinator._get_next_sunrise()
    assert sunrise is not None
