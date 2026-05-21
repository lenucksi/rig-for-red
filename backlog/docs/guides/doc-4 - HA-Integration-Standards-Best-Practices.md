---
id: doc-4
title: HA Integration Standards & Best Practices
type: guide
created_date: '2026-05-21 13:14'
updated_date: '2026-05-21 13:14'
---
## Type Safety & Static Type Checking

Home Assistant uses **mypy** (not pyright) as its static type checker. The project-wide config is in `mypy.ini` with `strict_equality = true`. Core integrations opt into strict checks via the `.strict-typing` file.

### Key Patterns

- **StateMachine**: does `__not__` define `__contains__`. Use `hass.states.get(entity_id) is None` instead of `entity_id in hass.states`.
- **ConfigEntry runtime_data**: store runtime data on `entry.runtime_data` (not `hass.data[DOMAIN][entry_id]`) for typed access.
- **Custom ConfigEntry type**: define `type MyIntegrationConfigEntry = ConfigEntry[CoordinatorType]` for strict typing.

## Config Flow Standards (Bronze mandatory)

Reference: https://developers.home-assistant.io/docs/core/integration/config_flow

- Config flows must use `data_description` in `strings.json` to give field context
- All configuration in `ConfigEntry.data`; optional settings in `ConfigEntry.options`
- EntitySelector supports `integration` filter: `EntitySelectorConfig(domain="switch", integration="adaptive_lighting")`
- SelectSelector supports `translation_key` for localized option labels

## i18n / Translations

Reference: https://developers.home-assistant.io/docs/internationalization/core

- Primary English source: `strings.json` (NOT `translations/en.json`)
- Select option translations: `"selector": { "<translation_key>": { "options": { "value": "Label" } } }`
- Entity name translations: `"entity": { "switch": { "<translation_key>": { "name": "..." } } }`

## Integration Quality Scale

Reference: https://developers.home-assistant.io/docs/core/integration-quality-scale

Four scaled tiers: Bronze, Silver, Gold, Platinum. Each includes all lower tier rules.

### Bronze (baseline)
- UI-based setup, config flow testing, unique IDs, `has_entity_name`, branding

### Silver (stability)
- 95%+ test coverage, action exceptions, config entry unloading

### Gold (UX)
- Device registry, diagnostics, translations, reconfigure flow

### Platinum (highest)
- Strict typing (full type annotations, mypy), async dependencies

## Testing

Reference: https://developers.home-assistant.io/docs/development_testing

- Use `pytest-homeassistant-custom-component` for test fixtures
- Test entry points: `hass.config_entries.flow.async_init(DOMAIN, ...)`
- Coverage via `pytest --cov`
- Config flows need FULL test coverage (all error paths)
