"""Read-only export of rugby.Post rows to rugby/data/archive_posts.json."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils import timezone as dj_tz

from rugby.models import Post

OUT = Path(__file__).resolve().parents[2] / "data" / "archive_posts.json"


def _iso(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    if dj_tz.is_naive(dt):
        dt = dj_tz.make_aware(dt, timezone.get_default_timezone())
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _id_gaps(ids: list[int]) -> list[int]:
    if not ids:
        return []
    lo, hi = min(ids), max(ids)
    present = set(ids)
    return [i for i in range(lo, hi + 1) if i not in present]


class Command(BaseCommand):
    help = "Export all rugby Post records to versioned JSON (no writes to Post)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--write",
            action="store_true",
            help="Write rugby/data/archive_posts.json (default: stdout report only).",
        )

    def handle(self, *args, **options):
        rows = list(Post.objects.order_by("id").values(
            "id",
            "author_id",
            "title_pl",
            "title_en",
            "text_pl",
            "text_en",
            "created_date",
            "published_date",
        ))
        now = dj_tz.now()
        published = [
            r
            for r in rows
            if r["published_date"] is not None and r["published_date"] <= now
        ]
        ids = [r["id"] for r in rows]
        gaps = _id_gaps(ids)

        payload = []
        for r in rows:
            payload.append(
                {
                    "id": r["id"],
                    "author_id": r["author_id"],
                    "title_pl": r["title_pl"],
                    "title_en": r["title_en"] or "",
                    "text_pl": r["text_pl"],
                    "text_en": r["text_en"] or "",
                    "created_date": _iso(r["created_date"]),
                    "published_date": _iso(r["published_date"]),
                }
            )

        canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        self.stdout.write(f"total_rows={len(rows)}")
        self.stdout.write(f"published_rows={len(published)}")
        self.stdout.write(f"id_gaps={gaps}")
        self.stdout.write(f"sha256={digest}")

        for r in published:
            if not (r["title_pl"] or "").strip() or not (r["text_pl"] or "").strip():
                self.stderr.write(self.style.ERROR(f"empty PL fields on published id={r['id']}"))
                return

        if options["write"]:
            OUT.parent.mkdir(parents=True, exist_ok=True)
            OUT.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            self.stdout.write(self.style.SUCCESS(f"wrote {OUT}"))
