"""Score a short public-domain IPIP set. Nothing here picks a martial art."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence

from walczak.models import IPIPItem

SCALE_ORDER = ("E", "A", "C", "N", "O")


def score_ipip(items: Sequence[IPIPItem], answers: Mapping[int, int]) -> dict[str, float]:
    buckets: dict[str, list[int]] = defaultdict(list)
    for item in items:
        raw = answers.get(item.pk)
        if raw is None:
            continue
        value = 6 - raw if item.reverse else raw
        buckets[item.scale.code].append(value)
    return {code: (sum(buckets[code]) / len(buckets[code]) if buckets[code] else 0.0) for code in SCALE_ORDER}
