---
id: decision-4
title: 'ADR-004: Adaptive Lighting ist vollständig optional'
date: '2026-05-20 20:16'
status: accepted
---
## Context

Der primäre Nutzer verwendet `adaptive_lighting` (HACS-Plugin) zur automatischen Lichttemperatur-Anpassung. Die Integration soll AL beim Aktivieren pausieren und beim Restore reaktivieren. Andere Nutzer könnten AL nicht installiert haben — ein hard dependency würde die Integration für sie unbrauchbar machen.

## Decision

- `adaptive_lighting_switches` Konfigurationsfeld ist optional: leere Liste `[]` ist valide
- `dependencies: []` in `manifest.json` — kein hard dependency
- Alle AL-Service-Calls (`adaptive_lighting.set_manual_control`, `switch.turn_on/off` für AL-Switches) werden in `try/except Exception` gewrapped
- Bei Fehler: `_LOGGER.warning(...)` ausgeben, aber Ausführung fortsetzen
- Restore-Reihenfolge wenn AL konfiguriert: erst `adaptive_lighting.set_manual_control(manual_control=False)`, dann `switch.turn_on` als Fallback

## Consequences

- Integration funktioniert vollständig ohne AL (Weißlicht-Restore via `color_temp_kelvin` weiterhin aktiv)
- Nutzer mit AL: konfigurieren `switch.adaptive_lighting_*` Entity-IDs manuell in der Config
- AL-Integration kann jederzeit ohne Neustart der rig_for_red Integration hinzugefügt/entfernt werden
- Tests brauchen zwei Fixture-Varianten: mit und ohne AL-Switches (`mock_config_entry` vs. `mock_config_entry_no_al`)
