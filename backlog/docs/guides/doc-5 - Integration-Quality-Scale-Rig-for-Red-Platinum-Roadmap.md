---
id: doc-5
title: Integration Quality Scale - Rig for Red Platinum Roadmap
type: guide
created_date: '2026-05-21 13:14'
updated_date: '2026-05-21 13:14'
---
## Overview

The Home Assistant Integration Quality Scale defines four tiers: Bronze, Silver, Gold, Platinum. This document tracks Rig for Red\'s current compliance and the gaps to reach Platinum.

Reference: https://developers.home-assistant.io/docs/core/integration-quality-scale

---

## Bronze (Baseline)

### Already Compliant
- ✅ action-setup — service actions registered in `async_setup`
- ✅ config-flow — UI setup via config flow
- ✅ config-entry-unloading — `async_unload_entry` implemented
- ✅ entity-unique-id — `entry.entry_id` as unique_id
- ✅ has-entity-name — `_attr_has_entity_name = True`
- ✅ entity-translations — `_attr_translation_key = "rig_for_red"`
- ✅ docs — multiple doc files created

### Missing for Bronze
- ❌ brands — no logo/icon in repo root
- ❌ common-modules — check for extractable patterns
- ❌ config-flow-test-coverage — missing entity_not_found test path
- ❌ dependency-transparency — document dependencies
- ❌ runtime-data — still uses `hass.data[DOMAIN]` instead of `entry.runtime_data`
- ❌ test-before-configure — no connection test in config flow
- ❌ test-before-setup — no init validation
- ❌ unique-config-entry — missing unique_id in config flow

## Silver

### Already Compliant
- ✅ config-entry-unloading

### Missing for Silver
- ❌ action-exceptions — service actions don\'t raise typed exceptions
- ❌ entity-unavailable — entity unavailable not implemented
- ❌ integration-owner — CODEOWNERS exists but needs verification
- ❌ test-coverage — need >95% coverage (currently ~70%)
- ❌ docs-configuration-parameters — missing from docs
- ❌ docs-installation-parameters — missing from docs

Not applicable: reauthentication (no auth), log-when-unavailable (no device), parallel-updates (not polling)

## Gold

### Missing for Gold
- ❌ devices — no device registry
- ❌ diagnostics — not implemented
- ❌ entity-category — switch not categorized
- ❌ entity-device-class — may not apply (switch)
- ❌ entity-disabled-by-default — may not apply
- ❌ exception-translations — no translatable exceptions
- ❌ icon-translations — icon not translatable
- ❌ reconfiguration-flow — no reconfigure step
- ❌ docs-use-cases, docs-examples, docs-troubleshooting, etc.

## Platinum

### Missing for Platinum
- ❌ strict-typing — no type annotations, no mypy CI check

Not applicable: async-dependency (no external deps), inject-websession (no external deps)

---

## Priority Order

1. Bronze gaps (8 rules) — quick wins, unblocks tier
2. Test coverage to >95% (Silver)
3. Docs improvements across all tiers
4. Diagnostics, device registry, reconfigure flow (Gold)
5. Strict typing + mypy CI (Platinum)
