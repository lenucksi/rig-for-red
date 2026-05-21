import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.translation import async_get_translations

from custom_components.rig_for_red.const import DOMAIN

EXPECTED_CONFIG_KEYS = [
    "config.step.user.title",
    "config.step.user.description",
    "config.step.user.data.lights",
    "config.step.user.data.schedule_days",
    "config.step.user.data.schedule_time",
    "config.step.user.data.dim_duration_minutes",
    "config.step.user.data.restore_at_sunrise",
    "config.step.user.data.restore_time",
    "config.step.user.data.adaptive_lighting_switches",
    "config.step.user.data.min_brightness_pct",
    "config.step.user.data_description.lights",
    "config.step.user.data_description.schedule_days",
    "config.step.user.data_description.schedule_time",
    "config.step.user.data_description.dim_duration_minutes",
    "config.step.user.data_description.restore_at_sunrise",
    "config.step.user.data_description.restore_time",
    "config.step.user.data_description.adaptive_lighting_switches",
    "config.step.user.data_description.min_brightness_pct",
    "config.error.lights_required",
    "config.error.restore_time_required",
    "config.error.entity_not_found",
]

EXPECTED_SELECTOR_KEYS = [
    "selector.weekdays.options.mon",
    "selector.weekdays.options.tue",
    "selector.weekdays.options.wed",
    "selector.weekdays.options.thu",
    "selector.weekdays.options.fri",
    "selector.weekdays.options.sat",
    "selector.weekdays.options.sun",
]

EXPECTED_ENTITY_KEYS = [
    "entity.switch.rig_for_red.name",
]

NON_EN_LANGUAGES = ["de", "fr", "es", "it", "pt", "nl", "da", "sv", "nb", "fi", "pl", "zh-TW", "hi", "ta"]
CONFIG_LANGUAGES = [*NON_EN_LANGUAGES, "en"]


@pytest.mark.parametrize("language", CONFIG_LANGUAGES)
async def test_config_translations_exist(hass: HomeAssistant, language: str) -> None:
    translations = await async_get_translations(
        hass,
        language,
        "config",
        integrations=[DOMAIN],
    )
    prefix = f"component.{DOMAIN}."
    our_keys = {k.removeprefix(prefix): v for k, v in translations.items() if k.startswith(prefix)}

    for key in EXPECTED_CONFIG_KEYS:
        assert key in our_keys, f"Missing config key '{key}' in {language}"
        assert our_keys[key], f"Empty value for config key '{key}' in {language}"


@pytest.mark.parametrize("language", NON_EN_LANGUAGES)
async def test_selector_translations_exist(hass: HomeAssistant, language: str) -> None:
    translations = await async_get_translations(
        hass,
        language,
        "selector",
        integrations=[DOMAIN],
    )
    prefix = f"component.{DOMAIN}."
    our_keys = {k.removeprefix(prefix): v for k, v in translations.items() if k.startswith(prefix)}

    for key in EXPECTED_SELECTOR_KEYS:
        assert key in our_keys, f"Missing selector key '{key}' in {language}"
        assert our_keys[key], f"Empty value for selector key '{key}' in {language}"


@pytest.mark.parametrize("language", NON_EN_LANGUAGES)
async def test_entity_translations_exist(hass: HomeAssistant, language: str) -> None:
    translations = await async_get_translations(
        hass,
        language,
        "entity",
        integrations=[DOMAIN],
    )
    prefix = f"component.{DOMAIN}."
    our_keys = {k.removeprefix(prefix): v for k, v in translations.items() if k.startswith(prefix)}

    for key in EXPECTED_ENTITY_KEYS:
        assert key in our_keys, f"Missing entity key '{key}' in {language}"
        assert our_keys[key], f"Empty value for entity key '{key}' in {language}"


@pytest.mark.parametrize("language", NON_EN_LANGUAGES)
async def test_translations_fallback_to_english(hass: HomeAssistant, language: str) -> None:
    """Non-English translations should have at least as many config keys as English."""
    en = await async_get_translations(hass, "en", "config", integrations=[DOMAIN])
    lang = await async_get_translations(hass, language, "config", integrations=[DOMAIN])
    prefix = f"component.{DOMAIN}."
    en_keys = {k.removeprefix(prefix) for k in en if k.startswith(prefix)}
    lang_keys = {k.removeprefix(prefix) for k in lang if k.startswith(prefix)}

    missing = en_keys - lang_keys
    assert not missing, (
        f"{language} is missing config keys that English has: {missing}. "
        f"These will fall back to English but should be translated."
    )
