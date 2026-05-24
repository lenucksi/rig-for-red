# Changelog

## [0.2.4](https://github.com/lenucksi/rig-for-red/compare/v0.2.3...v0.2.4) (2026-05-24)


### Bug Fixes

* remove redundante async_reload_entry + add_update_listener (verursacht Endlos-Rekursion bei Reconfigure) ([644e78c](https://github.com/lenucksi/rig-for-red/commit/644e78c1c89e626a1d6dec682e240f5e2c651f1b))
* renovate config — helpers:pinGitHubActionsDigests + separateMinor ([320f0b1](https://github.com/lenucksi/rig-for-red/commit/320f0b13705562ec251a1c2f5d614105498e8d50))

## [0.2.3](https://github.com/lenucksi/rig-for-red/compare/v0.2.2...v0.2.3) (2026-05-24)


### Bug Fixes

* set_manual_control Domain + AL-Race-Condition beim Aktivieren und Restoren ([365e9a4](https://github.com/lenucksi/rig-for-red/commit/365e9a40762cd387070f47baaba29e13d96c0b30))

## [0.2.2](https://github.com/lenucksi/rig-for-red/compare/v0.2.1...v0.2.2) (2026-05-21)


### Bug Fixes

* add data section to reconfigure step, fix cog check CI ([c133edc](https://github.com/lenucksi/rig-for-red/commit/c133edce0e94efddecdbfd72174f567ab5baa535))
* add documentation to manifest, fix cog install in CI ([bbc7963](https://github.com/lenucksi/rig-for-red/commit/bbc796399dbfe05d97b8f4b67a2794c4760456b3))
* add issue_tracker to manifest, fix cog check range ([3f48639](https://github.com/lenucksi/rig-for-red/commit/3f48639b8851596b287426b238b448d256ce2d46))
* **coordinator:** off lights stay off during activation ([16d9405](https://github.com/lenucksi/rig-for-red/commit/16d9405d1980047bd4224e13b278e6342a34022f))
* **renovate:** remove deprecated vulnerabilityAlerts config ([ab21505](https://github.com/lenucksi/rig-for-red/commit/ab2150528f048000856588920b48e05374b66529))
* sort manifest keys, use cocogitto-action@v4.1.0 ([e74e102](https://github.com/lenucksi/rig-for-red/commit/e74e10267da5c42e295416adfb41645abe0f6931))

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
