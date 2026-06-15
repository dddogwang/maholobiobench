#!/usr/bin/env python3
"""Sync the presentation asset inventory from robosuite Maholo MJCF assets."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BENCH_ROOT = ROOT / "maholobiobench"
ROBOSUITE_ASSETS = ROOT / "robosuite_maholo" / "robosuite" / "models" / "assets"
PRESENTATION = BENCH_ROOT / "presentation"
ENV_ASSETS_HTML = PRESENTATION / "env_assets.html"

ARENA_XMLS = [
    ROBOSUITE_ASSETS / "arenas" / "laboratory_arena_world.xml",
    ROBOSUITE_ASSETS / "arenas" / "laboratory_arena.xml",
]

MOVABLE_OBJECTS = [
    ("P1000 pipette", "P1000Pipette_withtip.xml", "可移动物品", [0.18, 0.50, 0.78]),
    ("1.5 ml tube", "1.5ml_tube.xml", "可移动物品", [0.88, 0.30, 0.26]),
]

EQUIPMENT_OBJECTS = [
    ("4°C cool incubator", "cool_incubator_4c.xml", "可交互仪器", [0.67, 0.60, 0.48]),
    ("CO2 incubator", "co2_incubator.xml", "可交互仪器", [0.66, 0.62, 0.52]),
    ("Deep freezer", "deep_freezer.xml", "可交互仪器", [0.62, 0.66, 0.71]),
    ("Thermal cycler", "thermal_cycler.xml", "实验仪器", [0.45, 0.45, 0.50]),
    ("MX-307", "mx307.xml", "实验仪器", [0.52, 0.52, 0.47]),
    ("Microtube mixer", "microtube_mixer.xml", "实验仪器", [0.42, 0.47, 0.58]),
    ("Vortex mixer", "vortex_mixer.xml", "实验仪器", [0.38, 0.49, 0.62]),
    ("Block thermostatic bath", "block_thermostatic_bath.xml", "实验仪器", [0.52, 0.58, 0.52]),
    ("Cool block bath", "cool_block_bath.xml", "实验仪器", [0.44, 0.58, 0.64]),
]

FORCE_OBJECT_STATUS = {
    "cool_incubator_4c.xml": "done",
    "co2_incubator.xml": "done",
    "deep_freezer.xml": "done",
    "block_thermostatic_bath.xml": "todo",
    "cool_block_bath.xml": "todo",
}

BASE_TABLE_MESHES = {
    "base_robot",
    "base_centrifuge",
    "base_deep_freezer",
    "table_main",
    "table_side_R1_FF",
    "table_side_R2",
    "table_incubator",
}

ARENA_COLOR_DONE = [0.42, 0.56, 0.50]
ARENA_COLOR_TODO = [0.68, 0.54, 0.31]


@dataclass
class MeshEntry:
    name: str
    file: str


@dataclass
class AssetCard:
    title: str
    category: str
    status: str
    note: str
    color: list[float]
    files: list[str]


def safe_rel(path: str) -> str:
    return path.replace("μ", "u")


def copy_mesh(source_root: Path, mesh_rel: str, dest_kind: str) -> str:
    rel = mesh_rel.removeprefix("meshes/")
    dest_rel = safe_rel(rel)
    source = source_root / rel
    dest = PRESENTATION / "assets" / "models" / dest_kind / dest_rel
    if not source.exists():
        raise FileNotFoundError(f"Missing source mesh: {source}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)
    return str(Path("assets") / "models" / dest_kind / dest_rel)


def parse_xml(path: Path) -> tuple[dict[str, MeshEntry], list[ET.Element], dict[ET.Element, ET.Element]]:
    root = ET.parse(path).getroot()
    meshes = {
        mesh.attrib["name"]: MeshEntry(mesh.attrib["name"], mesh.attrib["file"])
        for mesh in root.findall(".//mesh")
        if "name" in mesh.attrib and "file" in mesh.attrib
    }
    geoms = root.findall(".//geom")
    parents = {child: parent for parent in root.iter() for child in parent}
    return meshes, geoms, parents


def is_visual(geom: ET.Element) -> bool:
    name = geom.attrib.get("name", "").lower()
    return (
        geom.attrib.get("class") == "visual"
        or geom.attrib.get("group") == "1"
        or "visual" in name
        or (geom.attrib.get("contype") == "0" and geom.attrib.get("conaffinity") == "0")
    )


def is_collision(geom: ET.Element) -> bool:
    name = geom.attrib.get("name", "").lower()
    return geom.attrib.get("class") == "collision" or geom.attrib.get("group") == "0" or "collision" in name or "_col" in name


def body_ancestors(geom: ET.Element, parents: dict[ET.Element, ET.Element]) -> list[ET.Element]:
    bodies = []
    node = geom
    while node in parents:
        node = parents[node]
        if node.tag == "body":
            bodies.append(node)
    return bodies


def arena_cards() -> list[AssetCard]:
    by_title: dict[str, AssetCard] = {}
    collision_names: set[str] = set()
    arena_mesh_root = ROBOSUITE_ASSETS / "arenas" / "meshes"

    for xml in ARENA_XMLS:
        meshes, geoms, parents = parse_xml(xml)
        collision_names.update(g.attrib.get("mesh", "") for g in geoms if is_collision(g) and g.attrib.get("mesh"))
        for geom in geoms:
            mesh_name = geom.attrib.get("mesh")
            if not mesh_name or not is_visual(geom) or mesh_name not in meshes:
                continue
            if mesh_name in by_title:
                continue

            body_collisions: set[str] = set()
            bodies = body_ancestors(geom, parents)
            nearest_body = bodies[0] if bodies else None
            if nearest_body is not None:
                body_collisions = {
                    g.attrib["mesh"]
                    for g in nearest_body.findall(".//geom")
                    if g.attrib.get("mesh") and is_collision(g)
                }

            if mesh_name in BASE_TABLE_MESHES:
                status = "done" if len([n for n in collision_names if n.startswith("maholo_arena")]) > 1 else "todo"
                note = "arena base/table 使用 maholo_arena01-14 多段 collision mesh；冲撞模型已制作。"
            elif len(body_collisions) > 1:
                status = "done"
                note = f"使用 {len(body_collisions)} 个 collision mesh；冲撞模型已制作。"
            else:
                status = "todo"
                note = "仅使用同一 mesh 作为单段 collision；尚未做多段冲撞模型。"

            file_ref = copy_mesh(arena_mesh_root, meshes[mesh_name].file, "arenas")
            by_title[mesh_name] = AssetCard(
                title=mesh_name,
                category="固定场景",
                status=status,
                note=note,
                color=ARENA_COLOR_DONE if status == "done" else ARENA_COLOR_TODO,
                files=[file_ref],
            )

    ordered = []
    seen = set()
    for preferred in [
        "base_robot",
        "base_centrifuge",
        "base_deep_freezer",
        "table_main",
        "table_side_R1_FF",
        "table_side_R2",
        "table_incubator",
    ]:
        if preferred in by_title:
            ordered.append(by_title[preferred])
            seen.add(preferred)
    ordered.extend(card for key, card in by_title.items() if key not in seen)
    return ordered


def object_card(title: str, xml_name: str, category: str, color: list[float], dest_kind: str) -> AssetCard:
    xml = ROBOSUITE_ASSETS / "objects" / xml_name
    meshes, geoms, _parents = parse_xml(xml)
    visual_refs = []
    collision_refs = set()
    for geom in geoms:
        mesh_name = geom.attrib.get("mesh")
        if not mesh_name or mesh_name not in meshes:
            continue
        if is_visual(geom):
            visual_refs.append(mesh_name)
        if is_collision(geom):
            collision_refs.add(mesh_name)

    if not visual_refs:
        visual_refs = [name for name in meshes if "collision" not in name.lower()]

    files = []
    for mesh_name in dict.fromkeys(visual_refs):
        files.append(copy_mesh(ROBOSUITE_ASSETS / "objects" / "meshes", meshes[mesh_name].file, dest_kind))

    status = FORCE_OBJECT_STATUS.get(xml_name)
    if status is None:
        status = "done" if len(collision_refs) > 1 else "todo"
    note = (
        f"来自 {xml_name}；{len(files)} 个 visual mesh；{len(collision_refs)} 个 collision mesh。"
        if status == "done"
        else f"来自 {xml_name}；{len(files)} 个 visual mesh；尚未形成多段 collision / 交互状态。"
    )
    return AssetCard(title, category, status, note, color, files)


def js_value(value) -> str:
    return json.dumps(value, ensure_ascii=False)


def js_card(card: AssetCard) -> str:
    return "\n".join(
        [
            "  {",
            f"    title: {js_value(card.title)}, category: {js_value(card.category)}, status: {js_value(card.status)},",
            f"    note: {js_value(card.note)},",
            f"    color: {js_value(card.color)},",
            f"    files: {js_value(card.files)}",
            "  }",
        ]
    )


def js_array(name: str, cards: list[AssetCard]) -> str:
    return f"const {name} = [\n" + ",\n".join(js_card(card) for card in cards) + "\n];"


def update_html(arena: list[AssetCard], equipment: list[AssetCard], movable: list[AssetCard], dry_run: bool) -> bool:
    html = ENV_ASSETS_HTML.read_text()
    all_count = len(arena) + len(equipment) + len(movable)
    html = re.sub(r'data-filter="all"><span data-i18n="assets\.filter_all">全部</span><span class="tab-count">\d+</span>', f'data-filter="all"><span data-i18n="assets.filter_all">全部</span><span class="tab-count">{all_count}</span>', html)
    html = re.sub(r'data-filter="fixed"><span data-i18n="assets\.filter_fixed">固定场景</span><span class="tab-count">\d+</span>', f'data-filter="fixed"><span data-i18n="assets.filter_fixed">固定场景</span><span class="tab-count">{len(arena)}</span>', html)
    html = re.sub(r'data-filter="instrument"><span data-i18n="assets\.filter_instrument">实验仪器</span><span class="tab-count">\d+</span>', f'data-filter="instrument"><span data-i18n="assets.filter_instrument">实验仪器</span><span class="tab-count">{len(equipment)}</span>', html)
    html = re.sub(r'data-filter="movable"><span data-i18n="assets\.filter_movable">可移动物品</span><span class="tab-count">\d+</span>', f'data-filter="movable"><span data-i18n="assets.filter_movable">可移动物品</span><span class="tab-count">{len(movable)}</span>', html)

    block = "\n".join(
        [
            'const ROOT = "";',
            "const SCENE_MODELS = [",
            '  { file: "assets/models/maholo.stl", color: [0.64, 0.58, 0.47], autoFit: true }',
            "];",
            js_array("ARENA_WORLD_MODELS", arena),
            js_array("EQUIPMENT_MODELS", equipment),
            js_array("MOVABLE_MODELS", movable),
            "const MODELS = [...ARENA_WORLD_MODELS, ...EQUIPMENT_MODELS, ...MOVABLE_MODELS];",
        ]
    )
    pattern = re.compile(r'const ROOT = "";\n.*?const MODELS = \[\.\.\.ARENA_WORLD_MODELS, \.\.\.EQUIPMENT_MODELS, \.\.\.MOVABLE_MODELS\];', re.S)
    new_html, count = pattern.subn(block, html)
    if count != 1:
        raise RuntimeError(f"Expected one model constants block, found {count}")

    changed = new_html != ENV_ASSETS_HTML.read_text()
    if changed and not dry_run:
        ENV_ASSETS_HTML.write_text(new_html)
    return changed


def referenced_model_files() -> set[Path]:
    html = ENV_ASSETS_HTML.read_text()
    refs = set(re.findall(r'assets/models/[^"\']+', html))
    return {PRESENTATION / ref for ref in refs}


def prune_unreferenced_models(dry_run: bool) -> list[Path]:
    models_root = PRESENTATION / "assets" / "models"
    keep = referenced_model_files()
    removed: list[Path] = []
    for path in sorted(models_root.rglob("*"), reverse=True):
        if path.is_file() and path not in keep:
            removed.append(path)
            if not dry_run:
                path.unlink()
        elif path.is_dir() and not dry_run:
            try:
                path.rmdir()
            except OSError:
                pass
    return sorted(removed)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Generate and report without writing env_assets.html")
    parser.add_argument(
        "--keep-unused-models",
        action="store_true",
        help="Do not remove model files that are not referenced by env_assets.html",
    )
    args = parser.parse_args()

    arena = arena_cards()
    movable = [object_card(*item, dest_kind="objects") for item in MOVABLE_OBJECTS]
    equipment = [object_card(*item, dest_kind="equipments") for item in EQUIPMENT_OBJECTS]
    changed = update_html(arena, equipment, movable, args.dry_run)
    removed = [] if args.keep_unused_models else prune_unreferenced_models(args.dry_run)

    print(f"fixed scene assets: {len(arena)}")
    print(f"equipment assets: {len(equipment)}")
    print(f"movable assets: {len(movable)}")
    print(f"total cards: {len(arena) + len(equipment) + len(movable)}")
    print(f"{'would prune' if args.dry_run else 'pruned'} unused model files: {len(removed)}")
    print(("would update" if args.dry_run else "updated") + f" {ENV_ASSETS_HTML}" if changed else "env_assets.html already aligned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
