import pytest
from homeassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from homeassistant.core import HomeAssistant

from custom_components.rig_for_red.const import DOMAIN


@pytest.fixture
def switch_entity_id(setup_integration) -> str:
    return f"switch.rig_for_red_{setup_integration.entry_id}"


async def test_switch_exists(
    hass: HomeAssistant,
    switch_entity_id: str,
) -> None:
    state = hass.states.get(switch_entity_id)
    assert state is not None


async def test_switch_initially_off(
    hass: HomeAssistant,
    switch_entity_id: str,
) -> None:
    state = hass.states.get(switch_entity_id)
    assert state.state == "off"


async def test_turn_on(
    hass: HomeAssistant,
    setup_integration,
    mock_light_states,
    switch_entity_id: str,
) -> None:
    coordinator = hass.data[DOMAIN][setup_integration.entry_id]

    await hass.services.async_call(
        SWITCH_DOMAIN,
        "turn_on",
        {"entity_id": switch_entity_id},
        blocking=True,
    )
    await hass.async_block_till_done()

    assert coordinator.is_active


async def test_turn_off(
    hass: HomeAssistant,
    setup_integration,
    mock_light_states,
    switch_entity_id: str,
) -> None:
    coordinator = hass.data[DOMAIN][setup_integration.entry_id]

    await coordinator.async_activate()
    await hass.async_block_till_done()
    assert coordinator.is_active

    await hass.services.async_call(
        SWITCH_DOMAIN,
        "turn_off",
        {"entity_id": switch_entity_id},
        blocking=True,
    )
    await hass.async_block_till_done()

    assert not coordinator.is_active


async def test_icon_lighthouse_when_off(
    hass: HomeAssistant,
    switch_entity_id: str,
) -> None:
    state = hass.states.get(switch_entity_id)
    assert state.attributes.get("icon") == "mdi:lighthouse-on"


async def test_icon_submarine_when_on(
    hass: HomeAssistant,
    setup_integration,
    mock_light_states,
    switch_entity_id: str,
) -> None:
    coordinator = hass.data[DOMAIN][setup_integration.entry_id]

    await coordinator.async_activate()
    await hass.async_block_till_done()

    state = hass.states.get(switch_entity_id)
    assert state.attributes.get("icon") == "mdi:submarine"
