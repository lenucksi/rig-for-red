# Rig for Red — Submarine Night Mode für Home Assistant

> Automatische Rotlicht-Dimmung für den Nachtmodus — inspiriert vom Beleuchtungssystem
> eines U-Boots. Rig for Red dimmt konfigurierte Leuchten zur Schlafenszeit auf rotes
> Licht herunter und stellt sie bei Sonnenaufgang (oder zu einer festen Zeit) wieder
> auf Weißlicht zurück.

## Features

- **Automatischer Schedule** — tägliche Aktivierung zu konfigurierbarer Zeit an wählbaren Wochentagen
- **Gestufte Dimmung** — 10-stufiger sanfter Übergang von Weiß- zu Rotlicht (jederzeit abbrechbar)
- **Sunrise-Restore** — automatische Rückkehr zu Weißlicht bei Sonnenaufgang oder zu fester Zeit
- **Adaptive Lighting Integration** — optionale Pause/Resume von `adaptive_lighting`-Switches
- **Konfiguration via UI** — einfacher Setup über Home Assistant Config Flow

## Voraussetzungen

- **Home Assistant** ≥ 2025.3.0
- **HACS** (empfohlen) oder manuelle Installation
- **Adaptive Lighting** (optional) — nur wenn `adaptive_lighting`-Switches verwendet werden

> **Hinweis:** `adaptive_lighting` ist vollständig optional. Die Integration funktioniert
> ohne installiertes Adaptive Lighting. Alle AL-bezogenen Aufrufe sind in `try/except`
> gewrapped.

## Installation

### Via HACS (empfohlen)

1. Öffne HACS in Home Assistant
2. Gehe zu "Integrationen"
3. Klicke auf das Menü (drei Punkte) → "Custom repositories"
4. Füge `https://github.com/<dein-repo>/rig-for-red` hinzu (Kategorie: Integration)
5. Suche nach "Rig for Red" und installiere
6. Starte Home Assistant neu

### Manuelle Installation

1. Kopiere das Verzeichnis `custom_components/rig_for_red/` in dein HA `custom_components/` Verzeichnis
2. Starte Home Assistant neu

## Konfiguration

Nach der Installation über Home Assistant → Einstellungen → Geräte & Dienste → "Integration hinzufügen"
→ "Rig for Red" suchen.

### Konfigurationsfelder

| Feld | Typ | Required | Default | Beschreibung |
|------|-----|----------|---------|--------------|
| `lights` | `entity_id[]` | Ja | — | Licht-Entities, die gedimmt werden sollen |
| `schedule_days` | `string[]` | Ja | — | Wochentage für Aktivierung (`mon, tue, wed, thu, fri, sat, sun`) |
| `schedule_time` | `time` | Ja | — | Uhrzeit der Aktivierung |
| `dim_duration_minutes` | `number` | Ja | `60` | Dauer des Dimm-Vorgangs in Minuten (1–240) |
| `restore_at_sunrise` | `boolean` | Ja | `true` | Bei Sonnenaufgang zurück zum Weißlicht |
| `restore_time` | `time` | Nein | — | Feste Uhrzeit für Restore (nur wenn `restore_at_sunrise: false`) |
| `adaptive_lighting_switches` | `entity_id[]` | Nein | — | Adaptive Lighting Switch-Entities zum Pausieren |
| `min_brightness_pct` | `number` | Ja | `5` | Minimale Helligkeit in Prozent (1–10 %) |

> **Hinweis zu `restore_time`:** Wenn `restore_at_sunrise` auf `false` gesetzt ist, muss
> `restore_time` angegeben werden.

## Beispiel: Zigbee-Button für manuelle Steuerung

Über HA Automatisierungen kann die Integration mit einem Zigbee-Button verknüpft werden:

```yaml
alias: "Rig for Red — Toggle Nachtmodus"
trigger:
  - platform: state
    entity_id: sensor.dein_knopf_action
    to: "single"
action:
  - service: switch.toggle
    target:
      entity_id: switch.rig_for_red_night_mode
```

## Entwicklung

### Tests ausführen

```bash
pytest tests/ --cov=custom_components/rig_for_red --cov-report=term-missing
```

### CI

- `hassfest` — manifest.json Validierung
- `HACS validation` — HACS-Formatprüfung
- `pytest` — Test Suite mit Coverage ≥80%

### Architektur

Siehe `docs/ADR-001-architecture.md` für die vollständige Dokumentation der
Architekturentscheidungen.

## Lizenz

MIT
