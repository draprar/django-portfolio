"""Match a preference vector to training profiles. This module does not read psychology.

Distance orders a reading list. It is not a score to show.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any

from wiciedzy.data.instruments import OPTIONAL_SCALE_ORDERS
from wiciedzy.dimensions import LOW_REASON_COPY, REASON_COPY
from wiciedzy.models import PreferenceQuestion, StyleRelation, TrainingProfile

READING_LIMIT = 5
FAMILY_CAP = 2
REQUIRED_KINDS = frozenset({"scale", "ab", "situation"})


def answers_complete(questions: Sequence[PreferenceQuestion], posted: Mapping[str, Any]) -> bool:
    """Required scales, the choice questions, and the situation. Optional scales and the multi may be blank."""
    for question in questions:
        if question.kind not in REQUIRED_KINDS:
            continue
        if question.sort_order in OPTIONAL_SCALE_ORDERS:
            continue
        if question.kind == "scale":
            picked = _parse_int(posted.get(f"s{question.pk}"))
            if picked is None or not question.dimension or picked < 1 or picked > 5:
                return False
            continue
        selected = _selected_ids(posted, question)
        option_ids = {option.pk for option in question.options.all()}
        if len(selected) != 1 or selected[0] not in option_ids:
            return False
    return True


def rank_styles(questions: Sequence[PreferenceQuestion], posted: Mapping[str, Any]) -> dict[str, list[dict[str, Any]]]:
    user = user_vector(questions, posted)
    if not user:
        return {"picks": []}
    rows: list[dict[str, Any]] = []
    profiles = TrainingProfile.objects.select_related("style").filter(style__active=True, style__matcher_enabled=True)
    for profile in profiles:
        style_vector = profile.as_vector()
        shared = [name for name in user if name in style_vector]
        if not shared:
            continue
        distance = sum(abs(user[name] - style_vector[name]) for name in shared) / len(shared)
        plus_pl, plus_en, minus_pl, minus_en = _reasons(user, style_vector, shared)
        rows.append(
            {
                "slug": profile.style.slug,
                "style": profile.style,
                "distance": distance,
                "family": profile.style.family,
                "plus_pl": plus_pl,
                "plus_en": plus_en,
                "minus_pl": minus_pl,
                "minus_en": minus_en,
                "beside": [],
            }
        )
    rows.sort(key=_sort_key)
    return {"picks": _reading_list(rows, _relation_pairs())}


def _sort_key(row: dict[str, Any]) -> tuple[float, str]:
    return (float(row["distance"]), str(row["slug"]))


def user_vector(questions: Sequence[PreferenceQuestion], posted: Mapping[str, Any]) -> dict[str, float]:
    sums: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)
    for question in questions:
        if question.kind == "scale":
            picked = _parse_int(posted.get(f"s{question.pk}"))
            if picked is None or not question.dimension or picked < 1 or picked > 5:
                continue
            sums[question.dimension] += (picked - 1) / 4 * 5
            counts[question.dimension] += 1
            continue
        selected = _selected_ids(posted, question)
        options = {option.pk: option for option in question.options.all()}
        if question.kind == "multi":
            selected_options = [options[option_id] for option_id in selected if option_id in options]
            if any(not list(option.weights.all()) for option in selected_options):
                continue
        for option_id in selected:
            option = options.get(option_id)
            if option is None:
                continue
            for weight in option.weights.all():
                value = max(0.0, min(5.0, 2.5 + weight.weight * 1.25))
                sums[weight.dimension] += value
                counts[weight.dimension] += 1
    return {name: sums[name] / counts[name] for name in sums}


def _reading_list(rows: list[dict[str, Any]], pairs: set[frozenset[str]]) -> list[dict[str, Any]]:
    provisional: list[dict[str, Any]] = []
    family_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        if family_counts[row["family"]] >= FAMILY_CAP:
            continue
        provisional.append(row)
        family_counts[row["family"]] += 1
        if len(provisional) == READING_LIMIT:
            break

    dropped: set[str] = set()
    beside_for: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for index, row in enumerate(provisional):
        if row["slug"] in dropped:
            continue
        for other in provisional[index + 1 :]:
            if other["slug"] in dropped:
                continue
            if frozenset((row["slug"], other["slug"])) in pairs:
                dropped.add(other["slug"])
                beside_for[row["slug"]].append(other)

    kept = [row for row in provisional if row["slug"] not in dropped]
    for row in kept:
        row["beside"] = [_beside(other) for other in beside_for[row["slug"]]]

    used = {row["slug"] for row in kept} | dropped
    family_counts = defaultdict(int)
    for row in kept:
        family_counts[row["family"]] += 1
    if len(kept) < READING_LIMIT:
        for row in rows:
            if row["slug"] in used:
                continue
            if family_counts[row["family"]] >= FAMILY_CAP:
                continue
            if any(frozenset((row["slug"], kept_row["slug"])) in pairs for kept_row in kept):
                used.add(row["slug"])
                continue
            kept.append(row)
            used.add(row["slug"])
            family_counts[row["family"]] += 1
            if len(kept) == READING_LIMIT:
                break
    return kept


def _beside(row: dict[str, Any]) -> dict[str, str]:
    style = row["style"]
    return {"slug": style.slug, "name_pl": style.name_pl, "name_en": style.name_en}


def _relation_pairs() -> set[frozenset[str]]:
    pairs: set[frozenset[str]] = set()
    for left, right in StyleRelation.objects.values_list("from_style__slug", "to_style__slug"):
        pairs.add(frozenset((left, right)))
    return pairs


def _selected_ids(posted: Mapping[str, Any], question: PreferenceQuestion) -> list[int]:
    if question.kind == "multi":
        raw_many = posted.get(f"m{question.pk}")
        if hasattr(posted, "getlist"):
            raw_values = posted.getlist(f"m{question.pk}")
        elif isinstance(raw_many, list):
            raw_values = raw_many
        elif raw_many is None:
            raw_values = []
        else:
            raw_values = [raw_many]
    else:
        raw_values = [posted.get(f"q{question.pk}")]
    parsed: list[int] = []
    for raw in raw_values:
        value = _parse_int(raw)
        if value is not None:
            parsed.append(value)
    return parsed


def _reasons(
    user: dict[str, float],
    style_vector: dict[str, int],
    shared: list[str],
) -> tuple[list[str], list[str], list[str], list[str]]:
    plus: list[tuple[float, str, tuple[str, str]]] = []
    minus: list[tuple[float, str, tuple[str, str]]] = []
    for name in shared:
        copy = REASON_COPY.get(name)
        if copy is None:
            continue
        diff = abs(user[name] - style_vector[name])
        low = LOW_REASON_COPY.get(name)
        if diff <= 1 and user[name] >= 3 and style_vector[name] >= 3:
            plus.append((diff, name, copy[0]))
        elif low is not None and diff <= 1 and user[name] <= 1.5 and style_vector[name] <= 1:
            plus.append((diff, name, low))
        elif diff >= 2.5:
            side = copy[1] if style_vector[name] > user[name] else copy[2]
            minus.append((diff, name, side))
    plus.sort(key=lambda item: (item[0], item[1]))
    minus.sort(key=lambda item: (-item[0], item[1]))
    plus_lines = [item[2] for item in plus[:3]]
    minus_lines = [item[2] for item in minus[:2]]
    return (
        [line[0] for line in plus_lines],
        [line[1] for line in plus_lines],
        [line[0] for line in minus_lines],
        [line[1] for line in minus_lines],
    )


def _parse_int(raw: Any) -> int | None:
    if isinstance(raw, bool) or not isinstance(raw, (str, int)):
        return None
    try:
        return int(raw)
    except ValueError:
        return None
