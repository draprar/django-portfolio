import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils import timezone

from poligon.content_validation import validate_catalog
from poligon.models import Exercise, Review, Submission
from poligon.tests.factories import make_exercise, make_learner, make_vocabulary


def test_every_skill_cell_has_one_reviewed_exercise():
    report = validate_catalog()
    assert report.errors == []
    assert report.counts[3]["S"] == 1
    assert report.counts[3]["W"] == 1
    assert report.counts[4]["S"] == 1
    assert report.counts[4]["W"] == 1
    assert report.counts[2]["L"] == 6
    assert report.strict_counts[3]["S"] == 1
    assert report.coverage(3) == 100
    text = report.text()
    assert "reviewed cells at 1: 20/20" in text
    assert "reviewed cells at 8: 0/20" in text
    assert "reviewed cells at 20: 0/20" in text


def test_strict_validation_rejects_legacy_gaps():
    with pytest.raises(CommandError):
        call_command("validate_poligon_content", "--strict")


def test_the_default_validator_passes():
    call_command("validate_poligon_content")


@pytest.mark.django_db
def test_publication_migration_marks_the_previous_queue():
    import importlib

    from django.apps import apps

    migration = importlib.import_module("poligon.migrations.0010_content_publication")
    make_exercise(slug="listen-001-schedule-change")
    make_exercise(slug="not-on-the-list")
    migration.mark_the_live_queue(apps, None)

    live = Exercise.objects.get(slug="listen-001-schedule-change")
    draft = Exercise.objects.get(slug="not-on-the-list")
    assert live.publication_status == "published"
    assert live.quality_status == "legacy"
    assert live.active is True
    assert draft.publication_status == "draft"
    assert draft.active is False


@pytest.mark.django_db
def test_seed_keeps_an_exercise_that_already_has_an_answer():
    call_command("seed_poligon", "--exercises-only")
    learner = make_learner()
    kept = make_exercise(slug="orphan-kept", publication_status="published", active=True)
    Submission.objects.create(learner=learner, exercise=kept, score=10)
    make_exercise(slug="orphan-gone", publication_status="draft", active=False)

    call_command("seed_poligon", "--exercises-only")

    kept.refresh_from_db()
    assert kept.publication_status == "deprecated"
    assert kept.active is False
    assert Submission.objects.filter(exercise=kept).count() == 1
    assert not Exercise.objects.filter(slug="orphan-gone").exists()


@pytest.mark.django_db
def test_seed_keeps_a_vocabulary_card_that_already_has_a_review():
    call_command("seed_poligon", "--vocabulary-only")
    learner = make_learner()
    card = make_vocabulary(term="orphan-card")
    Review.objects.create(learner=learner, item=card, due_at=timezone.now())

    call_command("seed_poligon", "--vocabulary-only")

    card.refresh_from_db()
    assert card.publication_status == "deprecated"
    assert card.active is False
    assert Review.objects.filter(item=card).count() == 1
