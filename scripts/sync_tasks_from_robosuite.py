#!/usr/bin/env python3
"""Sync MaholoBioBench task status from the local robosuite Maholo envs.

This script treats `tasks.html` as the public benchmark taxonomy and uses the
current robosuite implementation as evidence for each family status.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BENCH_ROOT = ROOT / "maholobiobench"
ROBOSUITE_ROOT = ROOT / "robosuite_maholo" / "robosuite"
TASKS_HTML = BENCH_ROOT / "presentation" / "tasks.html"


STATUS_TEXT = {
    "done": ("done", "tasks.status_done", "已实现"),
    "partial": ("partial", "tasks.status_partial", "部分实现"),
    "todo": ("todo", "tasks.status_todo", "未实现"),
}


@dataclass(frozen=True)
class TaskRule:
    key: str
    status: str
    required_patterns: tuple[str, ...]
    partial_patterns: tuple[str, ...] = ()
    reason: str = ""


TASK_RULES = [
    TaskRule(
        "task_reach_target_pose",
        "done",
        ("Move2Pipette", "Move2Tube"),
        reason="Move2Pipette / Move2Tube envs implement target-pose reaching tasks.",
    ),
    TaskRule(
        "task_grasp_lab_object",
        "done",
        ("Grip2Pipette",),
        reason="Grip2Pipette envs implement a lab-object grasp task.",
    ),
    TaskRule(
        "task_transport_held_object",
        "todo",
        (),
        partial_patterns=("Transport", "Place"),
        reason="No held-object transport env exists yet.",
    ),
    TaskRule(
        "task_open_articulated_equipment",
        "done",
        ("OpenCoolIncubator", "OpenDeepFreezer", "OpenCO2Incubator"),
        reason="Cool incubator, deep freezer, and CO2 incubator opening envs exist.",
    ),
    TaskRule(
        "task_press_or_toggle_instrument_control",
        "partial",
        (),
        partial_patterns=("Push2Pipette",),
        reason="Push2Pipette exists, but general instrument control tasks are not implemented.",
    ),
    TaskRule(
        "task_retrieve_container",
        "todo",
        (),
        partial_patterns=("Move2Tube",),
        reason="Move2Tube exists, but no retrieve-container task with container/sample state exists.",
    ),
    TaskRule(
        "task_transfer_liquid",
        "todo",
        (),
        partial_patterns=("TransferLiquid", "Pipette"),
        reason="No liquid transfer env or liquid-volume state exists in the Maholo env list.",
    ),
    TaskRule("task_mount_disposable_tip", "todo", (), reason="No disposable-tip mounting env exists."),
    TaskRule("task_eject_disposable_tip", "todo", (), reason="No disposable-tip ejection env exists."),
    TaskRule("task_place_container_in_storage", "todo", (), reason="No storage placement env exists."),
    TaskRule("task_mix_sample", "todo", (), reason="No sample mixing env exists."),
    TaskRule("task_cap_or_seal_container", "todo", (), reason="No cap/seal task env exists."),
    TaskRule("task_scan_or_inspect_sample", "todo", (), reason="No scan/inspect task env exists."),
    TaskRule(
        "task_retrieve_and_transfer_sample",
        "todo",
        (),
        partial_patterns=("Move2Tube", "Grip2Pipette"),
        reason="Primitive tube/reach/grip envs exist, but no sequence protocol task exists.",
    ),
    TaskRule("task_prepare_dilution_series", "todo", (), reason="No dilution-series protocol env exists."),
    TaskRule("task_pipetting_workflow_with_tip_change", "todo", (), reason="No tip-change workflow env exists."),
    TaskRule("task_sample_storage_protocol", "todo", (), reason="No sample-storage protocol env exists."),
    TaskRule("task_media_change_simplified", "todo", (), reason="No media-change protocol env exists."),
    TaskRule("task_p_c_r_plate_preparation", "todo", (), reason="No PCR plate preparation protocol env exists."),
    TaskRule("task_device_incubation_workflow", "todo", (), reason="No device incubation workflow env exists."),
]


def maholo_env_files() -> list[Path]:
    roots = [
        ROBOSUITE_ROOT / "environments" / "manipulation" / "maholoSingleEnv",
        ROBOSUITE_ROOT / "environments" / "manipulation" / "maholoBimanualEnv",
    ]
    files: list[Path] = []
    for root in roots:
        files.extend(sorted(p for p in root.glob("*.py") if p.name != "__init__.py"))
    return files


def implemented_names(files: list[Path]) -> set[str]:
    names: set[str] = set()
    for path in files:
        text = path.read_text()
        names.update(re.findall(r"^class\s+([A-Za-z0-9_]+)\(", text, re.MULTILINE))
        names.add(path.stem)
    return names


def has_any(names: set[str], patterns: tuple[str, ...]) -> bool:
    return any(pattern in name for pattern in patterns for name in names)


def resolved_status(rule: TaskRule, names: set[str]) -> str:
    if rule.required_patterns:
        return "done" if has_any(names, rule.required_patterns) else "todo"
    if rule.status == "partial" and has_any(names, rule.partial_patterns):
        return "partial"
    return rule.status


def update_tasks_html(statuses: dict[str, str], dry_run: bool) -> bool:
    text = TASKS_HTML.read_text()
    original = text
    for key, status in statuses.items():
        css_class, i18n_key, label = STATUS_TEXT[status]
        pattern = re.compile(
            rf'(<td><code data-i18n="tasks\.{re.escape(key)}">[^<]+</code></td>\s*)'
            rf'<td class="status [^"]+" data-i18n="tasks\.status_[^"]+">[^<]+</td>',
            re.MULTILINE,
        )
        replacement = (
            rf'\1<td class="status {css_class}" data-i18n="{i18n_key}">{label}</td>'
        )
        text, count = pattern.subn(replacement, text)
        if count != 1:
            raise RuntimeError(f"Expected one tasks.html row for {key}, found {count}")

    changed = text != original
    if changed and not dry_run:
        TASKS_HTML.write_text(text)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Print updates without writing tasks.html")
    args = parser.parse_args()

    files = maholo_env_files()
    names = implemented_names(files)
    statuses = {rule.key: resolved_status(rule, names) for rule in TASK_RULES}
    changed = update_tasks_html(statuses, args.dry_run)

    print(f"scanned env files: {len(files)}")
    for rule in TASK_RULES:
        status = statuses[rule.key]
        evidence = []
        for pattern in (*rule.required_patterns, *rule.partial_patterns):
            hits = sorted(name for name in names if pattern in name)
            if hits:
                evidence.extend(hits)
        evidence_text = ", ".join(evidence[:6]) if evidence else "no matching env"
        print(f"{rule.key}: {status} | {evidence_text} | {rule.reason}")
    print(("would update" if args.dry_run else "updated") + f" {TASKS_HTML}" if changed else "tasks.html already aligned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
