"""Validation utilities for MaholoBioBench config files."""

from __future__ import annotations

from pathlib import Path

from .paths import EPISODE_OUTPUT_SCHEMA, PROTOCOL_STATE_SCHEMA, TASK_REGISTRY
from .registry import load_yaml, phase_b_task_families, task_family_map


REQUIRED_FAMILY_FIELDS = {
    "family_id",
    "level",
    "category",
    "summary",
    "success",
    "metrics",
    "instances",
    "variations",
}

MINIMAL_FUTURE_FAMILY_FIELDS = {
    "family_id",
    "level",
    "category",
    "summary",
    "metrics",
    "variations",
}


def validate_registry(path: Path = TASK_REGISTRY) -> list[str]:
    errors: list[str] = []
    registry = load_yaml(path)
    families = task_family_map(registry)
    phase_b = set(phase_b_task_families(registry))

    missing_phase = sorted(phase_b - set(families))
    if missing_phase:
        errors.append(f"Phase B families missing from registry: {missing_phase}")

    for family_id, family in families.items():
        required_fields = REQUIRED_FAMILY_FIELDS
        if family.get("phase") == "future" and family_id not in phase_b:
            required_fields = MINIMAL_FUTURE_FAMILY_FIELDS

        missing_fields = sorted(required_fields - set(family))
        if missing_fields:
            errors.append(f"{family_id}: missing fields {missing_fields}")

        if "instances" in required_fields and not family.get("instances"):
            errors.append(f"{family_id}: instances must not be empty")
        if not family.get("variations"):
            errors.append(f"{family_id}: variations must not be empty")
        if not family.get("metrics"):
            errors.append(f"{family_id}: metrics must not be empty")
        if "success" in required_fields and not family.get("success"):
            errors.append(f"{family_id}: success contract must not be empty")

    return errors


def validate_all() -> list[str]:
    errors: list[str] = []
    for path in [TASK_REGISTRY, PROTOCOL_STATE_SCHEMA, EPISODE_OUTPUT_SCHEMA]:
        try:
            load_yaml(path)
        except Exception as exc:  # noqa: BLE001 - report validation failures cleanly
            errors.append(f"{path}: {exc}")
    errors.extend(validate_registry(TASK_REGISTRY))
    return errors


def main() -> None:
    errors = validate_all()
    if errors:
        print("MaholoBioBench config validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("MaholoBioBench config validation passed.")


if __name__ == "__main__":
    main()
