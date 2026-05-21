#!/usr/bin/env python3
"""Update the pytest workflow matrix with latest HA Core versions.

Fetches Home Assistant Core release tags from GitHub, groups by minor version
(picking the highest patch), maps Python versions, and updates
.github/workflows/pytest.yaml.  Creates a PR with the changes.

Usage:
    python scripts/update-test-matrix.py
"""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

MIN_VERSION = (2025, 1)

REPO_ROOT = Path(__file__).resolve().parent.parent


def get_ha_core_versions() -> list[str]:
    all_tags: list[dict] = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/home-assistant/core/tags?per_page=100&page={page}"
        with urllib.request.urlopen(url) as response:
            tags = json.loads(response.read().decode())
        if not tags:
            break
        all_tags.extend(tags)
        oldest_in_page = None
        for t in tags:
            if re.match(r"^\d+\.\d+\.\d+$", t["name"]):
                parts = t["name"].split(".")
                year, month = int(parts[0]), int(parts[1])
                if oldest_in_page is None or (year, month) < oldest_in_page:
                    oldest_in_page = (year, month)
        if oldest_in_page and oldest_in_page < MIN_VERSION:
            break
        page += 1
        if page > 10:
            break

    stable = re.compile(r"^\d+\.\d+\.\d+$")
    versions = [t["name"] for t in all_tags if stable.match(t["name"])]

    latest: dict[str, str] = {}
    for version in versions:
        parts = version.split(".")
        year, month = int(parts[0]), int(parts[1])
        if (year, month) >= MIN_VERSION:
            minor_key = f"{parts[0]}.{parts[1]}"
            if minor_key not in latest:
                latest[minor_key] = version
            else:
                current_patch = int(latest[minor_key].split(".")[2])
                new_patch = int(parts[2])
                if new_patch > current_patch:
                    latest[minor_key] = version

    return sorted(latest.values(), key=lambda v: [int(x) for x in v.split(".")])


def get_python_version(ha_version: str) -> str:
    parts = ha_version.split(".")
    year, month = int(parts[0]), int(parts[1])
    if year == 2025 and month <= 1:
        return "3.12"
    if year > 2026 or (year == 2026 and month >= 3):
        return "3.14"
    return "3.13"


def generate_matrix_yaml(versions: list[str]) -> str:
    lines = []
    for version in versions:
        py_ver = get_python_version(version)
        lines.append(f'          - core-version: "{version}"')
        lines.append(f'            python-version: "{py_ver}"')
    return "\n".join(lines)


def update_workflow_file(workflow_path: Path, new_matrix: str) -> bool:
    content = workflow_path.read_text()

    pattern = re.compile(
        r"(        include:\n)(.*?)(    steps:)",
        re.DOTALL,
    )

    def replacer(m: re.Match) -> str:
        return f"{m.group(1)}{new_matrix}\n{m.group(3)}"

    new_content = pattern.sub(replacer, content)
    if new_content == content:
        return False
    workflow_path.write_text(new_content)
    return True


def main() -> None:
    print("Fetching latest HA Core versions...")
    versions = get_ha_core_versions()
    print(f"Found {len(versions)} versions: {', '.join(versions)}")

    print("\nGenerating matrix...")
    matrix = generate_matrix_yaml(versions)
    print(matrix)

    workflow_path = REPO_ROOT / ".github/workflows/pytest.yaml"
    print(f"\nUpdating {workflow_path}...")
    if update_workflow_file(workflow_path, matrix):
        print("Workflow updated successfully!")
    else:
        print("No changes needed.")


if __name__ == "__main__":
    main()
