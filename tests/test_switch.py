from homeassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from homeassistant.core import HomeAssistant

from custom_components.rig_for_red.const import DOMAIN


async def test_switch_exists(
    hass: HomeAssistant,
    setup_integration,
) -> None:
    entity_id = "switch.rig_for_red"
    state = hass.states.get(entity_id)
    assert state is not None


async def test_switch_initially_off(
    hass: HomeAssistant,
    setup_integration,
) -> None:
    entity_id = "switch.rig_for_red"
    state = hass.states.get(entity_id)
    assert state.state == "off"


async def test_turn_on(
    hass: HomeAssistant,
    setup_integration,
    mock_light_states,
) -> None:
    coordinator = hass.data[DOMAIN][setup_integration.entry_id]
    entity_id = "switch.rig_for_red"

    await hass.services.async_call(
        SWITCH_DOMAIN,
        "turn_on",
        {"entity_id": entity_id},
        blocking=True,
    )
    await hass.async_block_till_done()

    assert coordinator.is_active


async def test_turn_off(
    hass: HomeAssistant,
    setup_integration,
    mock_light_states,
) -> None:
    coordinator = hass.data[DOMAIN][setup_integration.entry_id]
    entity_id = "switch.rig_for_red"

    await coordinator.async_activate()
    await hass.async_block_till_done()
    assert coordinator.is_active

    await hass.services.async_call(
        SWITCH_DOMAIN,
        "turn_off",
        {"entity_id": entity_id},
        blocking=True,
    )
    await hass.async_block_till_done()

    assert not coordinator.is_active


async def test_icon_submarine_when_on(
    hass: HomeAssistant,
    setup_integration,
    mock_light_states,
) -> None:
    coordinator = hass.data[DOMAIN][setup_integration.entry_id]
    entity_id = "switch.rig_for_red"

    await coordinator.async_activate()
    await hass.async_block_till_done()

    state = hass.states.get(entity_id)
    assert state.attributes.get("icon") == "mdi:submarine"
