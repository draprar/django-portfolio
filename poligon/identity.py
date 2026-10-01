"""Who is practising right now.

Practice never needs an account and never leaves anything behind. A guest keeps
the chosen level in the Django session, which lasts as long as the visit, and
nothing about that guest reaches the database. An account exists so the level,
the history and the flashcard schedule survive the visit.
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass
from datetime import date

from django.http import HttpRequest

from .models import LearnerState

LEVEL_KEY = "poligon_level"
SEEN_KEY = "poligon_seen"
ATTEMPT_KEY = "poligon_attempt"
ACCOUNT_HINT_KEY = "poligon_account_hint"
SHUFFLE_KEY = "poligon_shuffle"

MIN_LEVEL = 1
MAX_LEVEL = 5
DEFAULT_DAILY_MINUTES = 35
# Enough to cover one level and skill without letting the session cookie grow.
SEEN_LIMIT = 40


@dataclass(frozen=True)
class GuestPlan:
    """What a guest has for the length of one visit. Never saved."""

    practice_level: int
    daily_minutes: int = DEFAULT_DAILY_MINUTES
    target_date: date | None = None

    @property
    def target_profile(self) -> str:
        return str(self.practice_level) * 4


def account_state(request: HttpRequest) -> LearnerState | None:
    """The row to read and write. ``None`` for everyone without an account."""
    if not request.user.is_authenticated:
        return None
    state, _created = LearnerState.objects.get_or_create(user=request.user)
    return state


def guest_level(request: HttpRequest) -> int | None:
    raw = request.session.get(LEVEL_KEY)
    # A visit that still has the old floor (level 0) continues at level 1.
    # Clearing the seen list here is what set_guest_level does on any change.
    if raw == 0:
        set_guest_level(request, MIN_LEVEL)
        return MIN_LEVEL
    if isinstance(raw, int) and MIN_LEVEL <= raw <= MAX_LEVEL:
        return raw
    return None


def set_guest_level(request: HttpRequest, level: int) -> None:
    request.session[LEVEL_KEY] = int(level)
    # A new level means a new pool. The previous result is not the current one.
    request.session.pop(SEEN_KEY, None)
    request.session.pop(ATTEMPT_KEY, None)


def current_plan(request: HttpRequest) -> LearnerState | GuestPlan | None:
    """Level and goals to read from. ``None`` when a guest has not chosen yet."""
    state = account_state(request)
    if state is not None:
        return state
    level = guest_level(request)
    if level is None:
        return None
    return GuestPlan(practice_level=level)


def adopt_guest_level(request: HttpRequest, account: LearnerState) -> bool:
    """Copy a guest visit onto an account that has no history yet.

    The copy is the level, the finished slugs, and the last result. Placement
    stays on the account because a guest cannot take it. Returns True only when
    the level itself changed, which is what the confirmation message talks about.
    """
    level = guest_level(request)
    seen = list(seen_slugs(request))
    attempt = request.session.get(ATTEMPT_KEY)
    request.session.pop(LEVEL_KEY, None)
    request.session.pop(SEEN_KEY, None)
    request.session.pop(ATTEMPT_KEY, None)
    fresh = not account.submissions.exists() and not account.reviews.exists()
    if fresh:
        _import_guest_slugs(account, seen, attempt if isinstance(attempt, dict) else None)
    if not fresh or level is None or account.practice_level == level:
        return False
    account.practice_level = level
    account.target_profile = str(level) * 4
    account.save(update_fields=["practice_level", "target_profile", "updated_at"])
    return True


def _import_guest_slugs(account: LearnerState, slugs: list[str], attempt: dict | None) -> None:
    """Mark the guest's finished exercises as done so the queue does not repeat them."""
    from .models import Exercise, Submission

    attempt = attempt or {}
    for slug in slugs:
        exercise = Exercise.objects.filter(slug=slug).first()
        if exercise is None or Submission.objects.filter(learner=account, exercise=exercise).exists():
            continue
        feedback: dict = {"imported_from_guest": True}
        answer = ""
        score = None
        selected_id = None
        if attempt.get("exercise_id") == exercise.pk:
            raw = attempt.get("feedback")
            if isinstance(raw, dict):
                feedback = {**raw, "imported_from_guest": True}
            answer = str(attempt.get("answer") or "")
            if attempt.get("score") is not None:
                score = float(attempt["score"])
            selected_id = attempt.get("selected_option_id")
        Submission.objects.create(
            learner=account,
            exercise=exercise,
            answer_text=answer,
            selected_option_id=selected_id,
            score=score,
            feedback=feedback,
        )


def shuffle_seed(request: HttpRequest) -> str:
    """A salt for the answer order, so a reload does not reshuffle the choices."""
    if request.user.is_authenticated:
        return f"user-{request.user.pk}"
    seed = request.session.get(SHUFFLE_KEY)
    if not isinstance(seed, str):
        seed = secrets.token_hex(8)
        request.session[SHUFFLE_KEY] = seed
    return seed


def seen_slugs(request: HttpRequest) -> list[str]:
    raw = request.session.get(SEEN_KEY)
    return [item for item in raw if isinstance(item, str)] if isinstance(raw, list) else []


def remember_seen(request: HttpRequest, slug: str) -> None:
    seen = [item for item in seen_slugs(request) if item != slug]
    seen.append(slug)
    request.session[SEEN_KEY] = seen[-SEEN_LIMIT:]


def clear_seen(request: HttpRequest) -> None:
    request.session.pop(SEEN_KEY, None)
