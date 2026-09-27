"""Rewrite exercise instructions in Poligon's own voice.

The catalog reuses a handful of instruction strings across all 1200 exercises,
so the whole set can be re-voiced from one mapping instead of item by item.
The instructions talk to the learner ("you"), and they stop repeating the word
"heuristic" — the result page says what the score is.

Run from the repository root:

    python poligon/data/revoice_instructions.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "exercises"

# old English instruction -> (new English, new Polish)
VOICE: dict[str, tuple[str, str]] = {
    "Speak in English. The heuristic scores English.": (
        "Say it out loud in English. Write down the same thing so you get feedback.",
        "Powiedz to na głos po angielsku. Zapisz to samo, żeby dostać informację zwrotną.",
    ),
    "Write in English. The heuristic scores English.": (
        "Write your answer in English. Full sentences work better than notes.",
        "Napisz odpowiedź po angielsku. Całe zdania działają lepiej niż notatki.",
    ),
    "Listen once and choose the best answer.": (
        "Listen once, then pick the answer that fits.",
        "Posłuchaj raz, potem wybierz odpowiedź, która pasuje.",
    ),
    "Read the English paragraph and choose the best description.": (
        "Read the English paragraph. Pick the sentence that says what it is about.",
        "Przeczytaj angielski akapit. Wybierz zdanie, które mówi, o co w nim chodzi.",
    ),
    "Read the note and choose the best answer.": (
        "Read the note, then pick the answer that fits.",
        "Przeczytaj notatkę, potem wybierz odpowiedź, która pasuje.",
    ),
    "Listen once for the main facts, then choose the best answer.": (
        "Listen once for the facts, not every word. Then pick the answer.",
        "Posłuchaj raz pod kątem faktów, nie każdego słowa. Potem wybierz odpowiedź.",
    ),
    "Speak for about 90 seconds in English. The heuristic scores English.": (
        "Speak for about 90 seconds in English, then write down the same thing.",
        "Mów około 90 sekund po angielsku, potem zapisz to samo.",
    ),
    "Write 100–140 words in English. The heuristic scores English.": (
        "Write 100 to 140 words in English.",
        "Napisz 100–140 słów po angielsku.",
    ),
    "Read the short note and choose the statement that matches it.": (
        "Read the short note. Pick the sentence that matches it.",
        "Przeczytaj krótką notatkę. Wybierz zdanie, które do niej pasuje.",
    ),
    "Read or listen for the practical consequence.": (
        "Work out what actually has to happen next.",
        "Wyłap, co z tego wynika w praktyce.",
    ),
    "Listen once and choose the word you heard.": (
        "Listen once. Which word was it?",
        "Posłuchaj raz. Które to było słowo?",
    ),
    "Choose the word written in the note.": (
        "Which word is written in the note?",
        "Które słowo jest zapisane w notatce?",
    ),
    "Catch the one fact, then choose.": (
        "Catch the one fact, then choose.",
        "Złap ten jeden fakt i wybierz.",
    ),
    "Listen for sequence and timing. Choose the statement that matches the message.": (
        "Listen for the order and the time. Pick the sentence that matches.",
        "Słuchaj kolejności i godziny. Wybierz zdanie, które się z tym zgadza.",
    ),
    "Listen for sequence. Select the final step.": (
        "Listen for the order. Which step comes last?",
        "Słuchaj kolejności. Który krok jest ostatni?",
    ),
    "Read the short note and identify the essential factual point.": (
        "Read the short note. What is the one fact that matters?",
        "Przeczytaj krótką notatkę. Który fakt jest tu najważniejszy?",
    ),
    "Read and infer the practical action.": (
        "Read it, then work out what has to be done.",
        "Przeczytaj i wywnioskuj, co trzeba zrobić.",
    ),
    "Read the note and identify the comparison stated in the text.": (
        "Read the note. What is being compared with what?",
        "Przeczytaj notatkę. Co jest z czym porównane?",
    ),
    "Speak for about 90 seconds. Keep the response connected and concrete. "
    "The heuristic scores English.": (
        "Speak for about 90 seconds. Keep it concrete and connected, then write it down.",
        "Mów około 90 sekund. Konkretnie i spójnie, potem to zapisz.",
    ),
    "Speak for about 90 seconds. Explain the situation clearly and in chronological order. "
    "The heuristic scores English.": (
        "Speak for about 90 seconds, in the order things happened. Then write it down.",
        "Mów około 90 sekund, po kolei tak, jak to się działo. Potem to zapisz.",
    ),
    "Write 100–140 words. Use simple paragraphs and clear sequencing. "
    "The heuristic scores English.": (
        "Write 100 to 140 words. Short paragraphs, clear order.",
        "Napisz 100–140 słów. Krótkie akapity, jasna kolejność.",
    ),
    "Write 100–140 words. Make the sequence easy to follow. The heuristic scores English.": (
        "Write 100 to 140 words, in an order that is easy to follow.",
        "Napisz 100–140 słów w kolejności, którą łatwo śledzić.",
    ),
}


def revoice() -> tuple[int, set[str]]:
    changed = 0
    unknown: set[str] = set()
    for path in sorted(ROOT.glob("*.json")):
        items = json.loads(path.read_text(encoding="utf-8"))
        touched = False
        for item in items:
            voice = VOICE.get(item["instructions_en"])
            if voice is None:
                unknown.add(item["instructions_en"])
                continue
            new_en, new_pl = voice
            if (item["instructions_en"], item["instructions_pl"]) != (new_en, new_pl):
                item["instructions_en"] = new_en
                item["instructions_pl"] = new_pl
                changed += 1
                touched = True
        if touched:
            path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed, unknown


if __name__ == "__main__":
    count, missing = revoice()
    print(f"re-voiced {count} exercises")
    for text in sorted(missing):
        print(f"no mapping for: {text}")
