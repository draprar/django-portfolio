import json
from datetime import date
from pathlib import Path

from django.core.management.base import BaseCommand

from poligon.models import ChoiceOption, Exercise, VocabularyItem

DATA_ROOT = Path(__file__).resolve().parents[2] / "data"
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

    def handle(self, *args, **options):
        manifest = json.loads((DATA_ROOT / "manifest.json").read_text(encoding="utf-8"))
        exercises_only = options["exercises_only"]
        vocabulary_only = options["vocabulary_only"]
        if exercises_only and vocabulary_only:
            self.stderr.write("Choose one of --exercises-only or --vocabulary-only.")
            return
        if not vocabulary_only:
            for relative in manifest["exercises"]:
                self.stdout.write(f"exercises {relative}")
                self._load_exercises(DATA_ROOT / relative)
        if not exercises_only:
            for relative in manifest["vocabulary"]:
                self.stdout.write(f"vocabulary {relative}")
                self._load_vocabulary(DATA_ROOT / relative)
        counts = {skill: Exercise.objects.filter(skill=skill).count() for skill in ("L", "S", "R", "W")}
        wiki = VocabularyItem.objects.filter(content_source="wiktionary").count()
        self.stdout.write(
            self.style.SUCCESS(
                "Seeded "
                f"{Exercise.objects.count()} exercises "
                f"(L{counts['L']} S{counts['S']} R{counts['R']} W{counts['W']}) and "
                f"{VocabularyItem.objects.count()} vocabulary items ({wiki} from Wiktionary)."
            )
        )

    def _load_exercises(self, path: Path) -> None:
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

    def _load_vocabulary(self, path: Path) -> None:
        for raw in json.loads(path.read_text(encoding="utf-8")):
            term = raw.pop("term")
            retrieved = raw.get("retrieved_at")
            if retrieved:
                raw["retrieved_at"] = date.fromisoformat(retrieved)
            defaults = {key: raw[key] for key in VOCAB_FIELDS if key in raw}
            VocabularyItem.objects.update_or_create(term=term, defaults=defaults)
