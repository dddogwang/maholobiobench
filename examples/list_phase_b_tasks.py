#!/usr/bin/env python3
"""Print Phase B task families and their representative instances."""

from maholobiobench.registry import load_task_registry, phase_b_task_families, task_family_map


def main() -> None:
    registry = load_task_registry()
    families = task_family_map(registry)
    for family_id in phase_b_task_families(registry):
        family = families[family_id]
        instances = [item["instance_id"] for item in family.get("instances", []) if item.get("phase") == "B"]
        print(f"{family_id}: {', '.join(instances) if instances else '(no Phase B instances)'}")


if __name__ == "__main__":
    main()

