# Changelog

## v0.2.0 (2026-05-21)

### Fixes

- **config_flow crash**: `entity_id in hass.states` → `hass.states.get(entity_id) is None`
  (StateMachine hat kein `__contains__`)
- **i18n**: `translation_key="weekdays"` + `integration="adaptive_lighting"` filter

### Features

- **14 Übersetzungen**: DE, FR, ES, IT, PT, NL, DA, SV, NB, FI, PL, ZH-TW, HI, TA
- **Test-Infrastruktur**: Dockerfile.test, 91 Tests, 95% Coverage
- **CI/CD**: Multi-Release Matrix-Testing, HASSfest, HACS Validation
- **Release Please**: Semantische Versionierung, auto-CHANGELOG, auto-Release
- **Testing & CI Guide**: Vollständige Dokumentation in backlog/docs/guides/testing-and-ci

### Maintenance

- Dockerfile.test mit `ARG HA_VERSION` (baubares HA-Release)
- tests/components/rig_for_red/ (HA-Core-Konvention)
- MockConfigEntry für HA 2026.2.3
- Codebase aufgeräumt (alte root-Tests gelöscht)
