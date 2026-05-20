---
id: TASK-8
title: __init__.py — Entry Setup und Teardown
status: Done
assignee: []
created_date: '2026-05-20 19:58'
updated_date: '2026-05-20 20:37'
labels: []
milestone: M2 - Coordinator Setup
dependencies:
  - TASK-7
priority: high
ordinal: 8000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
async_setup_entry, async_unload_entry, async_reload_entry in __init__.py implementieren. Platform-Forwarding zur switch-Platform.

PLATFORMS = ['switch']

async def async_setup_entry(hass, entry):
    coordinator = RigForRedCoordinator(hass, entry)
    await coordinator.async_setup()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True

async def async_unload_entry(hass, entry):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    await coordinator.async_unload()
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        del hass.data[DOMAIN][entry.entry_id]
    return unload_ok

async def async_reload_entry(hass, entry):
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 test_async_setup_entry_success: entry setup → coordinator in hass.data[DOMAIN][entry.entry_id]
- [x] #2 test_async_unload_entry: unload → hass.data[DOMAIN] hat keinen entry.entry_id Key mehr
- [x] #3 test_platform_forwarded: nach setup_entry existiert switch Plattform (entity switch.rig_for_red vorhanden)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
__init__.py mit async_setup_entry, async_unload_entry, async_reload_entry implementiert. PLATFORMS=['switch'], Coordinator-Instanziierung mit entry.runtime_data.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
__init__.py implementiert: async_setup_entry (Coordinator-Setup, Platform Forwarding, Update Listener), async_unload_entry (Coordinator-Unload, Platform Unload, Cleanup), async_reload_entry.
<!-- SECTION:FINAL_SUMMARY:END -->
