---
id: TASK-51
title: RGB-Preset und Custom-Color (Rig-for-Blue)
status: Done
assignee:
  - "@agent-k"
created_date: 2026-05-28 21:35
updated_date: 2026-05-28 21:35
labels:
  - feature
dependencies: []
references:
  - docs/README.md
modified_files:
  - custom_components/rig_for_red/const.py
  - custom_components/rig_for_red/config_flow.py
  - custom_components/rig_for_red/coordinator.py
  - custom_components/rig_for_red/strings.json
  - custom_components/rig_for_red/translations/en.json
  - custom_components/rig_for_red/translations/de.json
  - tests/components/rig_for_red/conftest.py
  - tests/conftest.py
priority: medium
ordinal: 51000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Config-Option rgb_preset (red/blue/custom) mit ColorRGBSelector für individuelle Farbe statt hartcodiertem Rot.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 CONF_RGB_PRESET SelectSelector in config_flow (user+reconfigure)
- [x] #2 CONF_RGB_CUSTOM ColorRGBSelector in config_flow
- [x] #3 coordinator _rgb property löst Preset in RGB-Liste auf
- [x] #4 Alle RED_RGB Referenzen durch self._rgb ersetzt
- [x] #5 Translations: strings.json, en.json, de.json (data + selector)
- [x] #6 Test-Fixtures mock_config_entry_data um rgb_preset ergänzt
- [x] #7 102 Tests pass, ruff clean
- [x] #8 README aktualisiert
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Config-Option rgb_preset (red/blue/custom) mit ColorRGBSelector für custom Farbe. coordinator._rgb Property löst Preset in RGB-Liste auf (RED_RGB/BLUE_RGB/custom). Alle RED_RGB Referenzen durch self._rgb ersetzt. SelectSelector + ColorRGBSelector in config_flow user+reconfigure. Translations und README aktualisiert. 102 Tests pass.
<!-- SECTION:FINAL_SUMMARY:END -->