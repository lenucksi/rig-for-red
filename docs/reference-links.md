# Reference Links — Rig for Red

> All reference sources for the `rig_for_red` integration implementation.

## Home Assistant Development

1. **Custom Component Guide** — https://developers.home-assistant.io/docs/creating_component_index
2. **Config Flow / Config Entries** — https://developers.home-assistant.io/docs/config_entries_config_flow_handler
3. **DataUpdateCoordinator** — https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
4. **Event Helpers** (`async_track_time_change`, `async_track_point_in_time`) — https://developers.home-assistant.io/docs/integration_listen_events
5. **Light Entity** (`color_temp_kelvin`, `rgb_color`, `brightness`) — https://developers.home-assistant.io/docs/core/entity/light
6. **HA Selectors Reference** — https://developers.home-assistant.io/docs/data_entry_flow_index
7. **Integration Manifest** (`manifest.json`) — https://developers.home-assistant.io/docs/creating_integration_manifest
8. **Service Actions** (`hass.services.async_call`) — https://developers.home-assistant.io/docs/dev_101_services
9. **Testing HA Integrations** — https://developers.home-assistant.io/docs/development_testing
10. **HA Sun Integration** — https://www.home-assistant.io/integrations/sun/

## Adaptive Lighting (optional)

11. **adaptive_lighting GitHub** — https://github.com/basnijholt/adaptive-lighting
12. **adaptive_lighting Services API** — https://adaptive-lighting.nijho.lt/services/
13. **set_manual_control service** — https://adaptive-lighting.nijho.lt/services/#set_manual_control
14. **Manual Control / Override** — https://adaptive-lighting.nijho.lt/advanced/manual-control/

> **Important:** `adaptive_lighting` is an optional dependency. The integration works without AL.
> If AL switches are configured, all AL calls are wrapped in `try/except`.

## HACS

15. **HACS Integration Publishing** — https://hacs.xyz/docs/publish/integration
16. **hacs.json Format** — https://hacs.xyz/docs/publish/integration#hacsjson

## CI/CD

17. **hassfest GitHub Action** — https://github.com/home-assistant/actions
18. **HACS Validation Action** — https://github.com/hacs/action

## Testing

19. **pytest-homeassistant-custom-component** — https://github.com/MatthewFlamm/pytest-homeassistant-custom-component
20. **freezegun** (time mocking) — https://github.com/spulec/freezegun
21. **integration_blueprint** (reference repo) — https://github.com/ludeeus/integration_blueprint

## Technical Notes

| Topic | Note |
|-------|------|
| `color_temp` | Deprecated since HA 2026.3 → use `color_temp_kelvin` exclusively |
| `async_track_time_change` | Always pass `second=0`, otherwise it fires every second |
| AL `set_manual_control` | Service domain is `adaptive_lighting`, not `switch` |
| RGBCCT lights | Support both `rgb_color` and `color_temp_kelvin` modes |
| `asyncio.CancelledError` | Must be caught in `_dim_lights`, otherwise exception propagates |
