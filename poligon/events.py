"""Product events for an account. A guest still leaves no row."""

from __future__ import annotations

from django.http import HttpRequest

from poligon.identity import account_state
from poligon.models import ProductEvent

EVENT_NAMES = (
    "exercise_started",
    "exercise_completed",
    "exercise_abandoned",
    "placement_started",
    "placement_completed",
    "account_created",
    "flashcard_reviewed",
    "language_changed",
)


def record_event(request: HttpRequest | None, name: str, payload: dict | None = None, *, learner=None) -> None:
    """Store one named action when it belongs to an account."""
    if name not in EVENT_NAMES:
        return
    if learner is None and request is not None and request.user.is_authenticated:
        learner = account_state(request)
    if learner is None and name != "account_created":
        return
    ProductEvent.objects.create(name=name, learner=learner, payload=payload or {})
