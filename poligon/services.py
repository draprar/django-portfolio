"""Spaced-repetition scheduling (SM-2) and skill averages for Poligon."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import timedelta

from django.utils import timezone

from .models import LearnerState, Review

SKILLS = ("L", "S", "R", "W")


def due_review_count(state: LearnerState) -> int:
    """Cards waiting right now on the learner's own practice level."""
    return Review.objects.filter(
        learner=state,
        due_at__lte=timezone.now(),
        item__level=state.practice_level,
    ).count()


def schedule_review(review: Review, grade: int) -> Review:
    """Apply one SM-2 step. Grades below 3 reset the card to a short delay."""
    grade = max(0, min(5, int(grade)))
    now = timezone.now()
    if grade < 3:
        review.repetitions = 0
        review.interval_days = 0
        review.ease = max(1.3, review.ease - 0.2)
        review.due_at = now + timedelta(minutes=20)
    else:
        review.repetitions += 1
        if review.repetitions == 1:
            review.interval_days = 1
        elif review.repetitions == 2:
            review.interval_days = 3
        else:
            review.interval_days = max(1, round(review.interval_days * review.ease))
        review.ease = min(3.0, review.ease + (0.1 if grade >= 4 else 0))
        review.due_at = now + timedelta(days=review.interval_days)
    review.last_grade = grade
    review.save(
        update_fields=["repetitions", "interval_days", "ease", "due_at", "last_grade", "updated_at"],
    )
    return review


def skill_scores(submissions: Iterable) -> dict[str, int]:
    buckets: dict[str, list[float]] = {skill: [] for skill in SKILLS}
    for item in submissions:
        skill = item.exercise.skill
        if item.score is not None and skill in buckets:
            buckets[skill].append(item.score)
    return {skill: round((sum(values) / len(values)) if values else 0) for skill, values in buckets.items()}
