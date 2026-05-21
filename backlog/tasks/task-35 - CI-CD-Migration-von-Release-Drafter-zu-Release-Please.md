---
id: TASK-35
title: 'CI/CD: Migration von Release Drafter zu Release Please'
status: In Progress
assignee:
  - '@agent-k'
created_date: '2026-05-21 16:05'
updated_date: '2026-05-21 16:06'
labels: []
dependencies: []
references:
  - .github/release-drafter.yml
  - .github/workflows/release-drafter.yml
priority: medium
ordinal: 34000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Vollständige Umstellung von release-drafter/release-drafter auf googleapis/release-please-action@v4 für semantische Versionierung, auto-CHANGELOG und automatisierte GitHub Releases.

Erforderlich: Alle zukünftigen Commits müssen Conventional Commits Convention folgen: feat:, fix:, BREAKING CHANGE:, chore:, docs:, ci:, refactor:, test:

Vergleich:
| Kriterium | Release Drafter (alt) | Release Please (neu) |
|---|---|---|
| Versionierung | ❌ Nur Notizen, kein Bump | ✅ Auto-Bump aus Conventional Commits |
| CHANGELOG.md | ❌ Nicht generiert | ✅ Auto-generiert |
| manifest.json Bump | ❌ Manuell nötig | ✅ Auto via extra-files Config |
| Release | Draft → manuell publish | PR → Merge → Auto-Release + Tag |
| Commit-Format | Beliebig (PR-Labels) | Erzwungen (Conventional Commits) |
| Setup-Komplexität | ✅ Einfach | ⚠️ Höher (Config + Convention) |
| Fehleranfälligkeit | ✅ Niedrig (passiv, nie broken) | ⚠️ Höher (aktive Changes bei Release)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 release-drafter.yml Config + Workflow gelöscht
- [ ] #2 .github/workflows/release-please.yml erstellt (on push to main)
- [ ] #3 release-please-config.json mit extra-files für manifest.json
- [ ] #4 .release-please-manifest.json mit aktueller Version
- [ ] #5 CHANGELOG.md initialisiert (Markdown)
- [ ] #6 pre-commit.yml trigger auf main statt master
- [ ] #7 Release Please erzeugt Release-PR bei nächstem push mit conventional commit
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. release-please-config.json + .release-please-manifest.json erstellen\n2. .github/workflows/release-please.yml erstellen\n3. Release Drafter Workflow + Config löschen\n4. pre-commit.yml fixen (master→main)\n5. CHANGELOG.md initialisieren\n6. manifest.json auf 0.2.0\n7. Commit, Branch umbenennen, pushen, Release erstellen
<!-- SECTION:PLAN:END -->
