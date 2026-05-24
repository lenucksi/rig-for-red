import asyncio
import contextlib
from datetime import UTC, datetime, timedelta

from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from custom_components.rig_for_red.const import (
    CONF_RESTORE_AT_SUNRISE,
    CONF_RESTORE_TIME,
    CONF_SCHEDULE_DAYS,
    DOMAIN,
)

from . import MockConfigEntry


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
    await coordinator._schedule_trigger(now)
    await hass.async_block_till_done()

    assert coordinator.is_active

    await coordinator.async_restore()
    await hass.async_block_till_done()


async def test_schedule_trigger_wrong_day(
    hass: HomeAssistant,
    mock_config_entry_data: dict,
    mock_light_states,
) -> None:
    data = {**mock_config_entry_data, CONF_SCHEDULE_DAYS: ["mon", "tue", "wed", "thu", "fri"]}
    entry = MockConfigEntry(domain=DOMAIN, data=data, entry_id="test_wrong_day")
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][entry.entry_id]

    now = datetime(2024, 1, 6, 23, 0, 0, tzinfo=dt_util.UTC)
    await coordinator._schedule_trigger(now)
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

    await coordinator.async_restore()
    await hass.async_block_till_done()


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

    await coordinator.async_restore()
    await hass.async_block_till_done()


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

    await coordinator.async_restore()
    await hass.async_block_till_done()


async def test_restore_time_trigger(
    hass: HomeAssistant,
    mock_config_entry_data: dict,
    mock_light_states,
) -> None:
    data = dict(mock_config_entry_data)
    data[CONF_RESTORE_AT_SUNRISE] = False
    data[CONF_RESTORE_TIME] = "07:00"
    entry = MockConfigEntry(domain=DOMAIN, data=data, entry_id="test_restore_time")
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][entry.entry_id]

    now = datetime(2024, 1, 3, 7, 0, 0, tzinfo=dt_util.UTC)
    await coordinator._restore_trigger(now)
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


async def test_activate_already_active(
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

    await coordinator.async_activate()
    await hass.async_block_till_done()
    assert coordinator.is_active

    await coordinator.async_restore()
    await hass.async_block_till_done()


async def test_restore_when_not_active(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_light_states,
) -> None:
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][mock_config_entry.entry_id]

    assert not coordinator.is_active
    await coordinator.async_restore()
    await hass.async_block_till_done()

    assert not coordinator.is_active


async def test_parse_time_invalid(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_light_states,
) -> None:
    from custom_components.rig_for_red.coordinator import _parse_time

    result = _parse_time("invalid")
    assert result is None


async def test_activate_max_brightness(
    hass: HomeAssistant,
    mock_config_entry_data: dict,
    mock_light_states,
) -> None:
    hass.states.async_set("light.bright_light", STATE_ON, {"brightness": 255})
    data = dict(mock_config_entry_data)
    data["lights"] = ["light.bright_light"]
    entry = MockConfigEntry(domain=DOMAIN, data=data, entry_id="test_max_brightness")
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][entry.entry_id]

    await coordinator.async_activate()
    await hass.async_block_till_done()
    assert coordinator.is_active

    await coordinator.async_restore()
    await hass.async_block_till_done()


async def test_sunrise_without_next_rising(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_light_states,
    mock_sun_state,
) -> None:
    hass.states.async_set("sun.sun", "above_horizon", {})
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][mock_config_entry.entry_id]

    sunrise = await coordinator._get_next_sunrise()
    assert sunrise is not None


async def test_schedule_trigger_already_active(
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

    now = datetime(2024, 1, 3, 23, 0, 0, tzinfo=dt_util.UTC)
    await coordinator._schedule_trigger(now)
    await hass.async_block_till_done()
    assert coordinator.is_active

    await coordinator.async_restore()
    await hass.async_block_till_done()


async def test_dim_is_active_abort(
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
    assert coordinator._dim_task is not None

    coordinator._is_active = False
    coordinator._dim_task.cancel()
    with contextlib.suppress(asyncio.CancelledError, Exception):
        await coordinator._dim_task
    await hass.async_block_till_done()

    assert not coordinator.is_active


async def test_activate_off_lights_stay_off(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_light_states,
) -> None:
    hass.states.async_set("light.living_room", STATE_OFF)
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][mock_config_entry.entry_id]

    await coordinator.async_activate()
    await hass.async_block_till_done()

    assert coordinator.is_active
    assert "light.bedroom" in coordinator._lights_to_restore
    assert "light.living_room" not in coordinator._lights_to_restore
    assert "light.living_room" in coordinator._lights_waiting_for_red

    await coordinator.async_restore()
    await hass.async_block_till_done()

    assert not coordinator.is_active
    assert coordinator._lights_to_restore == []
    assert coordinator._lights_waiting_for_red == []


async def test_activate_no_on_lights_skips(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_light_states,
) -> None:
    hass.states.async_set("light.bedroom", STATE_OFF)
    hass.states.async_set("light.living_room", STATE_OFF)
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][mock_config_entry.entry_id]

    await coordinator.async_activate()
    await hass.async_block_till_done()

    assert not coordinator.is_active
    assert coordinator._lights_to_restore == []


async def test_off_light_turned_on_during_activation_goes_red(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_light_states,
) -> None:
    hass.states.async_set("light.living_room", STATE_OFF)
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][mock_config_entry.entry_id]

    await coordinator.async_activate()
    await hass.async_block_till_done()

    assert coordinator.is_active
    assert "light.living_room" in coordinator._lights_waiting_for_red

    hass.states.async_set("light.living_room", STATE_ON, {"brightness": 200})
    await hass.async_block_till_done()

    assert "light.living_room" not in coordinator._lights_waiting_for_red
    assert "light.living_room" in coordinator._lights_to_restore

    await coordinator.async_restore()
    await hass.async_block_till_done()

    assert not coordinator.is_active


async def test_user_turned_off_red_light_stays_off_on_restore(
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

    assert "light.bedroom" in coordinator._lights_to_restore
    assert "light.living_room" in coordinator._lights_to_restore

    hass.states.async_set("light.bedroom", STATE_OFF)
    await hass.async_block_till_done()

    assert "light.bedroom" not in coordinator._lights_to_restore
    assert "light.living_room" in coordinator._lights_to_restore

    await coordinator.async_restore()
    await hass.async_block_till_done()

    assert not coordinator.is_active


async def test_off_light_no_red_when_sunrise_imminent(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_light_states,
) -> None:
    sunrise_time = datetime.now(UTC) + timedelta(minutes=5)
    hass.states.async_set(
        "sun.sun",
        "above_horizon",
        {"next_rising": sunrise_time.isoformat()},
    )
    hass.states.async_set("light.living_room", STATE_OFF)

    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][mock_config_entry.entry_id]

    await coordinator.async_activate()
    await hass.async_block_till_done()

    assert coordinator.is_active
    assert "light.living_room" in coordinator._lights_waiting_for_red
    assert "light.living_room" not in coordinator._lights_to_restore

    hass.states.async_set("light.living_room", STATE_ON, {"brightness": 200})
    await hass.async_block_till_done()

    assert "light.living_room" not in coordinator._lights_waiting_for_red
    assert "light.living_room" in coordinator._lights_to_restore

    await coordinator.async_restore()
    await hass.async_block_till_done()
    assert not coordinator.is_active


async def test_off_light_no_red_when_restore_time_imminent(
    hass: HomeAssistant,
    mock_config_entry_data,
    mock_light_states,
) -> None:
    now = datetime.now(UTC)
    near_future = (now + timedelta(minutes=5)).time()
    data = dict(mock_config_entry_data)
    data[CONF_RESTORE_AT_SUNRISE] = False
    data[CONF_RESTORE_TIME] = near_future.strftime("%H:%M")

    entry = MockConfigEntry(domain=DOMAIN, data=data, entry_id="test_imminent_time")
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][entry.entry_id]

    hass.states.async_set("light.living_room", STATE_OFF)
    await hass.async_block_till_done()

    await coordinator.async_activate()
    await hass.async_block_till_done()

    assert coordinator.is_active
    assert "light.living_room" in coordinator._lights_waiting_for_red

    hass.states.async_set("light.living_room", STATE_ON, {"brightness": 200})
    await hass.async_block_till_done()

    assert "light.living_room" not in coordinator._lights_waiting_for_red
    assert "light.living_room" in coordinator._lights_to_restore

    await coordinator.async_restore()
    await hass.async_block_till_done()
    assert not coordinator.is_active
