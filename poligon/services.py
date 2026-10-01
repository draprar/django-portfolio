"""Review scheduling (srs_v1) and skill averages for Ćwiczba.

srs_v1 is the schedule in this file. A grade below 3 is due again in 20 minutes.
A passing grade waits 1 day, then 3 days, then the current interval times ease.
Ease moves by tenths and stays between 1.3 and 3.0. This is not textbook SM-2:
there is no EF formula and the second success is 3 days, not 6.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import timedelta

from django.db.models import Case, IntegerField, Value, When
from django.utils import timezone

from .framework import SRS_VERSION
from .models import LearnerState, Review, VocabularyItem

SKILLS = ("L", "S", "R", "W")
VOCABULARY_SKILL = "V"
NEW_CARDS_PER_SESSION = 12


def due_review_count(state: LearnerState) -> int:
    """Cards waiting right now on the learner's own practice level."""
    return Review.objects.filter(
        learner=state,
        due_at__lte=timezone.now(),
        item__level=state.practice_level,
    ).count()


def schedule_review(review: Review, grade: int) -> Review:
    """Apply one srs_v1 step. Grades below 3 reset the card to a short delay."""
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


def next_vocabulary_card(state: LearnerState, level: int, introductions_left: int) -> tuple[Review | None, int]:
    """The next card: due (weak first), otherwise a new card, up to the session limit.

    New cards are taken in catalog order (id), not A–Z. ``introductions_left`` is
    how many new cards this visit may still add. The return is the card and how
    many new cards were just created (0 or 1).
    """
    due = (
        Review.objects.filter(learner=state, due_at__lte=timezone.now(), item__level=level, item__active=True)
        .select_related("item")
        .annotate(
            weak_first=Case(
                When(last_grade__lt=3, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        )
        .order_by("weak_first", "due_at", "id")
        .first()
    )
    if due is not None:
        return due, 0
    if introductions_left <= 0:
        return None, 0
    seen = Review.objects.filter(learner=state).values("item_id")
    item = (
        VocabularyItem.objects.filter(active=True, level=level, publication_status="published")
        .exclude(pk__in=seen)
        .order_by("id")
        .first()
    )
    if item is None:
        return None, 0
    review = Review.objects.create(learner=state, item=item, due_at=timezone.now())
    return review, 1


# Re-exported so callers can record which schedule produced a card.
__all__ = [
    "NEW_CARDS_PER_SESSION",
    "SRS_VERSION",
    "VOCABULARY_SKILL",
    "due_review_count",
    "next_vocabulary_card",
    "schedule_review",
    "skill_scores",
]
