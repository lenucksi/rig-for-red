import pytest
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResultType

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
    DOMAIN,
)


@pytest.fixture
def config_entry_data():
    return {
        CONF_LIGHTS: ["light.bedroom", "light.living_room"],
        CONF_SCHEDULE_DAYS: ["mon", "tue", "wed", "thu", "fri"],
        CONF_SCHEDULE_TIME: "23:00",
        CONF_DIM_DURATION_MINUTES: DEFAULT_DIM_DURATION_MINUTES,
        CONF_RESTORE_AT_SUNRISE: True,
        CONF_RESTORE_TIME: None,
        CONF_ADAPTIVE_LIGHTING_SWITCHES: ["switch.adaptive_lighting"],
        CONF_MIN_BRIGHTNESS_PCT: DEFAULT_MIN_BRIGHTNESS_PCT,
    }


async def test_form_displayed(hass):
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"
    schema = result["data_schema"]
    assert schema is not None
    field_keys = set(schema.schema.keys()) if isinstance(schema.schema, dict) else {k.key for k in schema.schema}
    assert CONF_LIGHTS in field_keys
    assert CONF_SCHEDULE_DAYS in field_keys
    assert CONF_SCHEDULE_TIME in field_keys
    assert CONF_DIM_DURATION_MINUTES in field_keys
    assert CONF_RESTORE_AT_SUNRISE in field_keys
    assert CONF_RESTORE_TIME in field_keys
    assert CONF_ADAPTIVE_LIGHTING_SWITCHES in field_keys
    assert CONF_MIN_BRIGHTNESS_PCT in field_keys


async def test_valid_config_creates_entry(hass, config_entry_data, mock_light_states):
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
        data=config_entry_data,
    )
    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "Rig for Red (23:00 [mon,tue,wed,thu,fri])"
    assert result["data"][CONF_LIGHTS] == config_entry_data[CONF_LIGHTS]


async def test_valid_config_no_al(hass, mock_light_states):
    data = {
        CONF_LIGHTS: ["light.bedroom"],
        CONF_SCHEDULE_DAYS: ["mon", "tue"],
        CONF_SCHEDULE_TIME: "22:00",
        CONF_DIM_DURATION_MINUTES: DEFAULT_DIM_DURATION_MINUTES,
        CONF_RESTORE_AT_SUNRISE: False,
        CONF_RESTORE_TIME: "07:00",
        CONF_ADAPTIVE_LIGHTING_SWITCHES: [],
        CONF_MIN_BRIGHTNESS_PCT: DEFAULT_MIN_BRIGHTNESS_PCT,
    }
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
        data=data,
    )
    assert result["type"] == FlowResultType.CREATE_ENTRY


async def test_missing_lights_error(hass):
    data = {
        CONF_LIGHTS: [],
        CONF_SCHEDULE_DAYS: ["mon"],
        CONF_SCHEDULE_TIME: "23:00",
        CONF_DIM_DURATION_MINUTES: DEFAULT_DIM_DURATION_MINUTES,
        CONF_RESTORE_AT_SUNRISE: True,
        CONF_RESTORE_TIME: None,
        CONF_ADAPTIVE_LIGHTING_SWITCHES: [],
        CONF_MIN_BRIGHTNESS_PCT: DEFAULT_MIN_BRIGHTNESS_PCT,
    }
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
        data=data,
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"].get(CONF_LIGHTS) == "lights_required"


async def test_entity_not_found(hass):
    data = {
        CONF_LIGHTS: ["light.nonexistent"],
        CONF_SCHEDULE_DAYS: ["mon"],
        CONF_SCHEDULE_TIME: "23:00",
        CONF_DIM_DURATION_MINUTES: DEFAULT_DIM_DURATION_MINUTES,
        CONF_RESTORE_AT_SUNRISE: True,
        CONF_RESTORE_TIME: None,
        CONF_ADAPTIVE_LIGHTING_SWITCHES: [],
        CONF_MIN_BRIGHTNESS_PCT: DEFAULT_MIN_BRIGHTNESS_PCT,
    }
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
        data=data,
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"].get(CONF_LIGHTS) == "entity_not_found"


async def test_restore_time_required(hass, mock_light_states):
    data = {
        CONF_LIGHTS: ["light.bedroom"],
        CONF_SCHEDULE_DAYS: ["mon"],
        CONF_SCHEDULE_TIME: "23:00",
        CONF_DIM_DURATION_MINUTES: DEFAULT_DIM_DURATION_MINUTES,
        CONF_RESTORE_AT_SUNRISE: False,
        CONF_RESTORE_TIME: None,
        CONF_ADAPTIVE_LIGHTING_SWITCHES: [],
        CONF_MIN_BRIGHTNESS_PCT: DEFAULT_MIN_BRIGHTNESS_PCT,
    }
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
        data=data,
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"].get(CONF_RESTORE_TIME) == "restore_time_required"


async def test_reconfigure_form_displayed(hass, mock_config_entry):
    mock_config_entry.add_to_hass(hass)
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_RECONFIGURE, "entry_id": mock_config_entry.entry_id},
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "reconfigure"
    schema = result["data_schema"]
    assert schema is not None
    field_keys = set(schema.schema.keys()) if isinstance(schema.schema, dict) else {k.key for k in schema.schema}
    assert CONF_LIGHTS in field_keys
    assert CONF_SCHEDULE_DAYS in field_keys
    assert CONF_SCHEDULE_TIME in field_keys


async def test_reconfigure_updates_entry(hass, mock_config_entry, mock_light_states):
    mock_config_entry.add_to_hass(hass)
    init = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_RECONFIGURE, "entry_id": mock_config_entry.entry_id},
    )
    assert init["type"] == FlowResultType.FORM

    new_data = {
        CONF_LIGHTS: ["light.bedroom"],
        CONF_SCHEDULE_DAYS: ["mon", "tue"],
        CONF_SCHEDULE_TIME: "22:00",
        CONF_DIM_DURATION_MINUTES: DEFAULT_DIM_DURATION_MINUTES,
        CONF_RESTORE_AT_SUNRISE: True,
        CONF_ADAPTIVE_LIGHTING_SWITCHES: [],
        CONF_MIN_BRIGHTNESS_PCT: DEFAULT_MIN_BRIGHTNESS_PCT,
    }
    result = await hass.config_entries.flow.async_configure(
        init["flow_id"],
        user_input=new_data,
    )
    assert result["type"] == FlowResultType.ABORT
    entry = hass.config_entries.async_get_entry(mock_config_entry.entry_id)
    assert entry.data[CONF_LIGHTS] == new_data[CONF_LIGHTS]
    assert entry.data[CONF_SCHEDULE_DAYS] == new_data[CONF_SCHEDULE_DAYS]
    assert entry.data[CONF_SCHEDULE_TIME] == new_data[CONF_SCHEDULE_TIME]


async def test_reconfigure_missing_lights_error(hass, mock_config_entry, mock_light_states):
    mock_config_entry.add_to_hass(hass)
    init = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_RECONFIGURE, "entry_id": mock_config_entry.entry_id},
    )
    new_data = {
        CONF_LIGHTS: [],
        CONF_SCHEDULE_DAYS: mock_config_entry.data.get(CONF_SCHEDULE_DAYS),
        CONF_SCHEDULE_TIME: mock_config_entry.data.get(CONF_SCHEDULE_TIME),
        CONF_DIM_DURATION_MINUTES: mock_config_entry.data.get(CONF_DIM_DURATION_MINUTES),
        CONF_RESTORE_AT_SUNRISE: mock_config_entry.data.get(CONF_RESTORE_AT_SUNRISE),
        CONF_ADAPTIVE_LIGHTING_SWITCHES: mock_config_entry.data.get(CONF_ADAPTIVE_LIGHTING_SWITCHES, []),
        CONF_MIN_BRIGHTNESS_PCT: mock_config_entry.data.get(CONF_MIN_BRIGHTNESS_PCT),
    }
    result = await hass.config_entries.flow.async_configure(
        init["flow_id"],
        user_input=new_data,
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"].get(CONF_LIGHTS) == "lights_required"


async def test_reconfigure_entity_not_found(hass, mock_config_entry):
    mock_config_entry.add_to_hass(hass)
    init = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_RECONFIGURE, "entry_id": mock_config_entry.entry_id},
    )
    new_data = {
        CONF_LIGHTS: ["light.nonexistent"],
        CONF_SCHEDULE_DAYS: mock_config_entry.data.get(CONF_SCHEDULE_DAYS),
        CONF_SCHEDULE_TIME: mock_config_entry.data.get(CONF_SCHEDULE_TIME),
        CONF_DIM_DURATION_MINUTES: mock_config_entry.data.get(CONF_DIM_DURATION_MINUTES),
        CONF_RESTORE_AT_SUNRISE: mock_config_entry.data.get(CONF_RESTORE_AT_SUNRISE),
        CONF_ADAPTIVE_LIGHTING_SWITCHES: mock_config_entry.data.get(CONF_ADAPTIVE_LIGHTING_SWITCHES, []),
        CONF_MIN_BRIGHTNESS_PCT: mock_config_entry.data.get(CONF_MIN_BRIGHTNESS_PCT),
    }
    result = await hass.config_entries.flow.async_configure(
        init["flow_id"],
        user_input=new_data,
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"].get(CONF_LIGHTS) == "entity_not_found"


async def test_reconfigure_restore_time_required(hass, mock_config_entry, mock_light_states):
    mock_config_entry.add_to_hass(hass)
    init = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_RECONFIGURE, "entry_id": mock_config_entry.entry_id},
    )
    new_data = {
        CONF_LIGHTS: mock_config_entry.data.get(CONF_LIGHTS),
        CONF_SCHEDULE_DAYS: mock_config_entry.data.get(CONF_SCHEDULE_DAYS),
        CONF_SCHEDULE_TIME: mock_config_entry.data.get(CONF_SCHEDULE_TIME),
        CONF_DIM_DURATION_MINUTES: mock_config_entry.data.get(CONF_DIM_DURATION_MINUTES),
        CONF_RESTORE_AT_SUNRISE: False,
        CONF_ADAPTIVE_LIGHTING_SWITCHES: mock_config_entry.data.get(CONF_ADAPTIVE_LIGHTING_SWITCHES, []),
        CONF_MIN_BRIGHTNESS_PCT: mock_config_entry.data.get(CONF_MIN_BRIGHTNESS_PCT),
    }
    result = await hass.config_entries.flow.async_configure(
        init["flow_id"],
        user_input=new_data,
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"].get(CONF_RESTORE_TIME) == "restore_time_required"
