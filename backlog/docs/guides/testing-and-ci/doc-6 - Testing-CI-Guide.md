---
id: doc-6
title: Testing & CI Guide
type: guide
created_date: '2026-05-21 15:29'
updated_date: '2026-05-21 15:30'
---
# Testing & CI Guide für HA Custom Components

> Dieses Dokument beschreibt die Test- und CI/CD-Infrastruktur für "Rig for Red"
> und dient als **Vorlage für zukünftige HA Custom Components**.
> Jede Sektion ist so geschrieben, dass sie unabhängig verstanden werden kann.

---

## 1. Übersicht

Eine HA Custom Component braucht drei Dinge, um maintainable zu sein: | Bereich | Warum | --------- | ------- | **Reproduzierbare Tests** | Jeder Entwickler (und CI) muss exakt die gleichen Testergebnisse bekommen | **Multi-Release Testing** | HA erscheint alle 2-4 Wochen — Kompatibilität zu mehreren Versionen muss sichergestellt sein | **Automatisierte Releases** | Changelog, Versionierung, HASSfest/HACS-Validierung — alles automatisiert | Dieses Setup löst alle drei Anforderungen mit zwei komplementären Ansätzen:

- **Docker (schnell, für stabile Releases)**: Baut gegen PyPI-package `homeassistant`
- **Core-Venv (aufwändig, für dev-Branch)**: Klont HA Core und testet in einer venv

---

## 2. Lokale Entwicklung

### 2.1. Docker (Path A — empfohlen für schnelle Tests)

Der einfachste Weg, Tests zu laufen — kein HA-Core-Klon nötig.

```bash
# Bauen (installiert homeassistant und Test-Deps in ein Docker-Image)
docker build -t rig-for-red-test -f Dockerfile.test .

# Testen
docker run --rm rig-for-red-test

# Mit Coverage (durch setup.cfg automatisch aktiviert)
docker run --rm rig-for-red-test --cov-report=term-missing

# Gegen eine andere HA-Version testen
docker build --build-arg HA_VERSION=2026.1.3 -t rig-for-red-test -f Dockerfile.test .
docker run --rm rig-for-red-test
```

**Wie Dockerfile.test funktioniert:**

```dockerfile
ARG HA_VERSION=2026.2.3                    # Baubares HA-Release
FROM python:3.13-slim
ARG HA_VERSION
RUN pip install --no-cache-dir \
    homeassistant==${HA_VERSION} \          # PyPI-Paket, kein Core-Klon
    pytest-homeassistant-custom-component \ # HA-Test-Fixtures + Mock-Komponenten
    pytest-cov \
    freezegun                               # Datum-Mocking für Zeit-Tests
COPY custom_components/rig_for_red/ ...     # Unsere Component
COPY tests/ ...                              # Unsere Tests
COPY setup.cfg /app/                         # pytest + coverage defaults
WORKDIR /app
ENV PYTHONPATH="/app"                       # custom_components importierbar
ENTRYPOINT ["python3", "-m", "pytest"]      # docker run = pytest
CMD ["tests/components/rig_for_red/"]        # default: unsere Test-Suite
```

**Vorteile Docker-Ansatz:**
- ✅ Kein HA-Core-Klon nötig (spart ~2GB + 5 Minuten)
- ✅ Vollständig reproduzierbar (gleiche Umgebung = gleiche Ergebnisse)
- ✅ Schnell: 1-2 Minuten Build, 2 Sekunden Tests
- ✅ Exakt gleicher Build in CI

**Nachteile:**
- ❌ Funktioniert nur mit PyPI-Releases (kein dev-Branch)
- ❌ Kein Zugriff auf HA-Core-Source-Code zum Debuggen

### 2.2. Core-Venv (Path B — für dev-Branch-Testing)

Wenn du gegen den `dev`-Branch von HA testen musst (z.B. für Kompatibilität vor einem Release):

```bash
# 1. HA Core klonen
git clone https://github.com/home-assistant/core.git

# 2. Venv erstellen
python3 -m venv .venv
source .venv/bin/activate

# 3. HA + Test-Deps installieren
uv pip install -r core/requirements.txt
uv pip install -r core/requirements_test.txt

# 4. Dev-Deps (pytest-cov, freezegun)
uv pip install pytest-cov freezegun

# 5. HA als Paket installieren (editable)
uv pip install -e core/

# 6. Symlinks setzen (Custom Component + Tests in Core-Baum)
ln -fs "$PWD/custom_components/rig_for_red" core/homeassistant/components/rig_for_red
mkdir -p core/tests/components
ln -fs "$PWD/tests/components/rig_for_red" core/tests/components/rig_for_red
ln -fs "$PWD/tests/conftest.py" core/tests/conftest.py

# 7. Testen (von INNERHALB des Core-Baums)
cd core
python3 -m pytest tests/components/rig_for_red -v --tb=short
```

**Warum Symlinks?**  
HA Components tests müssen **innerhalb** des Core-Baums laufen (`core/homeassistant/components/`), weil HA's Import-System und die Test-Fixtures darauf ausgelegt sind. Der Symlink trickst das System aus: unsere Dateien leben im Repo-Root, sind aber im Core-Baum sichtbar.

---

## 3. Test-Struktur

```
tests/
  conftest.py                                    # Root-Fixtures (für alle Komponenten)
  components/
    __init__.py
    rig_for_red/                                 # Komponenten-spezifische Tests
      __init__.py                                # MockConfigEntry, Hilfsfunktionen
      conftest.py                                # Komponenten-Fixtures
      test_config_flow.py                        # Config-Flow-Tests
      test_coordinator.py                        # Coordinator-Tests
      test_switch.py                             # Entity-Tests
      test_init.py                               # Setup/Unload-Tests
```

**Warum `tests/components/<domain>/`?**  
Das ist die HA-Core-Konvention. Tests in diesem Pfad können direkt im Core-Baum verwendet werden (Symlink von `core/tests/components/rig_for_red` → `tests/components/rig_for_red`). Außerdem erkennt `pytest-homeassistant-custom-component` diesen Pfad und aktiviert die richtigen Plugins.

### MockConfigEntry

HA 2026.x hat einen strengen `ConfigEntry.__init__`, der viele Parameter verlangt. Unser `MockConfigEntry` in `tests/conftest.py` kapselt das:

```python
class MockConfigEntry(ConfigEntry):
    def __init__(self, *, domain, data, entry_id=None, **kwargs):
        super().__init__(
            version=kwargs.pop("version", 1),
            minor_version=kwargs.pop("minor_version", 1),
            domain=domain,
            title=kwargs.pop("title", ""),
            source=kwargs.pop("source", "user"),
            data=data.copy(),                      # <-- copy() verhindert Mutation
            options=kwargs.pop("options", {}),
            unique_id=kwargs.pop("unique_id", None),
            discovery_keys=kwargs.pop("discovery_keys", {}),
            subentries_data=kwargs.pop("subentries_data", None),
            pref_disable_new_entities=...,
            pref_disable_polling=...,
        )
        if entry_id is not None:
            object.__setattr__(self, "entry_id", entry_id)

    def add_to_hass(self, hass):
        self._hass = hass
        hass.config_entries._entries[self.entry_id] = self
```

**Wichtige Details:**
- `data.copy()` — ConfigEntry speichert Daten als FrozenDict; Kopie verhindert Seiteneffekte
- `object.__setattr__` — ConfigEntry verwendet `__setattr__`-Sperre ("entry_id kann nur einmal gesetzt werden")
- `_entries` ist ein `UserDict`, kein `dict` oder `list` — also `_entries[self.entry_id] = self`

---

## 4. Multi-Release Testing — Strategie

### 4.1. Welche Versionen testen?

Die Faustregel: **Letzte 5-6 stabile Minor-Releases + dev-Branch**.

HA verwendet CalVer: `YYYY.MM.PATCH` (z.B. 2026.2.3 = Februar 2026, 3. Patch).
- Neue Minor-Releases erscheinen alle 2-4 Wochen
- Patch-Releases fast wöchentlich
- Der dev-Branch ist immer die neueste (ungefrorene) Entwicklung

### 4.2. Python-Version-Mapping

HA wechselt die Python-Version etwa 1x pro Jahr. Aktuell:

| HA Version | Python | Grund |
|------------|--------|-------|
| ≤ 2025.1 | 3.12 | Letzte 3.12-Release |
| 2025.2 – 2026.2 | 3.13 | Hauptversion 2025–Anfang 2026 |
| ≥ 2026.3 | 3.14 | Python 3.14 Upgrade |
| dev | 3.14 | Entwicklungs-Branch |

### 4.3. Implementierung der Matrix

**Docker-Job (stabile Releases):** Jede Matrix-Zelle baut ein Docker-Image mit `HA_VERSION` als Build-Arg und führt `docker run` aus. Docker cached Schichten: nur wenn `HA_VERSION` wechselt, wird neu installiert.

**Dev-Job:** Klont HA-Core (Branch `dev`), erstellt venv, installiert Dependencies, setzt Symlinks und führt pytest direkt aus — völlig getrennt vom Docker-Ansatz.

### 4.4. Auto-Update der Matrix

Das Script `scripts/update-test-matrix.py` läuft wöchentlich per GitHub Actions:

1. **Fetch**: Holt alle Tags von `github.com/home-assistant/core`
2. **Filter**: Nur stabile Releases ≥ 2025.1
3. **Group**: Für jedes Minor-Release (YYYY.MM) das höchste Patch
4. **Map**: Python-Version pro HA-Release (Tabelle oben)
5. **Write**: Aktualisiert `pytest.yaml` mit neuem `include:`-Block
6. **PR**: Erstellt einen Pull-Request mit den Änderungen (via `peter-evans/create-pull-request`)

```python
# Kern-Logik von update-test-matrix.py:
def get_python_version(ha_version: str) -> str:
    year, month = parse(ha_version)
    if year == 2025 and month <= 1:  return "3.12"
    if year > 2026 or (year == 2026 and month >= 3):  return "3.14"
    return "3.13"
```

---

## 5. CI/CD in GitHub Actions

### 5.1. Workflow-Übersicht

| Workflow | Wann | Was |
|----------|------|-----|
| `pytest.yaml` | Push/PR zu main | Matrix-Tests (Docker für stable, Core-Venv für dev) |
| `update-test-matrix.yaml` | Wöchentlich (Mo 9:00 UTC) | Aktualisiert HA-Version-Matrix, erstellt PR |
| `hassfest.yaml` | Push/PR + täglich | HA's eigener Validator (manifest.json, icons, translations) | `validate.yml` | Push/PR | HACS-Validierung | `release-drafter.yml` | Push zu main + PR-Events | Generiert Release-Notes aus PR-Titeln | `renovate.yml` | Täglich 3:00 UTC | Auto-Updates für Dependencies | ### 5.2. pytest.yaml im Detail

```yaml
jobs:
  test-docker:
    strategy:
      matrix:
        include:
          - core-version: "2026.1.3"
            python-version: "3.13"
          - core-version: "2026.2.3"
            python-version: "3.13"
    steps:
      - uses: actions/checkout@v4
      - run: docker build --build-arg HA_VERSION=${{ matrix.core-version }} -t rig-for-red-test -f Dockerfile.test .
      - run: docker run --rm rig-for-red-test --timeout=30

  test-dev:
    steps:
      - uses: actions/checkout@v4
      - uses: actions/checkout@v4
        with:
          repository: home-assistant/core
          path: core
          ref: dev
      - uses: actions/setup-python@v5
        with: { python-version: "3.14" }
      - uses: astral-sh/setup-uv@v8
      - run: uv venv && snip run -- uv pip install -r core/requirements.txt ...
      - run: ln -fs ...   # Symlinks setzen
      - run: cd core && python3 -m pytest tests/components/rig_for_red
```

**Wichtige Design-Entscheidungen:**
- `fail-fast: false` — Alle Matrix-Jobs laufen auch wenn einer fehlschlägt
- `concurrency` — Laufende Workflows werden bei neuem Push gecancelt
- Docker-Jobs und Dev-Job sind **unabhängig** — der Dev-Job kann fehlschlagen ohne die stabilen Tests zu blockieren

### 5.3. Release Drafter

Der [Release Drafter](https://github.com/release-drafter/release-drafter) erstellt automatisch Release-Notes:

**`.github/release-drafter.yml`** (Konfiguration):
```yaml
categories:
  - title: "Features"
    labels: [feature, enhancement]
  - title: "Bug Fixes"
    labels: [bug, fix]
  - title: "Maintenance"
    labels: [chore, ci, refactor, dependencies]
template: | ## Changes
  $CHANGES
```

**`.github/workflows/release-drafter.yml`** (Workflow):
```yaml
on:
  push: { branches: [main] }
jobs:
  update_release_draft:
    steps:
      - uses: release-drafter/release-drafter@v6
```

**Wie es funktioniert:**
1. Du erstellst PRs mit Labels (`feature`, `bug`, `chore`, etc.)
2. Bei Push zu `main` aktualisiert Release Drafter einen Release-Entwurf
3. PRs werden nach Label in Kategorien gruppiert
4. Wenn du einen GitHub Release publishst, sind die Notes fertig

### 5.4. Renovate

[Renovate](https://docs.renovatebot.com/) aktualisiert automatisch Dependencies.

**Warum Renovate statt Dependabot?**
- Gruppiert Updates (z.B. alle dev-dependencies in einem PR)
- Auto-merge für Minor/Patch (spart manuelles Mergen)
- Dependency Dashboard (Übersicht aller pending Updates)
- SHA-Pinning für GitHub Actions (Sicherheit)

**`.github/renovate.json`** (Auszug):
```json
{
  "extends": ["config:recommended", "helpers:pinGitHubActionDigests"],
  "dependencyDashboard": true,
  "packageRules": [
    {
      "matchManagers": ["github-actions"],
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true
    },
    {
      "matchManagers": ["pip_requirements"],
      "groupName": "dev dependencies"
    }
  ]
}
```

---

## 6. Release-Prozess

Ein Release von "Rig for Red" läuft so ab:

1. **Features/Bugs** werden als PRs mit Labels gemerged
2. **Release Drafter** sammelt alle Merges → Release-Entwurf
3. **Maintainer** prüft, setzt Version (SemVer: `v1.0.0`, `v1.1.0`, `v2.0.0`)
4. **GitHub Release publish**: Notes sind fertig, Changelog ist da
5. **HACS** erkennt das neue Tag und bietet Update an
6. **Renovate** updated weiterhin Dependencies automatisch

Für Versionierung gilt: **Semantic Versioning 2.0.0**
- `MAJOR` — Breaking Changes (Config-Format, API)
- `MINOR` — Neue Features (rückwärtskompatibel)
- `PATCH` — Bugfixes

---

## 7. Reusability-Template

So überträgst du dieses Setup auf ein **neues HA Custom Component**:

### Checkliste

- [ ] `Dockerfile.test` kopieren, `rig_for_red` → `dein_domain` ersetzen
- [ ] `setup.cfg` kopieren (enthält pytest + coverage config)
- [ ] `tests/conftest.py` kopieren, `MockConfigEntry` + Fixtures anpassen
- [ ] Tests in `tests/components/<domain>/` schreiben
- [ ] `.github/workflows/pytest.yaml` kopieren, Domain ersetzen
- [ ] `.github/workflows/update-test-matrix.yaml` kopieren
- [ ] `scripts/update-test-matrix.py` kopieren
- [ ] `.github/renovate.json` kopieren
- [ ] `.github/release-drafter.yml` kopieren
- [ ] `.github/workflows/hassfest.yaml` kopieren
- [ ] `.github/workflows/validate.yml` kopieren

### Anpassungen für `update-test-matrix.py`

```python
# 1. MIN_VERSION anpassen (wie weit zurück unterstützen?)
MIN_VERSION = (2025, 1)

# 2. Python-Version-Mapping anpassen (falls nötig)
def get_python_version(ha_version: str) -> str:
    ...

# 3. Workflow-Pfad anpassen (falls pytest.yaml anders heißt)
workflow_path = REPO_ROOT / ".github/workflows/pytest.yaml"
```

### Minimal-Variante (ohne Matrix)

Nur Docker, kein dev-Branch-Testing:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t test -f Dockerfile.test .
      - run: docker run --rm test
```

---

## 8. Troubleshooting

### StateMachine hat kein `__contains__`

```python
# ❌ FALSCH — Home Assistant's StateMachine unterstützt kein `in`
if entity_id in hass.states:
    ...

# ✅ RICHTIG
if hass.states.get(entity_id) is not None:
    ...
```

### ServiceNotFound in Tests

Wenn ein Test `ServiceNotFound` wirft, fehlt die Service-Registrierung:

```python
# Im conftest.py Fixture registrieren (autouse=True):
@pytest.fixture(autouse=True)
def mock_light_services(hass):
    hass.services.async_register("light", "turn_on", lambda x: None)
    hass.services.async_register("light", "turn_off", lambda x: None)
```

### ConfigEntry.__init__ Signature

Die `__init__`-Signatur von ConfigEntry ändert sich zwischen HA-Releases. In 2026.x:

```python
ConfigEntry.__init__(
    version, minor_version, domain, title, source, data, options,
    unique_id, discovery_keys, subentries_data,
    pref_disable_new_entities, pref_disable_polling,
)
```

Unser `MockConfigEntry` kapselt das und federt API-Änderungen ab.

### DeprecationWarnings in Tests

utcnow() ist deprecated ab Python 3.12+:

```python
# ❌ Deprecated
datetime.utcnow()

# ✅ Richtig (timezone-aware)
datetime.now(datetime.UTC)

# ✅ Für Tests: freezegun fixture nutzen
```

### dev-Branch schlägt dauernd fehl

Der dev-Branch von HA ändert sich täglich. Wenn Tests dort fehlschlagen:
1. Prüfen ob es ein HA-API-Break ist (dann anpassen)
2. Oder ein Test-Infrastruktur-Problem (dann dev-Job temporär deaktivieren über `if: false`)

Der dev-Job sollte **nie required** sein (blockiert keine PR-Merges).

---

## 9. Referenzen

- [Dockerfile.test](../../Dockerfile.test) — Unser Docker-Test-Setup
- [scripts/update-test-matrix.py](../../scripts/update-test-matrix.py) — Matrix-Update-Script
- [.github/workflows/pytest.yaml](../../.github/workflows/pytest.yaml) — Haupt-Test-Workflow
- [.github/workflows/update-test-matrix.yaml](../../.github/workflows/update-test-matrix.yaml) — Matrix-Update-Workflow
- [.github/release-drafter.yml](../../.github/release-drafter.yml) — Release-Drafter-Konfig
- [.github/renovate.json](../../.github/renovate.json) — Renovate-Konfig
- [tests/conftest.py](../../tests/conftest.py) — Test-Fixtures
- [HA Core CI (adaptiv lighting)](https://github.com/basnijholt/adaptive-lighting/tree/master/.github) — Inspiration
