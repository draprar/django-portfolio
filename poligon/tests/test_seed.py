import json
from pathlib import Path

import pytest
from django.core.management import call_command

from poligon.models import Exercise, Submission, VocabularyItem
from poligon.tests.factories import make_learner

EXPECTED_EXERCISE_LEVELS = {1: 73, 2: 87, 3: 40, 4: 25, 5: 27}
EXPECTED_EXERCISE_COUNT = 252
EXPECTED_VOCAB_LEVELS = {1: 388, 2: 188, 3: 199, 4: 199, 5: 199}


@pytest.mark.django_db
def test_seed_poligon_is_bilingual_and_safe_to_repeat():
    call_command("seed_poligon")
    assert Exercise.objects.count() == EXPECTED_EXERCISE_COUNT
    assert VocabularyItem.objects.count() == 1173
    assert Exercise.objects.filter(skill="L").count() == 61
    for level, count in EXPECTED_EXERCISE_LEVELS.items():
        assert Exercise.objects.filter(level=level).count() == count
    for level, count in EXPECTED_VOCAB_LEVELS.items():
        assert VocabularyItem.objects.filter(level=level).count() == count
    assert Exercise.objects.filter(level=0).count() == 0
    assert VocabularyItem.objects.filter(level=0).count() == 0
    assert Exercise.objects.filter(level=0, content_source="wikipedia").count() == 0
    assert Exercise.objects.filter(content_source="wikipedia").count() == 21
    from poligon.content_validation import load_exercises

    published = {item["slug"] for item in load_exercises() if item.get("publication_status") == "published"}
    legacy = {
        item["slug"]
        for item in load_exercises()
        if item.get("publication_status") == "published" and item.get("quality_status") == "legacy"
    }
    active = set(Exercise.objects.filter(active=True).values_list("slug", flat=True))
    assert active == published
    assert Exercise.objects.filter(publication_status="published", quality_status="legacy").count() == len(legacy)
    assert len(published - legacy) == 20
    for item in Exercise.objects.filter(active=True, exercise_type__in=("mcq", "listening")):
        options = list(item.options.all())
        assert len(options) == 4, item.slug
        assert sum(option.is_correct for option in options) == 1, item.slug
        assert all(option.text_en.strip() for option in options), item.slug
        assert not all(option.text_en.startswith("It is about") for option in options), item.slug
    assert not Exercise.objects.exclude(content_source="original").filter(attribution_en="").exists()
    assert not VocabularyItem.objects.exclude(content_source="original").filter(attribution_en="").exists()
    assert not VocabularyItem.objects.filter(content_source="wiktionary", attribution_en="").exists()
    assert VocabularyItem.objects.filter(content_source="wiktionary").count() >= 97

    exercise = Exercise.objects.get(slug="read-001-route")
    assert exercise.title_pl
    assert exercise.title_en
    assert exercise.prompt_pl != exercise.prompt_en
    assert exercise.options.count() == 4
    assert exercise.options.filter(text_pl="", text_en="").count() == 0
    item = VocabularyItem.objects.get(term="briefing")
    assert item.explanation_pl
    assert item.example_en

    learner = make_learner()
    Submission.objects.create(learner=learner, exercise=exercise, score=10)
    call_command("seed_poligon")
    assert Exercise.objects.count() == EXPECTED_EXERCISE_COUNT
    assert VocabularyItem.objects.count() == 1173
    assert Exercise.objects.filter(skill="L").count() == 61
    assert Exercise.objects.filter(content_source="wikipedia").count() == 21
    assert not Exercise.objects.exclude(content_source="original").filter(attribution_en="").exists()
    assert not VocabularyItem.objects.filter(content_source="wiktionary", attribution_en="").exists()
    assert Submission.objects.filter(learner=learner, exercise__slug="read-001-route").count() == 1


def test_catalog_migration_does_not_seed_the_test_database(monkeypatch):
    import importlib

    migration = importlib.import_module("poligon.migrations.0006_seed_catalog")
    called = []
    monkeypatch.setattr(
        "django.core.management.call_command",
        lambda *args, **kwargs: called.append(args),
    )
    migration.seed_catalog(None, None)
    assert called == []


def test_catalog_migration_seeds_when_migrate_runs_against_the_app_database(monkeypatch):
    import importlib
    import sys

    from django.conf import settings

    migration = importlib.import_module("poligon.migrations.0006_seed_catalog")
    monkeypatch.setattr(sys, "argv", ["manage.py", "migrate", "--noinput"])
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    monkeypatch.delenv("DJANGO_TESTING", raising=False)
    monkeypatch.setitem(settings.DATABASES["default"], "NAME", "postgres")
    called = []
    monkeypatch.setattr(
        "django.core.management.call_command",
        lambda *args, **kwargs: called.append(args),
    )
    migration.seed_catalog(None, None)
    assert called == [("seed_poligon",)]


OLD_WIKI_TRIO = {
    "It is about a spare tyre.",
    "It is about a radio call sign.",
    "It is about a night shift roster.",
}


def test_wikipedia_items_do_not_share_one_distractor_trio():
    data = Path(__file__).resolve().parents[1] / "data"
    triples = []
    for path in (data / "exercises").glob("*.json"):
        for row in json.loads(path.read_text(encoding="utf-8")):
            prompt = row.get("prompt_en") or ""
            assert not prompt.endswith("…"), row.get("slug")
            wrongs = tuple(
                sorted(option["text_en"] for option in row.get("options") or [] if not option.get("is_correct"))
            )
            assert not OLD_WIKI_TRIO <= set(wrongs), row.get("slug")
            if row.get("content_source") == "wikipedia" and len(wrongs) == 3:
                triples.append(wrongs)
    assert triples
    assert len(triples) == len(set(triples))

    for path in (data / "vocabulary").glob("*.json"):
        for row in json.loads(path.read_text(encoding="utf-8")):
            explanation = row.get("explanation_pl") or ""
            assert not explanation.startswith("W tym zestawie:"), row.get("term")
