"""What a practice level means, and the closed lists content is allowed to use.

Labels shown on screen stay in ``levels.py``. This module is the competency
profile those labels point at: a level is not a difficulty number stored in
JSON. Scoring, placement and the review schedule are named here so later code
can record which version produced a result.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

SKILLS = ("L", "S", "R", "W")

EXERCISE_TYPES_LIVE = ("mcq", "listening", "speaking", "writing", "true_false")
EXERCISE_TYPES_RESERVED = (
    "sequence",
    "main_idea",
    "detail",
    "inference",
    "short_answer",
)
EXERCISE_TYPES = EXERCISE_TYPES_LIVE + EXERCISE_TYPES_RESERVED

PUBLICATION_STATUSES = ("draft", "review", "approved", "published", "deprecated")
QUALITY_LEGACY = "legacy"
QUALITY_UNCHECKED = "unchecked"
QUALITY_PASSED = "passed"

SOURCE_TYPES = ("original", "external", "adapted", "generated")
CATALOG_ROLES = ("practice", "placement")

PLACEMENT_VERSION = "placement_v1"
PLACEMENT_QUESTION_COUNT = 15
WRITING_EVAL_V1 = "writing_eval_v1"
WRITING_EVAL_V2 = "writing_eval_v2"
SRS_VERSION = "srs_v1"
SRS_SUMMARY = (
    "Custom schedule: a grade below 3 is due again in 20 minutes; "
    "a passing grade waits 1 day, then 3 days, then interval times ease. "
    "This is not textbook SM-2."
)

COVERAGE_GATES = (1, 8, 20)

GLOSSARY_PATH = Path(__file__).resolve().parent / "data" / "glossary.json"


@dataclass(frozen=True)
class Scenario:
    id: str
    name_en: str
    name_pl: str


@dataclass(frozen=True)
class Competency:
    """One minimum ability for a level and a skill."""

    id: str
    skill: str
    text_en: str
    text_pl: str


@dataclass(frozen=True)
class LevelProfile:
    level: int
    goal_en: str
    goal_pl: str
    utterance_en: str
    utterance_pl: str
    speed_en: str
    speed_pl: str
    ambiguity_en: str
    ambiguity_pl: str
    competencies: dict[str, Competency]
    scenarios: tuple[str, ...]


SCENARIOS = (
    Scenario("orders", "Orders", "Rozkazy"),
    Scenario("time", "Time", "Czas"),
    Scenario("numbers", "Numbers", "Liczby"),
    Scenario("checkpoint", "Checkpoint", "Punkt kontrolny"),
    Scenario("logistics", "Logistics", "Logistyka"),
    Scenario("equipment", "Equipment", "Sprzęt"),
    Scenario("weather", "Weather", "Pogoda"),
    Scenario("vehicle", "Vehicle movement", "Ruch pojazdów"),
    Scenario("briefing", "Briefing", "Odprawa"),
    Scenario("radio", "Radio", "Łączność"),
    Scenario("patrol", "Patrol", "Patrol"),
    Scenario("map", "Map", "Mapa"),
    Scenario("medical", "Medical", "Medyczny"),
    Scenario("handover", "Handover", "Przekazanie"),
    Scenario("reporting", "Reporting", "Meldunek"),
)

_SCENARIO_IDS = {item.id for item in SCENARIOS}

_L1 = ("orders", "time", "numbers")
_L2 = _L1 + ("checkpoint", "logistics", "equipment", "weather", "vehicle")
_L3 = _L2 + ("briefing", "radio", "patrol", "map")
_L4 = _L3 + ("medical", "handover", "reporting")
_L5 = _L4


def _competency(level: int, skill: str, text_en: str, text_pl: str) -> Competency:
    skill_name = {"L": "listening", "S": "speaking", "R": "reading", "W": "writing"}[skill]
    return Competency(f"l{level}-{skill_name}", skill, text_en, text_pl)


LEVEL_PROFILES: dict[int, LevelProfile] = {
    1: LevelProfile(
        level=1,
        goal_en="Understand a basic message: a number, a direction, or a simple order.",
        goal_pl="Rozumie podstawowy komunikat: liczbę, kierunek albo prosty rozkaz.",
        utterance_en="One short sentence.",
        utterance_pl="Jedno krótkie zdanie.",
        speed_en="Slow and clear.",
        speed_pl="Wolno i wyraźnie.",
        ambiguity_en="One meaning. No extra detail that could be the answer.",
        ambiguity_pl="Jedno znaczenie. Żaden dodatkowy szczegół nie może być odpowiedzią.",
        scenarios=_L1,
        competencies={
            "L": _competency(
                1,
                "L",
                "Understands a time, a number, a direction, or a simple order.",
                "Rozumie godzinę, liczbę, kierunek albo prosty rozkaz.",
            ),
            "S": _competency(
                1,
                "S",
                "Says one fact: a time, a place, or a simple need.",
                "Mówi jeden fakt: godzinę, miejsce albo prostą potrzebę.",
            ),
            "R": _competency(
                1,
                "R",
                "Reads a one-fact note and identifies the time, place, or quantity.",
                "Czyta notatkę z jednym faktem i wskazuje godzinę, miejsce albo liczbę.",
            ),
            "W": _competency(
                1,
                "W",
                "Writes one or two simple sentences with a time, a place, or a quantity.",
                "Pisze jedno albo dwa proste zdania z godziną, miejscem albo liczbą.",
            ),
        },
    ),
    2: LevelProfile(
        level=2,
        goal_en="Take part in a simple duty situation: a route, a supply, a change of plan.",
        goal_pl="Uczestniczy w prostej sytuacji służbowej: trasa, zaopatrzenie, zmiana planu.",
        utterance_en="Two to four short sentences.",
        utterance_pl="Dwa do czterech krótkich zdań.",
        speed_en="Careful everyday pace.",
        speed_pl="Spokojne, codzienne tempo.",
        ambiguity_en="One main fact, plus a detail that is not the task.",
        ambiguity_pl="Jeden główny fakt i szczegół, który nie jest zadaniem.",
        scenarios=_L2,
        competencies={
            "L": _competency(
                2,
                "L",
                "Follows a short duty exchange about a route, supply, or a change of plan.",
                "Nadąża za krótką wymianą o trasie, zaopatrzeniu albo zmianie planu.",
            ),
            "S": _competency(
                2,
                "S",
                "Takes a short turn in a simple duty situation.",
                "Zabiera głos w prostej sytuacji służbowej.",
            ),
            "R": _competency(
                2,
                "R",
                "Reads a short note and finds the fact the task asks for.",
                "Czyta krótką notatkę i znajduje fakt, o który pyta zadanie.",
            ),
            "W": _competency(
                2,
                "W",
                "Writes a short message about a route, a supply, or a change of plan.",
                "Pisze krótką wiadomość o trasie, zaopatrzeniu albo zmianie planu.",
            ),
        },
    ),
    3: LevelProfile(
        level=3,
        goal_en="Cope with communication that is no longer fully predictable.",
        goal_pl="Radzi sobie z komunikacją, która nie jest już w pełni przewidywalna.",
        utterance_en="A short paragraph or several turns.",
        utterance_pl="Krótki akapit albo kilka wymian.",
        speed_en="Natural pace, with a few words that may be new.",
        speed_pl="Naturalne tempo, z kilkoma słowami, które mogą być nowe.",
        ambiguity_en="A sequence or a cause, and one detail that is not the point.",
        ambiguity_pl="Kolejność albo przyczyna oraz jeden szczegół, który nie jest sednem.",
        scenarios=_L3,
        competencies={
            "L": _competency(
                3,
                "L",
                "Follows a sequence and what happens because of it.",
                "Śledzi kolejność i to, co z niej wynika.",
            ),
            "S": _competency(
                3,
                "S",
                "Handles a short exchange when the next fact is not fully scripted.",
                "Prowadzi krótką wymianę, gdy kolejny fakt nie jest w pełni zapisany.",
            ),
            "R": _competency(
                3,
                "R",
                "Understands a short operational note, finds the main fact, follows the order of events, "
                "recognises cause and effect, copes with some unknown words, and separates an important "
                "detail from a side fact.",
                "Rozumie krótką notatkę operacyjną, wyławia najważniejszą informację, rozumie chronologię, "
                "rozpoznaje przyczynę i skutek, radzi sobie z częściowo nieznanym słownictwem i odróżnia "
                "istotny szczegół od informacji pobocznej.",
            ),
            "W": _competency(
                3,
                "W",
                "Writes a short account of what happened and what should happen next.",
                "Pisze krótki opis tego, co się stało i co ma stać się dalej.",
            ),
        },
    ),
    4: LevelProfile(
        level=4,
        goal_en="Understand a longer instruction, a report, and a reason.",
        goal_pl="Rozumie dłuższą instrukcję, meldunek i uzasadnienie.",
        utterance_en="Several connected sentences.",
        utterance_pl="Kilka powiązanych zdań.",
        speed_en="Natural pace across more than one point.",
        speed_pl="Naturalne tempo przez więcej niż jedną myśl.",
        ambiguity_en="A reason and a nuance. One reading is still the intended one.",
        ambiguity_pl="Uzasadnienie i niuans. Nadal jest jedno zamierzone odczytanie.",
        scenarios=_L4,
        competencies={
            "L": _competency(
                4,
                "L",
                "Understands a longer instruction, including why something is done.",
                "Rozumie dłuższą instrukcję, także powód działania.",
            ),
            "S": _competency(
                4,
                "S",
                "Explains a reason and a consequence in a few connected sentences.",
                "Wyjaśnia powód i skutek w kilku powiązanych zdaniach.",
            ),
            "R": _competency(
                4,
                "R",
                "Reads a longer instruction or report and keeps the main point apart from supporting detail.",
                "Czyta dłuższą instrukcję albo meldunek i oddziela myśl główną od szczegółu.",
            ),
            "W": _competency(
                4,
                "W",
                "Writes a short report with a reason, a consequence, and the action asked for.",
                "Pisze krótki meldunek z powodem, skutkiem i oczekiwanym działaniem.",
            ),
        },
    ),
    5: LevelProfile(
        level=5,
        goal_en="Work in complex communication: situation, effect, action, and a backup.",
        goal_pl="Działa w złożonej komunikacji: sytuacja, wpływ, działanie i plan zastępczy.",
        utterance_en="A full short report.",
        utterance_pl="Pełny krótki meldunek.",
        speed_en="Natural pace, including a point that has to be resolved.",
        speed_pl="Naturalne tempo, także gdy jedną rzecz trzeba dopiero ustalić.",
        ambiguity_en="More than one possible reading. The task still has one intended outcome.",
        ambiguity_pl="Więcej niż jedno możliwe odczytanie. Zadanie nadal ma jeden zamierzony wynik.",
        scenarios=_L5,
        competencies={
            "L": _competency(
                5,
                "L",
                "Follows a complex message: situation, effect, action, and backup.",
                "Śledzi złożony komunikat: sytuację, wpływ, działanie i plan zastępczy.",
            ),
            "S": _competency(
                5,
                "S",
                "Takes part fluently and can repair a misunderstanding in the same exchange.",
                "Uczestniczy płynnie i potrafi w tej samej wymianie naprawić nieporozumienie.",
            ),
            "R": _competency(
                5,
                "R",
                "Reads a full short report and tracks situation, effect, action, and backup.",
                "Czyta pełny krótki meldunek i śledzi sytuację, wpływ, działanie i plan zastępczy.",
            ),
            "W": _competency(
                5,
                "W",
                "Writes a report with the situation, the effect, the action, and a backup.",
                "Pisze meldunek z sytuacją, wpływem, działaniem i planem zastępczym.",
            ),
        },
    ),
}


def scenario_by_id(scenario_id: str) -> Scenario | None:
    for item in SCENARIOS:
        if item.id == scenario_id:
            return item
    return None


def level_profile(level: int) -> LevelProfile | None:
    return LEVEL_PROFILES.get(level)


def competency_for(level: int, skill: str) -> Competency | None:
    profile = LEVEL_PROFILES.get(level)
    if profile is None:
        return None
    return profile.competencies.get(skill)


def suggest_placement_level(correct: int) -> int:
    """placement_v1. Fifteen questions. A different cut is a new version."""
    if correct <= 3:
        return 1
    if correct <= 6:
        return 2
    if correct <= 9:
        return 3
    if correct <= 12:
        return 4
    return 5


def score_band(score: int) -> str:
    """A 0–4 rubric point, shown as a band rather than a false percentage."""
    if score <= 1:
        return "needs_work"
    if score == 2:
        return "developing"
    return "strong"


def load_glossary() -> list[dict[str, str]]:
    raw = json.loads(GLOSSARY_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("glossary.json must be a list")
    return raw
