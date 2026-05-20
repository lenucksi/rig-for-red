---
id: doc-1
title: Reference Links
type: guide
created_date: '2026-05-20 20:10'
---

# Reference Links

Alle Referenz-Quellen für die Implementierung der rig_for_red Integration.

## Home Assistant Development

- **Custom Component Guide**: https://developers.home-assistant.io/docs/creating_component_index
- **Config Flow / Config Entries**: https://developers.home-assistant.io/docs/config_entries_config_flow_handler
- **DataUpdateCoordinator**: https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
- **Event Helpers** (`async_track_time_change`, `async_track_point_in_time`): https://developers.home-assistant.io/docs/integration_listen_events
- **Light Entity** (`color_temp_kelvin`, `rgb_color`, `brightness`): https://developers.home-assistant.io/docs/core/entity/light
- **HA Selectors Reference**: https://developers.home-assistant.io/docs/data_entry_flow_index
- **Integration Manifest** (`manifest.json`): https://developers.home-assistant.io/docs/creating_integration_manifest
- **Service Actions** (`hass.services.async_call`): https://developers.home-assistant.io/docs/dev_101_services
- **Testing HA Integrations**: https://developers.home-assistant.io/docs/development_testing

## Adaptive Lighting (optional)

- **adaptive_lighting GitHub**: https://github.com/basnijholt/adaptive-lighting
- **adaptive_lighting Services API**: https://adaptive-lighting.nijho.lt/services/
- **set_manual_control service**: https://adaptive-lighting.nijho.lt/services/#set_manual_control
- **Manual Control / Override**: https://adaptive-lighting.nijho.lt/advanced/manual-control/

> **Wichtig**: `adaptive_lighting` ist eine optionale Abhängigkeit. Die Integration funktioniert ohne AL. Wenn AL-Switches konfiguriert sind, werden alle AL-Calls in `try/except` gewrapped.

## Sun Integration

- **HA Sun Integration docs**: https://www.home-assistant.io/integrations/sun/
- `sun.sun` entity hat Attribut `next_rising` (ISO 8601 UTC string)
- `sensor.sun_next_rising` als Alternative verfügbar

## HACS

- **HACS Integration Publishing**: https://hacs.xyz/docs/publish/integration
- **hacs.json Format**: https://hacs.xyz/docs/publish/integration#hacsjson

## CI/CD

- **hassfest GitHub Action**: https://github.com/home-assistant/actions
- **HACS Validation Action**: https://github.com/hacs/action

## Testing

- **pytest-homeassistant-custom-component**: https://github.com/MatthewFlamm/pytest-homeassistant-custom-component
- **freezegun** (time mocking): https://github.com/spulec/freezegun
- **integration_blueprint** (Referenz-Repo): https://github.com/ludeeus/integration_blueprint

## Kritische technische Hinweise

| Thema | Hinweis |
|-------|---------|
| `color_temp` | Deprecated seit HA 2026.3 → ausschließlich `color_temp_kelvin` verwenden |
| `async_track_time_change` | Immer `second=0` übergeben, sonst feuert es jede Sekunde |
| AL `set_manual_control` | Service-Domain ist `adaptive_lighting`, nicht `switch` |
| RGBCCT Lichter | Unterstützen sowohl `rgb_color` als auch `color_temp_kelvin` Modi |
| `asyncio.CancelledError` | In `_dim_lights` fangen, sonst wird Exception propagiert |
