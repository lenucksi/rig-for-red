# Reference Links — Rig for Red

> Alle Referenz-Quellen für die Implementierung der `rig_for_red` Integration.

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

> **Wichtig:** `adaptive_lighting` ist eine optionale Abhängigkeit. Die Integration funktioniert ohne AL.
> Wenn AL-Switches konfiguriert sind, werden alle AL-Calls in `try/except` gewrapped.

## HACS

15. **HACS Integration Publishing** — https://hacs.xyz/docs/publish/integration
16. **hacs.json Format** — https://hacs.xyz/docs/publish/integration#hacsjson

## CI/CD

17. **hassfest GitHub Action** — https://github.com/home-assistant/actions
18. **HACS Validation Action** — https://github.com/hacs/action

## Testing

19. **pytest-homeassistant-custom-component** — https://github.com/MatthewFlamm/pytest-homeassistant-custom-component
20. **freezegun** (time mocking) — https://github.com/spulec/freezegun
21. **integration_blueprint** (Referenz-Repo) — https://github.com/ludeeus/integration_blueprint

## Technische Hinweise

| Thema | Hinweis |
|-------|---------|
| `color_temp` | Deprecated seit HA 2026.3 → ausschließlich `color_temp_kelvin` verwenden |
| `async_track_time_change` | Immer `second=0` übergeben, sonst feuert es jede Sekunde |
| AL `set_manual_control` | Service-Domain ist `adaptive_lighting`, nicht `switch` |
| RGBCCT Lichter | Unterstützen sowohl `rgb_color` als auch `color_temp_kelvin` Modi |
| `asyncio.CancelledError` | In `_dim_lights` fangen, sonst wird Exception propagiert |
