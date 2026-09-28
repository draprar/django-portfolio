"""Drop civilian filler from Poligon JSON catalogs. Run from repo root."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from military_catalog import fix_categories, keep_exercise, keep_vocabulary  # noqa: E402


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prune_exercises(path: Path) -> tuple[int, int]:
    items = json.loads(path.read_text(encoding="utf-8"))
    kept = [fix_categories(item) for item in items if keep_exercise(item)]
    write_json(path, kept)
    return len(items), len(kept)


def prune_vocabulary(path: Path) -> tuple[int, int]:
    items = json.loads(path.read_text(encoding="utf-8"))
    source = path.name
    kept = [fix_categories(item) for item in items if keep_vocabulary(item, source=source)]
    write_json(path, kept)
    return len(items), len(kept)


def main() -> None:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    total_before = 0
    total_after = 0
    for relative in manifest["exercises"]:
        before, after = prune_exercises(ROOT / relative)
        total_before += before
        total_after += after
        print(f"exercises {relative}: {before} -> {after}")
    for relative in manifest["vocabulary"]:
        before, after = prune_vocabulary(ROOT / relative)
        total_before += before
        total_after += after
        print(f"vocabulary {relative}: {before} -> {after}")
    print(f"total: {total_before} -> {total_after}")


if __name__ == "__main__":
    main()
