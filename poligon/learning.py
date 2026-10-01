"""What to do next, and the writing rubric.

``writing_eval_v1`` stays in ``heuristics.py`` for rows already saved.
New speaking and writing attempts use ``writing_eval_v2``: five scores from
0 to 4, shown as bands. The next step is a rule, not a model.
"""

from __future__ import annotations

import re

from poligon.framework import WRITING_EVAL_V2, score_band
from poligon.heuristics import _min_words, tokenize

RUBRIC = ("task", "grammar", "vocabulary", "clarity", "structure")


def assess_writing_v2(text: str, criteria: list | None = None) -> dict:
    """Score one typed answer against the facts the task listed."""
    sample = text or ""
    tokens = tokenize(sample)
    sentences = [part.strip() for part in re.split(r"[.!?]+", sample) if part.strip()]
    facts = [str(item).strip() for item in (criteria or []) if str(item).strip()]
    lowered = sample.lower()
    checked = [{"text": fact, "met": fact.lower() in lowered} for fact in facts]
    rubric = {
        "task": _task_score(checked),
        "grammar": _grammar_score(sentences),
        "vocabulary": _vocabulary_score(tokens),
        "clarity": _clarity_score(tokens, sentences),
        "structure": _structure_score(sentences, tokens),
    }
    mean = sum(rubric.values()) / len(RUBRIC)
    return {
        "evaluator_version": WRITING_EVAL_V2,
        "rubric": rubric,
        "bands": {name: score_band(points) for name, points in rubric.items()},
        "criteria": checked,
        "word_count": len(tokens),
        "sentence_count": len(sentences),
        "overall": round(mean / 4 * 100),
        "overall_band": score_band(round(mean)),
    }


def one_improvement(feedback: dict, level: int = 2) -> tuple[str, str]:
    """One change, not a list of everything that is weak."""
    words = int(feedback.get("word_count") or 0)
    if words < _min_words(level):
        return (
            "That is too short to judge. Aim for a few full sentences.",
            "To za krótko, żeby cokolwiek ocenić. Napisz kilka pełnych zdań.",
        )
    missing = next(
        (item.get("text") for item in feedback.get("criteria") or [] if isinstance(item, dict) and not item.get("met")),
        None,
    )
    if missing:
        return (
            f"Add this fact: {missing}.",
            f"Dopisz ten fakt: {missing}.",
        )
    band = feedback.get("overall_band")
    if band == "needs_work":
        return (
            "Split the answer into two or three sentences.",
            "Podziel odpowiedź na dwa albo trzy zdania.",
        )
    return (
        "Read it once and check that every fact you were asked for is still there.",
        "Przeczytaj jeszcze raz i sprawdź, czy jest tam każdy fakt z polecenia.",
    )


def _task_score(checked: list[dict]) -> int:
    if not checked:
        return 2
    covered = sum(1 for item in checked if item["met"])
    ratio = covered / len(checked)
    if ratio == 1:
        return 4
    if ratio >= 0.67:
        return 3
    if ratio >= 0.34:
        return 2
    if covered:
        return 1
    return 0


def _grammar_score(sentences: list[str]) -> int:
    if not sentences:
        return 0
    shaped = sum(1 for sentence in sentences if sentence[:1].isupper())
    return round(4 * shaped / len(sentences))


def _vocabulary_score(tokens: list[str]) -> int:
    if not tokens:
        return 0
    ratio = len(set(tokens)) / len(tokens)
    if ratio < 0.4:
        return 1
    if ratio < 0.6:
        return 2
    if ratio < 0.8:
        return 3
    return 4


def _clarity_score(tokens: list[str], sentences: list[str]) -> int:
    if not tokens or not sentences:
        return 0
    average = len(tokens) / len(sentences)
    if average < 4:
        return 1
    if average <= 18:
        return 4
    if average <= 28:
        return 2
    return 1


def _structure_score(sentences: list[str], tokens: list[str]) -> int:
    if not sentences:
        return 0
    if len(sentences) == 1:
        base = 1
    elif len(sentences) == 2:
        base = 3
    else:
        base = 4
    if any(word in {"then", "because", "after", "and"} for word in tokens):
        base = min(4, base + 1)
    return base
