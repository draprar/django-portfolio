from datetime import timedelta

import pytest
from django.utils import timezone

from poligon.models import Review, StudyEvent, Submission
from poligon.services import VOCABULARY_SKILL, next_vocabulary_card, schedule_review, skill_scores
from poligon.tests.factories import make_exercise, make_learner, make_vocabulary


@pytest.mark.django_db
def test_schedule_again_resets_the_card():
    review = Review.objects.create(
        learner=make_learner(),
        item=make_vocabulary(),
        due_at=timezone.now(),
        ease=1.3,
    )
    schedule_review(review, 0)
    assert review.repetitions == 0
    assert review.interval_days == 0
    assert review.ease == 1.3
    assert review.last_grade == 0
    assert review.due_at <= timezone.now() + timedelta(minutes=21)


@pytest.mark.django_db
def test_schedule_good_grades_grow_the_interval():
    review = Review.objects.create(
        learner=make_learner(), item=make_vocabulary(term="route"), due_at=timezone.now()
    )
    schedule_review(review, 4)
    assert review.repetitions == 1
    assert review.interval_days == 1
    schedule_review(review, 3)
    assert review.repetitions == 2
    assert review.interval_days == 3
    assert review.ease == 2.6
    schedule_review(review, 5)
    assert review.repetitions == 3
    assert review.interval_days >= 3
    assert review.ease == 2.7


@pytest.mark.django_db
def test_new_cards_follow_catalog_order_not_the_alphabet():
    learner = make_learner(practice_level=2)
    first_created = make_vocabulary(term="zebra", level=2)
    make_vocabulary(term="alpha", level=2)
    chosen, added = next_vocabulary_card(learner, 2, introductions_left=12)
    assert added == 1
    assert chosen.item_id == first_created.pk
    assert chosen.item.term == "zebra"


@pytest.mark.django_db
def test_a_due_weak_card_comes_before_a_due_strong_card():
    learner = make_learner(practice_level=2)
    strong = Review.objects.create(
        learner=learner,
        item=make_vocabulary(term="strong-card", level=2),
        due_at=timezone.now() - timedelta(minutes=5),
        last_grade=5,
        repetitions=2,
    )
    weak = Review.objects.create(
        learner=learner,
        item=make_vocabulary(term="weak-card", level=2),
        due_at=timezone.now() - timedelta(minutes=1),
        last_grade=1,
        repetitions=1,
    )
    chosen, added = next_vocabulary_card(learner, 2, introductions_left=12)
    assert added == 0
    assert chosen.pk == weak.pk
    assert chosen.pk != strong.pk


@pytest.mark.django_db
def test_the_session_limit_stops_new_cards():
    learner = make_learner(practice_level=2)
    make_vocabulary(term="one-more", level=2)
    chosen, added = next_vocabulary_card(learner, 2, introductions_left=0)
    assert chosen is None
    assert added == 0


@pytest.mark.django_db
def test_a_vocabulary_event_is_not_a_reading_score():
    exercise = make_exercise(skill="R")
    learner = make_learner()
    Submission.objects.create(learner=learner, exercise=exercise, score=80)
    StudyEvent.objects.create(learner=learner, skill=VOCABULARY_SKILL, minutes=2, note="Vocabulary review")
    assert skill_scores(Submission.objects.select_related("exercise"))["R"] == 80
    assert "V" not in skill_scores(Submission.objects.select_related("exercise"))


@pytest.mark.django_db
def test_skill_scores_average_known_skills_only():
    exercise = make_exercise()
    learner = make_learner()
    Submission.objects.create(learner=learner, exercise=exercise, score=40)
    Submission.objects.create(learner=learner, exercise=exercise, score=60)
    Submission.objects.create(learner=learner, exercise=exercise, score=None)
    scores = skill_scores(Submission.objects.select_related("exercise"))
    assert scores == {"L": 0, "S": 0, "R": 50, "W": 0}
    assert str(exercise) == "Demo"
    assert str(Submission.objects.filter(score=40).get()).startswith(f"{learner.pk} /")
