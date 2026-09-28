import pytest
from django.core.management import call_command

from poligon.models import Exercise, Submission, VocabularyItem
from poligon.tests.factories import make_learner

EXPECTED_EXERCISE_LEVELS = {0: 32, 1: 30, 2: 80, 3: 31, 4: 16, 5: 16}
EXPECTED_VOCAB_LEVELS = {0: 197, 1: 191, 2: 188, 3: 199, 4: 199, 5: 199}


@pytest.mark.django_db
def test_seed_poligon_is_bilingual_and_safe_to_repeat():
    call_command("seed_poligon")
    assert Exercise.objects.count() == 205
    assert VocabularyItem.objects.count() == 1173
    assert Exercise.objects.filter(skill="L").count() == 52
    for level, count in EXPECTED_EXERCISE_LEVELS.items():
        assert Exercise.objects.filter(level=level).count() == count
    for level, count in EXPECTED_VOCAB_LEVELS.items():
        assert VocabularyItem.objects.filter(level=level).count() == count
    assert Exercise.objects.filter(level=0, content_source="wikipedia").count() == 0
    assert Exercise.objects.filter(content_source="wikipedia").count() == 21
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
    assert Exercise.objects.count() == 205
    assert VocabularyItem.objects.count() == 1173
    assert Exercise.objects.filter(skill="L").count() == 52
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
