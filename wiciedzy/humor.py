"""Archetype quiz for /quiz/. Scoring stays inside this module."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from wiciedzy.models import Archetype, HumorQuestion


def choose_archetypes(questions: Sequence[HumorQuestion], posted: Mapping[str, Any]) -> list[Archetype]:
    """Return every archetype tied for the top. A blank form returns nothing."""
    scores: dict[int, int] = {}
    for question in questions:
        raw = posted.get(f"q{question.pk}")
        if isinstance(raw, bool) or not isinstance(raw, (str, int)):
            continue
        try:
            choice_id = int(raw)
        except ValueError:
            continue
        choice = next((item for item in question.choices.all() if item.pk == choice_id), None)
        if choice is None:
            continue
        scores[choice.archetype_id] = scores.get(choice.archetype_id, 0) + choice.points
    if not scores:
        return []
    best = max(scores.values())
    winner_ids = [key for key, value in scores.items() if value == best]
    return list(Archetype.objects.filter(pk__in=winner_ids).order_by("slug"))
