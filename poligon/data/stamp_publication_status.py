"""One-shot: write publication fields into exercise JSON.

The files are the source of truth. Slugs that were on the live allowlist stay
published and are marked legacy. Everything else stays a draft. Safe to run
again: an existing publication_status is left alone.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    published = set(json.loads((ROOT / "active_slugs.json").read_text(encoding="utf-8")))
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    for relative in manifest["exercises"]:
        path = ROOT / relative
        rows = json.loads(path.read_text(encoding="utf-8"))
        for item in rows:
            if "publication_status" not in item:
                live = item["slug"] in published
                item["publication_status"] = "published" if live else "draft"
                item["quality_status"] = "legacy" if live else ""
            item.setdefault("scenario", "")
            item.setdefault("subskill", "")
            item.setdefault("learning_objective", "")
            item.setdefault("competency", "")
            item.setdefault("success_criteria", [])
            item.setdefault("review_status", "")
            item.setdefault("reviewed_by", "")
            if "source_type" not in item:
                source = item.get("content_source") or "original"
                item["source_type"] = "original" if source == "original" else "external"
            item.pop("active", None)
        path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"updated {len(manifest['exercises'])} files")


if __name__ == "__main__":
    main()
