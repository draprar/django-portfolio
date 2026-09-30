"""Turn quiz answers into one catalog style.

The guest result lives in the session, same idea as a Ćwiczba guest attempt:
count it once, then read it from a separate page. This module does not import
Ćwiczba. A blank form still returns a style, the first active one by sort order.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from walczak.models import Question, Style


def choose_style(questions: Sequence[Question], posted: Mapping[str, Any]) -> Style | None:
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
        _add(scores, choice.style, choice.points)
        _add(scores, choice.extra_style, choice.extra_points)

    active = list(Style.objects.filter(active=True).order_by("sort_order", "pk"))
    if not active:
        return None
    if not scores:
        return active[0]
    best = max(scores.values())
    ranked = [style for style in active if scores.get(style.pk, 0) == best]
    return ranked[0] if ranked else active[0]


def _add(scores: dict[int, int], style: Style | None, points: int) -> None:
    if style is None or not style.active or points <= 0:
        return
    scores[style.pk] = scores.get(style.pk, 0) + points
