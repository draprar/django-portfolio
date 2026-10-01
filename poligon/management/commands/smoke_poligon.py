"""A small check after seed: the queue, the placement bank, and the matrix."""

from django.core.management.base import BaseCommand, CommandError

from poligon.framework import SKILLS
from poligon.levels import LEVELS
from poligon.models import Exercise


class Command(BaseCommand):
    help = "Fail when the seeded catalog is missing a reviewed cell or the placement bank."

    def handle(self, *args, **options):
        placement = Exercise.objects.filter(catalog_role="placement", publication_status="published").count()
        if placement != 15:
            raise CommandError(f"placement bank has {placement} published items, expected 15")
        if Exercise.objects.filter(catalog_role="placement", active=True).exists():
            raise CommandError("a placement item is in the practice queue")
        missing = []
        for level in LEVELS:
            for skill in SKILLS:
                ready = Exercise.objects.filter(
                    level=level,
                    skill=skill,
                    publication_status="published",
                    catalog_role="practice",
                    active=True,
                ).exclude(quality_status="legacy")
                if not ready.exists():
                    missing.append(f"L{level}{skill}")
        if missing:
            raise CommandError("reviewed cells missing: " + ", ".join(missing))
        self.stdout.write(self.style.SUCCESS("Smoke passed."))
