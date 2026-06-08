"""Task registry loading helpers."""

from pathlib import Path
from typing import Any

import yaml

from .paths import TASK_REGISTRY


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def load_task_registry(path: Path = TASK_REGISTRY) -> dict[str, Any]:
    return load_yaml(path)


def phase_b_task_families(registry: dict[str, Any] | None = None) -> list[str]:
    data = registry or load_task_registry()
    return list(data.get("phase_b_v0_1", {}).get("task_families", []))


def task_family_map(registry: dict[str, Any] | None = None) -> dict[str, dict[str, Any]]:
    data = registry or load_task_registry()
    families = data.get("task_families", [])
    return {family["family_id"]: family for family in families}

