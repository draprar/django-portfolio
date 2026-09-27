"""
Training heuristic for speaking and writing samples.

Rule-based scoring on English tokens: sentence shape, lexical variety,
filler words, and linking words. The numbers are a study signal.
They are not an official proficiency result and they are not calibrated
to any published language standard.
"""

from __future__ import annotations

import re

FILLERS = {"um", "uh", "er", "erm", "like", "you know"}
LINKERS = {
    "because",
    "however",
    "therefore",
    "first",
    "then",
    "finally",
    "while",
    "although",
    "also",
    "but",
    "so",
    "after",
    "before",
    "when",
    "during",
}

HEURISTIC_NOTE = "Training heuristic only; not an official proficiency score."


def tokenize(text: str) -> list[str]:
    return re.findall(r"[A-Za-z']+", (text or "").lower())


def assess_language_sample(text: str, minutes: float | None = None) -> dict[str, int | float | str]:
    tokens = tokenize(text)
    sentences = [part for part in re.split(r"[.!?]+", text or "") if part.strip()]
    unique = len(set(tokens))
    total = len(tokens)
    if minutes is None or minutes <= 0:
        minutes = max(0.75, total / 115)

    filler_count = sum(tokens.count(word) for word in FILLERS)
    linker_count = sum(tokens.count(word) for word in LINKERS)
    avg_sentence = total / max(1, len(sentences))
    lexical_ratio = unique / max(1, total)
    wpm = total / minutes

    structure = min(100, round((min(3.0, len(sentences) / 3) / 3) * 100 + min(15, linker_count * 3)))
    vocabulary = min(100, round(lexical_ratio * 110))
    fluency = max(0, min(100, round(100 - filler_count * 9 - max(0, 75 - wpm) * 0.6)))
    clarity = min(100, round((min(16, avg_sentence) / 16) * 70 + min(30, linker_count * 4)))
    overall = round((structure + vocabulary + fluency + clarity) / 4)

    return {
        "word_count": total,
        "sentence_count": len(sentences),
        "words_per_minute": round(wpm),
        "lexical_diversity": round(lexical_ratio, 2),
        "fillers": filler_count,
        "linkers": linker_count,
        "structure": structure,
        "vocabulary": vocabulary,
        "fluency": fluency,
        "clarity": clarity,
        "overall": overall,
        "note": HEURISTIC_NOTE,
    }


def coaching_hint(feedback: dict) -> tuple[str, str]:
    """The single most useful thing to change next, as (English, Polish).

    A bare percentage does not tell anyone what to do, so the weakest signal is
    turned into one concrete instruction.
    """
    words = int(feedback.get("word_count") or 0)
    sentences = int(feedback.get("sentence_count") or 0)
    fillers = int(feedback.get("fillers") or 0)
    linkers = int(feedback.get("linkers") or 0)
    diversity = float(feedback.get("lexical_diversity") or 0)

    if words < 25:
        return (
            "That is too short to judge. Aim for a few full sentences.",
            "To za krótko, żeby cokolwiek ocenić. Celuj w kilka pełnych zdań.",
        )
    if fillers >= 3:
        return (
            "Plenty of fillers there (um, like, you know). Say the same thing without them.",
            "Dużo wypełniaczy (um, like, you know). Powiedz to samo bez nich.",
        )
    if linkers == 0:
        return (
            "Nothing joins your sentences. Try because, then, however, although.",
            "Nic nie łączy Twoich zdań. Spróbuj: because, then, however, although.",
        )
    if sentences <= 1:
        return (
            "This is one long sentence. Cut it into two or three.",
            "To jedno długie zdanie. Podziel je na dwa albo trzy.",
        )
    if diversity < 0.45:
        return (
            "The same words keep coming back. Reach for a synonym next time.",
            "Te same słowa ciągle wracają. Następnym razem poszukaj synonimu.",
        )
    return (
        "Clear shape: connected sentences and varied words. Keep this length.",
        "Jasna forma: zdania są połączone, słowa się nie powtarzają. Zachowaj tę długość.",
    )
