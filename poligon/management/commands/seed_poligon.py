import json
from datetime import date, datetime
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import connection

from poligon.models import ChoiceOption, Exercise, Review, Submission, VocabularyItem

DATA_ROOT = Path(__file__).resolve().parents[2] / "data"
# The live queue is an explicit list, not "the first rows by id". A fresh seed
# used to switch on whatever was inserted first, which put template drills
# ahead of the items worth practising.
ACTIVE_SLUGS_PATH = DATA_ROOT / "active_slugs.json"
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
    "publication_status",
}
# Columns added after the first catalog seed. Migration 0006 calls this command
# before those columns exist, so they are omitted until the table has them.
STATUS_FIELDS = {
    "publication_status",
    "quality_status",
    "scenario",
    "subskill",
    "learning_objective",
    "competency",
    "success_criteria",
    "review_status",
    "reviewed_by",
    "reviewed_at",
    "source_type",
    "catalog_role",
}
PLACEMENT_PATH = DATA_ROOT / "placement" / "v1.json"


class Command(BaseCommand):
    help = "Load original Poligon exercises and vocabulary, including attributed Wiktionary cards."

    def add_arguments(self, parser):
        parser.add_argument("--exercises-only", action="store_true")
        parser.add_argument("--vocabulary-only", action="store_true")
        parser.add_argument(
            "--full-catalog",
            action="store_true",
            help="Leave every practice exercise active instead of the published set.",
        )
        parser.add_argument(
            "--placement-only",
            action="store_true",
            help="Load the placement bank and leave the practice catalog untouched.",
        )

    def handle(self, *args, **options):
        exercise_columns = _columns(Exercise)
        self._exercise_columns = exercise_columns
        self._exercise_ready = "publication_status" in exercise_columns
        self._catalog_ready = "catalog_role" in exercise_columns
        self._vocab_ready = "publication_status" in _columns(VocabularyItem)
        if options["placement_only"]:
            self._load_placement()
            self._set_active_pool(full_catalog=False)
            self.stdout.write(self.style.SUCCESS("Placement bank loaded."))
            return
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
            loaded_slugs.update(self._load_placement())
        if not exercises_only:
            for relative in manifest["vocabulary"]:
                self.stdout.write(f"vocabulary {relative}")
                loaded_terms.update(self._load_vocabulary(DATA_ROOT / relative))
        if not vocabulary_only:
            self._set_active_pool(full_catalog=options["full_catalog"])
            self._retire_exercises(loaded_slugs)
        if not exercises_only:
            self._retire_vocabulary(loaded_terms)
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
            raw.pop("active", None)
            retrieved = raw.get("retrieved_at")
            if retrieved:
                raw["retrieved_at"] = date.fromisoformat(retrieved)
            reviewed = raw.get("reviewed_at")
            if reviewed:
                raw["reviewed_at"] = datetime.fromisoformat(reviewed)
            allowed = ({field.name for field in Exercise._meta.fields} - {"id"}) & self._exercise_columns
            if not self._exercise_ready:
                allowed -= STATUS_FIELDS
            raw = {key: value for key, value in raw.items() if key in allowed}
            exercise, _created = Exercise.objects.update_or_create(slug=slug, defaults=raw)
            exercise.options.all().delete()
            for index, option in enumerate(options):
                ChoiceOption.objects.create(exercise=exercise, sort_order=index, **option)
            loaded.add(slug)
        return loaded

    def _load_placement(self) -> set[str]:
        if not self._catalog_ready or not PLACEMENT_PATH.exists():
            return set()
        self.stdout.write("placement bank")
        return self._load_exercises(PLACEMENT_PATH)

    def _set_active_pool(self, *, full_catalog: bool) -> None:
        """``active`` follows publication. The allowlist remains only for old databases."""
        if full_catalog:
            pool = Exercise.objects.all()
            if self._catalog_ready:
                pool = pool.filter(catalog_role="practice")
            pool.update(active=True)
            if self._catalog_ready:
                Exercise.objects.filter(catalog_role="placement").update(active=False)
            return
        if not self._exercise_ready:
            keep = set(json.loads(ACTIVE_SLUGS_PATH.read_text(encoding="utf-8")))
            Exercise.objects.exclude(slug__in=keep).update(active=False)
            Exercise.objects.filter(slug__in=keep).update(active=True)
            return
        published = Exercise.objects.filter(publication_status="published")
        if self._catalog_ready:
            published = published.filter(catalog_role="practice")
        published.update(active=True)
        Exercise.objects.exclude(pk__in=published.values("pk")).update(active=False)

    def _retire_exercises(self, loaded_slugs: set[str]) -> None:
        """A missing slug with history is deprecated. It is not deleted."""
        missing = Exercise.objects.exclude(slug__in=loaded_slugs)
        if not self._exercise_ready:
            removed = missing.delete()[0]
            if removed:
                self.stdout.write(f"removed {removed} orphan exercises")
            return
        kept = list(
            missing.filter(pk__in=Submission.objects.values("exercise_id")).values_list("pk", flat=True)
        )
        if kept:
            Exercise.objects.filter(pk__in=kept).update(publication_status="deprecated", active=False)
            self.stdout.write(f"deprecated {len(kept)} exercises that still have answers")
        removed = missing.exclude(pk__in=kept).delete()[0]
        if removed:
            self.stdout.write(f"removed {removed} orphan exercises")

    def _retire_vocabulary(self, loaded_terms: set[str]) -> None:
        missing = VocabularyItem.objects.exclude(term__in=loaded_terms)
        if not self._vocab_ready:
            removed = missing.delete()[0]
            if removed:
                self.stdout.write(f"removed {removed} orphan vocabulary items")
            return
        kept = list(missing.filter(pk__in=Review.objects.values("item_id")).values_list("pk", flat=True))
        if kept:
            VocabularyItem.objects.filter(pk__in=kept).update(publication_status="deprecated", active=False)
            self.stdout.write(f"deprecated {len(kept)} vocabulary items that still have reviews")
        removed = missing.exclude(pk__in=kept).delete()[0]
        if removed:
            self.stdout.write(f"removed {removed} orphan vocabulary items")

    def _load_vocabulary(self, path: Path) -> set[str]:
        loaded: set[str] = set()
        for raw in json.loads(path.read_text(encoding="utf-8")):
            term = raw.pop("term")
            retrieved = raw.get("retrieved_at")
            if retrieved:
                raw["retrieved_at"] = date.fromisoformat(retrieved)
            defaults = {key: raw[key] for key in VOCAB_FIELDS if key in raw}
            if not self._vocab_ready:
                defaults.pop("publication_status", None)
            elif defaults.get("publication_status") == "published":
                defaults["active"] = True
            elif "publication_status" in defaults:
                defaults["active"] = False
            VocabularyItem.objects.update_or_create(term=term, defaults=defaults)
            loaded.add(term)
        return loaded


def _columns(model) -> set[str]:
    with connection.cursor() as cursor:
        description = connection.introspection.get_table_description(cursor, model._meta.db_table)
    return {column.name for column in description}
