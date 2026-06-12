# Rig for Red — Submarine Night Mode for Home Assistant

> ⚠️ **Early Development** — This project is in early development stage.
> APIs, configuration and behavior may change at any time. Feedback and contributions
> are welcome!

> Automated red-light dimming for night mode — inspired by the lighting system
> of a submarine. Rig for Red dims configured lights to red at bedtime and
> restores them to white light at sunrise (or at a fixed time).

## Features

- **Scheduled activation** — daily activation at a configurable time on selected weekdays
- **Staged dimming** — 10-step smooth transition from white to red light (interruptible at any step)
- **Sunrise restore** — automatic return to white light at sunrise or at a fixed time
- **Adaptive Lighting integration** — optional pause/resume of `adaptive_lighting` switches
- **UI configuration** — simple setup via Home Assistant Config Flow

## Requirements

- **Home Assistant** ≥ 2025.3.0
- **HACS** (recommended) or manual installation
- **Adaptive Lighting** (optional) — only if using `adaptive_lighting` switches

> **Note:** `adaptive_lighting` is completely optional. The integration works
> without Adaptive Lighting installed. All AL-related calls are wrapped in `try/except`.

## Installation

### Via HACS (recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the menu (three dots) → "Custom repositories"
4. Add `https://github.com/lenucksi/rig-for-red` (Category: Integration)
5. Search for "Rig for Red" and install
6. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/rig_for_red/` directory into your HA `custom_components/` directory
2. Restart Home Assistant

## Configuration

After installation: Home Assistant → Settings → Devices & Services → "Add integration"
→ Search for "Rig for Red".

### Configuration Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `lights` | `entity_id[]` | Yes | — | Light entities to dim |
| `schedule_days` | `string[]` | Yes | — | Weekdays for activation (`mon, tue, wed, thu, fri, sat, sun`) |
| `schedule_time` | `time` | Yes | — | Activation time |
| `dim_duration_minutes` | `number` | Yes | `60` | Dimming duration in minutes (1–240) |
| `restore_at_sunrise` | `boolean` | Yes | `true` | Restore to white light at sunrise |
| `restore_time` | `time` | No | — | Fixed restore time (only if `restore_at_sunrise: false`) |
| `adaptive_lighting_switches` | `entity_id[]` | No | — | Adaptive Lighting switch entities to pause |
| `min_brightness_pct` | `number` | Yes | `5` | Minimum brightness in percent (1–10 %) |
| `enable_debug_logging` | `boolean` | No | `false` | Enable detailed debug logging for troubleshooting |
| `al_sleep_mode` | `boolean` | No | `false` | Use Adaptive Lighting sleep mode instead of manual red |
| `rgb_preset` | `select` | Yes | `red` | RGB color preset: `red`, `blue`, or `custom` |
| `rgb_custom` | `color_rgb` | No | — | Custom RGB color (only used when `rgb_preset: custom`) |

> **Note on `restore_time`:** If `restore_at_sunrise` is set to `false`, `restore_time` must be provided.

### Adaptive Lighting Configuration Recommendations

When using Rig for Red with Adaptive Lighting (`adaptive_lighting_switches` configured), the following AL settings are recommended to avoid race conditions:

#### `detect_non_ha_changes: true`
Enable detection of non-HA changes (e.g., physical switch presses). This prevents AL from overriding a manual light change.

#### `autoreset_control_seconds: 0`
Disable automatic reset of manual control. When Rig for Red sets `manual_control` on an AL switch, this timer would otherwise clear it after N seconds, causing AL to re-adapt and override the red light. Setting to `0` disables the timer entirely (requires AL to be paused via the Rig switch, or use AL sleep mode via `al_sleep_mode: true` (the AL sleep mode will use your configured preset/custom RGB color).

> **Note on `rgb_custom`:** The `ColorRGBSelector` returns a hex-like RGB value. Stored as a list `[R, G, B]` in the config entry.

> **Note:** `autoreset_control_seconds` corresponds to the `Automatic reset of manual control` slider in the AL config flow UI.

#### AL Logger Debug Configuration
To debug AL interactions, add this to your `configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.adaptive_lighting: debug
    custom_components.rig_for_red: debug
```

## Sensor Entity

Rig for Red exposes a sensor entity (`sensor.rig_for_red_state`) that tracks the current night mode state:

| State | Description |
|-------|-------------|
| `inactive` | Night mode is not active |
| `active_red` | Lights are currently red (or transitioning to red) |
| `dimming` | Lights are in the staged dimming phase |
| `restoring` | Lights are being restored to white |
| `restored` | Lights have been restored to white |

**Attributes:**

- `active_since` — timestamp when night mode was activated
- `lights_active` — list of light entities currently in red
- `lights_tracked_off` — list of light entities that were off at activation (tracked for delayed red)
- `next_restore` — scheduled restore time (sunrise or fixed time)
- `dim_step` — current dimming step (0 = not dimming)
- `al_switches` — list of AL switch entities being managed

## Example: Zigbee Button for Manual Control

Via HA automations, the integration can be linked to a Zigbee button:

```yaml
alias: "Rig for Red — Toggle Night Mode"
trigger:
  - platform: state
    entity_id: sensor.your_button_action
    to: "single"
action:
  - service: switch.toggle
    target:
      entity_id: switch.rig_for_red_night_mode
```

Alternatively, use the custom services directly:

```yaml
# Activate red lights
action:
  service: rig_for_red.trigger_rig

# Restore white lights
action:
  service: rig_for_red.restore_lights
```

## Development

### Running Tests

```bash
pytest tests/ --cov=custom_components/rig_for_red --cov-report=term-missing
```

### CI

- `hassfest` — manifest.json validation
- `HACS validation` — HACS format check
- `pytest` — test suite with ≥80% coverage

### Architecture

See `docs/ADR-001-architecture.md` for the complete architecture decision records.

## License

MIT

## Star History

<a href="https://www.star-history.com/?repos=lenucksi%2Frig-for-red&type=date&logscale&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=lenucksi/rig-for-red&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=lenucksi/rig-for-red&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=lenucksi/rig-for-red&type=date&legend=top-left" />
 </picture>
</a>
