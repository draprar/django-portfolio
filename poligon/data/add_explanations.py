"""Fill the "why" line shown after a wrong multiple-choice answer.

Only question shapes where the explanation follows from the item itself are
filled, so nothing here invents facts:

* single-word choices  -> name the word and gloss the ones that were not said
* "It is about ..."     -> explain that this is a gist question

Comprehension questions written for Poligon (the level-2 ``reading.json`` and
``listening.json`` sets) need an explanation per item and stay empty until
someone writes them.

Run from the repository root:

    python poligon/data/add_explanations.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "exercises"

GIST = {
    "L": (
        "This asks for the general topic. The right answer sums up what you heard; "
        "the others name things the message never mentions.",
        "To pytanie o ogólny temat. Dobra odpowiedź streszcza to, co usłyszałeś — "
        "pozostałe mówią o rzeczach, o których w nagraniu nie ma ani słowa.",
    ),
    "R": (
        "This asks for the general topic. The right answer sums up the whole text; "
        "the others name things the text never mentions.",
        "To pytanie o ogólny temat. Dobra odpowiedź streszcza cały tekst — "
        "pozostałe mówią o rzeczach, których w nim nie ma.",
    ),
}


def _is_gist(options: list[dict]) -> bool:
    return bool(options) and all(option["text_en"].startswith("It is about") for option in options)


def _is_single_word(options: list[dict]) -> bool:
    return bool(options) and all(len(option["text_en"].split()) == 1 for option in options)


def _word_explanation(options: list[dict], skill: str) -> tuple[str, str]:
    right = next(option for option in options if option["is_correct"])
    others = [option for option in options if not option["is_correct"]]
    glosses_en = ", ".join(f"{option['text_en']} ({option['text_pl']})" for option in others)
    glosses_pl = ", ".join(f"{option['text_en']} to {option['text_pl']}" for option in others)
    heard_en = "The word was" if skill == "L" else "The note says"
    heard_pl = "Słowo, które padło, to" if skill == "L" else "W notatce stoi"
    return (
        f"{heard_en} {right['text_en']} — {right['text_pl']}. The others mean something else: {glosses_en}.",
        f"{heard_pl}: {right['text_en']} — {right['text_pl']}. Pozostałe znaczą co innego: {glosses_pl}.",
    )


def add_explanations() -> tuple[int, int]:
    filled = 0
    skipped = 0
    for path in sorted(ROOT.glob("*.json")):
        items = json.loads(path.read_text(encoding="utf-8"))
        touched = False
        for item in items:
            options = item.get("options") or []
            if not options:
                continue
            if _is_single_word(options):
                explanation = _word_explanation(options, item["skill"])
            elif _is_gist(options):
                explanation = GIST[item["skill"]]
            else:
                skipped += 1
                continue
            if (item.get("explanation_en"), item.get("explanation_pl")) != explanation:
                item["explanation_en"], item["explanation_pl"] = explanation
                filled += 1
                touched = True
        if touched:
            path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return filled, skipped


if __name__ == "__main__":
    written, left = add_explanations()
    print(f"explained {written} exercises, {left} still need a hand-written why")
