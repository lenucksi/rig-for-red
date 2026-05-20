---
id: decision-2
title: 'ADR-002: Gestufte Dimmung statt einzelner langer Transition'
date: '2026-05-20 20:16'
status: accepted
---
## Context

HA's `light.turn_on` hat einen `transition` Parameter für sanfte Übergänge. Ein einziger Aufruf mit `transition=dim_duration_minutes*60` (z.B. 3600 Sekunden) wäre technisch möglich, ist aber nicht unterbrechbar: HA bietet keine API um eine laufende Transition abzubrechen.

## Decision

10 diskrete `light.turn_on` Aufrufe (Konstante `DIM_STEPS=10`) mit jeweils `transition=interval` für Glättung zwischen den Schritten. `asyncio.sleep(interval)` zwischen Steps mit Abbruch-Flag-Check (`if not self.is_active: return`) und `asyncio.CancelledError` Handling.

```python
interval = (dim_duration_minutes * 60) / DIM_STEPS
for i in range(1, DIM_STEPS + 1):
    if not self.is_active:
        return
    brightness = int(start - (start - target) * i / DIM_STEPS)
    await hass.services.async_call("light", "turn_on", {
        "rgb_color": RED_RGB, "brightness": brightness, "transition": interval
    })
    await asyncio.sleep(interval)
```

## Consequences

- **Pro**: Jederzeit abbrechbar via `is_active=False` Flag oder `_dim_task.cancel()`
- **Pro**: Zukünftige Features (Pause, Resume, dynamische Step-Anzahl) möglich
- **Con**: 10 Service-Calls statt 1 — bei lokaler HA-Instanz vernachlässigbar
- `asyncio.CancelledError` muss in `_dim_lights` gefangen werden, sonst Exception-Propagation
