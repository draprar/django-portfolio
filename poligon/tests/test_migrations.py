import importlib

import pytest


def _migration(module_name: str):
    return importlib.import_module(f"poligon.migrations.{module_name}").Migration


def test_identity_migration_does_not_share_a_transaction_with_alters():
    """DML then ALTER on poligon_learnerstate fails on PostgreSQL if atomic."""
    assert _migration("0004_learner_identity").atomic is False


def test_account_migration_does_not_share_a_transaction_with_alters():
    """Deleting guest rows then dropping guest_token hits the same PostgreSQL error."""
    assert _migration("0007_learner_state_needs_an_account").atomic is False


def test_five_level_migration_does_not_share_a_transaction_with_alters():
    """Lifting level 0 and then adding the check hits the same PostgreSQL error."""
    assert _migration("0009_five_levels").atomic is False


@pytest.mark.django_db(transaction=True)
def test_level_zero_rows_move_to_level_one_and_history_stays():
    """The lift runs against rows the check would otherwise refuse to store."""
    import importlib

    from django.apps import apps
    from django.db import connection

    from poligon.models import Exercise, LearnerState, Submission, VocabularyItem
    from poligon.tests.factories import make_exercise, make_learner, make_vocabulary

    lift_level_zero = importlib.import_module("poligon.migrations.0009_five_levels").lift_level_zero

    if connection.vendor != "sqlite":
        pytest.skip("this check uses the SQLite session pragma")

    with connection.cursor() as cursor:
        cursor.execute("PRAGMA ignore_check_constraints = ON")
    try:
        learner = make_learner(practice_level=0, target_profile="0000")
        other = make_learner(practice_level=2, target_profile="2020")
        exercise = make_exercise(slug="old-floor", level=0)
        kept = make_exercise(slug="listen-001-schedule-change", level=2, active=False)
        card = make_vocabulary(term="old-floor-word", level=0)
        Submission.objects.create(learner=learner, exercise=exercise, score=1)
        lift_level_zero(apps, None)
        learner.refresh_from_db()
        other.refresh_from_db()
        exercise.refresh_from_db()
        kept.refresh_from_db()
        card.refresh_from_db()
        assert learner.practice_level == 1
        assert learner.target_profile == "1111"
        assert other.practice_level == 2
        assert other.target_profile == "2121"
        assert exercise.level == 1
        assert exercise.active is False
        assert card.level == 1
        assert kept.active is True
        assert Submission.objects.filter(learner=learner, exercise=exercise).count() == 1
        assert LearnerState.objects.filter(practice_level=0).count() == 0
        assert Exercise.objects.filter(level=0).count() == 0
        assert VocabularyItem.objects.filter(level=0).count() == 0
    finally:
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA ignore_check_constraints = OFF")
