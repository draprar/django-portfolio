"""Compare published practice exercises in the database with the JSON catalog."""

import json

from django.core.management.base import BaseCommand

from poligon.content_validation import load_exercises
from poligon.models import Exercise


class Command(BaseCommand):
    help = "Print how many published practice exercises were added, removed, or changed."

    def handle(self, *args, **options):
        incoming = {
            item["slug"]: item
            for item in load_exercises()
            if item.get("publication_status") == "published" and item.get("catalog_role", "practice") == "practice"
        }
        stored = {
            row.slug: row
            for row in Exercise.objects.filter(publication_status="published", catalog_role="practice")
        }
        added = sorted(set(incoming) - set(stored))
        removed = sorted(set(stored) - set(incoming))
        changed = sorted(
            slug
            for slug in set(incoming) & set(stored)
            if (stored[slug].prompt_en or "") != (incoming[slug].get("prompt_en") or "")
        )
        report = {
            "was": len(stored),
            "incoming": len(incoming),
            "added": added,
            "removed": removed,
            "changed": changed,
        }
        self.stdout.write(json.dumps(report, ensure_ascii=False))
        self.stdout.write(
            f"published was {len(stored)} incoming {len(incoming)} "
            f"added {len(added)} removed {len(removed)} changed {len(changed)}"
        )
