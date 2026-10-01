"""The five practice levels, in one place.

Start, the dashboard, settings, the account page, placement and the result
page all read the names from here, so a level cannot be called one thing on
one screen and another thing on the next.

What a learner should be able to do at that level lives in ``framework.py``.
These tuples are only the names and the one-line hints.
"""

from __future__ import annotations

LEVELS = (1, 2, 3, 4, 5)

LEVEL_LABELS = {
    1: ("Survival", "Przetrwanie"),
    2: ("Functional", "Funkcjonalny"),
    3: ("Operational", "Operacyjny"),
    4: ("Advanced", "Zaawansowany"),
    5: ("Full proficiency", "Pełna biegłość"),
}

LEVEL_HINTS = {
    1: ("One fact: a time, a place, or an order.", "Jeden fakt: godzina, miejsce albo rozkaz."),
    2: (
        "Everyday duty: route, supply, a change of plan.",
        "Codzienna służba: trasa, zaopatrzenie, zmiana planu.",
    ),
    3: ("Sequence, radio, and consequence.", "Kolejność, łączność i skutek."),
    4: ("A reason and a consequence.", "Uzasadnienie i konsekwencja."),
    5: (
        "A report: situation, effect, action, backup.",
        "Meldunek: sytuacja, wpływ, działanie, plan zastępczy.",
    ),
}


def level_names(level: int) -> tuple[str, str]:
    """English name, then Polish name. Empty strings when the number is unknown."""
    pair = LEVEL_LABELS.get(level)
    if pair is None:
        return ("", "")
    return pair
