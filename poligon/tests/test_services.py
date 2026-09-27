from datetime import timedelta

import pytest
from django.utils import timezone

from poligon.models import Review, Submission
from poligon.services import schedule_review, skill_scores
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
