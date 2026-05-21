# Changelog

## [0.2.1](https://github.com/lenucksi/rig-for-red/compare/v0.2.0...v0.2.1) (2026-05-21)


### Bug Fixes

* add checkout step with fetch-depth:0 for release-please ([8b3478b](https://github.com/lenucksi/rig-for-red/commit/8b3478bf057e9b0e97f19f0785f54adc2246c8ed))
* correct release-please action SHA pin ([6deac19](https://github.com/lenucksi/rig-for-red/commit/6deac190a3974c22f0f60a622e372eaa45443cbd))
* integration icon + config flow UI docs for adaptive lighting ([99034ba](https://github.com/lenucksi/rig-for-red/commit/99034ba561c92e167f4ba2605dfc2b95f5fcb3a4))
* sync release-please-manifest to v0.2.0, use correct commit SHA for release-please-action ([9526809](https://github.com/lenucksi/rig-for-red/commit/9526809153ad42f7ab241d7868c79954128c27b2))

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
