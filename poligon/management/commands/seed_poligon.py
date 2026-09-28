import json
from datetime import date
from pathlib import Path

from django.core.management.base import BaseCommand

from poligon.models import ChoiceOption, Exercise, VocabularyItem

DATA_ROOT = Path(__file__).resolve().parents[2] / "data"
# A short, solid pool beats a long one nobody finishes. The rest of the
# catalog stays in the database, only switched off, so widening it is a flag.
ACTIVE_PER_LEVEL_SKILL = 5
VOCAB_FIELDS = {
    "translation",
    "explanation_pl",
    "explanation_en",
    "example_pl",
    "example_en",
    "category_pl",
    "category_en",
    "level",
    "content_source",
    "source_url",
    "source_license",
    "retrieved_at",
    "attribution_en",
    "attribution_pl",
}


class Command(BaseCommand):
    help = "Load original Poligon exercises and vocabulary, including attributed Wiktionary cards."

    def add_arguments(self, parser):
        parser.add_argument("--exercises-only", action="store_true")
        parser.add_argument("--vocabulary-only", action="store_true")
        parser.add_argument(
            "--full-catalog",
            action="store_true",
            help=f"Leave every exercise active instead of {ACTIVE_PER_LEVEL_SKILL} per level and skill.",
        )

    def handle(self, *args, **options):
        manifest = json.loads((DATA_ROOT / "manifest.json").read_text(encoding="utf-8"))
        exercises_only = options["exercises_only"]
        vocabulary_only = options["vocabulary_only"]
        if exercises_only and vocabulary_only:
            self.stderr.write("Choose one of --exercises-only or --vocabulary-only.")
            return
        loaded_slugs: set[str] = set()
        loaded_terms: set[str] = set()
        if not vocabulary_only:
            for relative in manifest["exercises"]:
                self.stdout.write(f"exercises {relative}")
                loaded_slugs.update(self._load_exercises(DATA_ROOT / relative))
        if not exercises_only:
            for relative in manifest["vocabulary"]:
                self.stdout.write(f"vocabulary {relative}")
                loaded_terms.update(self._load_vocabulary(DATA_ROOT / relative))
        if not vocabulary_only:
            self._set_active_pool(full_catalog=options["full_catalog"])
            removed = Exercise.objects.exclude(slug__in=loaded_slugs).delete()[0]
            if removed:
                self.stdout.write(f"removed {removed} orphan exercises")
        if not exercises_only:
            removed = VocabularyItem.objects.exclude(term__in=loaded_terms).delete()[0]
            if removed:
                self.stdout.write(f"removed {removed} orphan vocabulary items")
        counts = {skill: Exercise.objects.filter(skill=skill).count() for skill in ("L", "S", "R", "W")}
        wiki = VocabularyItem.objects.filter(content_source="wiktionary").count()
        self.stdout.write(
            self.style.SUCCESS(
                "Seeded "
                f"{Exercise.objects.count()} exercises "
                f"(L{counts['L']} S{counts['S']} R{counts['R']} W{counts['W']}, "
                f"{Exercise.objects.filter(active=True).count()} active) and "
                f"{VocabularyItem.objects.count()} vocabulary items ({wiki} from Wiktionary)."
            )
        )

    def _load_exercises(self, path: Path) -> set[str]:
        loaded: set[str] = set()
        for raw in json.loads(path.read_text(encoding="utf-8")):
            options = raw.pop("options", [])
            slug = raw.pop("slug")
            retrieved = raw.get("retrieved_at")
            if retrieved:
                raw["retrieved_at"] = date.fromisoformat(retrieved)
            exercise, _created = Exercise.objects.update_or_create(slug=slug, defaults=raw)
            exercise.options.all().delete()
            for index, option in enumerate(options):
                ChoiceOption.objects.create(exercise=exercise, sort_order=index, **option)
            loaded.add(slug)
        return loaded

    def _set_active_pool(self, *, full_catalog: bool) -> None:
        """Keep the first few items of every level and skill switched on."""
        if full_catalog:
            Exercise.objects.update(active=True)
            return
        keep: list[int] = []
        # order_by() drops the model ordering, or DISTINCT would see every row.
        for level, skill in Exercise.objects.order_by().values_list("level", "skill").distinct():
            keep += list(
                Exercise.objects.filter(level=level, skill=skill)
                .order_by("id")
                .values_list("id", flat=True)[:ACTIVE_PER_LEVEL_SKILL]
            )
        Exercise.objects.exclude(id__in=keep).update(active=False)
        Exercise.objects.filter(id__in=keep).update(active=True)

    def _load_vocabulary(self, path: Path) -> set[str]:
        loaded: set[str] = set()
        for raw in json.loads(path.read_text(encoding="utf-8")):
            term = raw.pop("term")
            retrieved = raw.get("retrieved_at")
            if retrieved:
                raw["retrieved_at"] = date.fromisoformat(retrieved)
            defaults = {key: raw[key] for key in VOCAB_FIELDS if key in raw}
            VocabularyItem.objects.update_or_create(term=term, defaults=defaults)
            loaded.add(term)
        return loaded
