"""Write practice levels 0, 1, 3, 4 and 5. Level 2 already lives in the earlier files.

Wikipedia extracts and Tatoeba sentences are stored only when the API returns a CC license.
Wiktionary definitions reuse the cached helper in build_catalog.py.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from build_catalog import ATTR_EN, ATTR_PL, LICENSE, RETRIEVED, fetch_definition, load_cache  # noqa: E402
from fetch_tatoeba import fetch_sentence  # noqa: E402
from fetch_wikipedia import fetch_summary  # noqa: E402

COUNTS = {0: 8, 1: 8, 3: 8, 4: 4, 5: 4}
WIKI_TITLES = {
    1: ["Weather", "Breakfast"],
    3: ["Public_transport", "First_aid"],
    4: ["Logistics", "Navigation"],
    5: ["Occupational_safety_and_health", "Emergency_management"],
}
TOPICS = [
    ("water", "water", "woda", "logistics", "logistyka"),
    ("gate", "gate", "brama", "procedures", "procedury"),
    ("radio", "radio", "radiostacja", "communications", "łączność"),
    ("meal", "meal", "posiłek", "logistics", "logistyka"),
    ("map", "map", "mapa", "movement", "przemieszczanie"),
    ("bus", "bus", "autobus", "movement", "przemieszczanie"),
    ("rain", "rain", "deszcz", "weather", "pogoda"),
    ("tent", "tent", "namiot", "equipment", "sprzęt"),
]
WORDS = {
    0: ["yes", "no", "hello", "stop", "go", "left", "right", "one", "two", "help", "please", "name", "door", "bed", "day", "night", "hot", "cold", "open", "close"],
    1: ["ticket", "station", "breakfast", "doctor", "hotel", "key", "bag", "train", "street", "shop", "price", "today", "tomorrow", "late", "early", "phone", "number", "room", "bus stop", "rainy"],
    3: ["milestone", "handover", "estimate", "priority", "constraint", "debrief", "outcome", "resource", "stakeholder", "mitigation", "compliance", "workload", "itinerary", "contingency", "liaison", "protocol", "capacity", "surplus", "shortage", "timeline"],
    4: ["assumption", "implication", "criterion", "discrepancy", "feasibility", "oversight", "rationale", "scope", "threshold", "trade-off", "accountability", "benchmark", "escalation", "procurement", "resilience", "ambiguity", "bottleneck", "justification", "provision", "sustainment"],
    5: ["nuance", "caveat", "corollary", "precedent", "inference", "synthesis", "discretion", "mandate", "jurisdiction", "liability", "proportionality", "stake", "contention", "qualification", "attribution", "coherence", "premise", "rebuttal", "stipulation", "viability"],
}
WIKI_CHOICES = {
    "Weather": ("It is about weather.", "Chodzi o pogodę."),
    "Breakfast": ("It is about a morning meal.", "Chodzi o poranny posiłek."),
    "Public_transport": ("It is about public transport.", "Chodzi o transport publiczny."),
    "First_aid": ("It is about first aid.", "Chodzi o pierwszą pomoc."),
    "Logistics": ("It is about moving supplies.", "Chodzi o przemieszczanie zaopatrzenia."),
    "Navigation": ("It is about finding the way.", "Chodzi o odnajdywanie drogi."),
    "Occupational_safety_and_health": ("It is about safety at work.", "Chodzi o bezpieczeństwo w pracy."),
    "Emergency_management": ("It is about handling an emergency.", "Chodzi o działanie w sytuacji nagłej."),
}
WIKI_WRONGS = [
    ("It is about a spare tyre.", "Chodzi o zapasową oponę."),
    ("It is about a radio call sign.", "Chodzi o sygnał wywoławczy."),
    ("It is about a night shift roster.", "Chodzi o grafik nocnej zmiany."),
]
GLOSSES = {
    "yes": "tak", "no": "nie", "hello": "cześć", "stop": "stop", "go": "idź", "left": "lewo", "right": "prawo",
    "one": "jeden", "two": "dwa", "help": "pomoc", "please": "proszę", "name": "imię", "door": "drzwi",
    "bed": "łóżko", "day": "dzień", "night": "noc", "hot": "gorący", "cold": "zimny", "open": "otwarty",
    "close": "zamknij", "ticket": "bilet", "station": "stacja", "breakfast": "śniadanie", "doctor": "lekarz",
    "hotel": "hotel", "key": "klucz", "bag": "torba", "train": "pociąg", "street": "ulica", "shop": "sklep",
    "price": "cena", "today": "dziś", "tomorrow": "jutro", "late": "spóźniony", "early": "wcześnie",
    "phone": "telefon", "number": "numer", "room": "pokój", "bus stop": "przystanek", "rainy": "deszczowy",
    "milestone": "kamień milowy", "handover": "przekazanie", "estimate": "szacunek", "priority": "priorytet",
    "debrief": "omówienie po zadaniu", "bottleneck": "wąskie gardło",
    "constraint": "ograniczenie", "outcome": "rezultat", "resource": "zasób",
    "stakeholder": "interesariusz", "mitigation": "łagodzenie ryzyka", "compliance": "zgodność",
    "workload": "obciążenie pracą", "itinerary": "plan podróży", "contingency": "wariant awaryjny",
    "liaison": "łącznik", "protocol": "protokół", "capacity": "zdolność", "surplus": "nadwyżka",
    "shortage": "niedobór", "timeline": "oś czasu", "assumption": "założenie", "implication": "konsekwencja",
    "criterion": "kryterium", "discrepancy": "rozbieżność", "feasibility": "wykonalność", "oversight": "nadzór",
    "rationale": "uzasadnienie", "scope": "zakres", "threshold": "próg", "trade-off": "kompromis",
    "accountability": "odpowiedzialność", "benchmark": "punkt odniesienia", "escalation": "eskalacja",
    "procurement": "zakupy", "resilience": "odporność", "ambiguity": "niejednoznaczność",
    "justification": "uzasadnienie", "provision": "postanowienie", "sustainment": "utrzymanie",
    "nuance": "niuans", "caveat": "zastrzeżenie", "corollary": "wniosek uboczny", "precedent": "precedens",
    "inference": "wnioskowanie", "synthesis": "synteza", "discretion": "swoboda decyzji", "mandate": "mandat",
    "jurisdiction": "właściwość", "liability": "odpowiedzialność prawna", "proportionality": "proporcjonalność",
    "stake": "stawka", "contention": "spór", "qualification": "zastrzeżenie", "attribution": "przypisanie",
    "coherence": "spójność", "premise": "przesłanka", "rebuttal": "odparcie", "stipulation": "warunek",
    "viability": "wykonalność",
}


def clip(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def base_exercise(level: int, slug: str, skill: str, exercise_type: str, minutes: int, topic: tuple) -> dict:
    _key, _en, _pl, cat_en, cat_pl = topic
    return {
        "slug": slug,
        "skill": skill,
        "level": level,
        "exercise_type": exercise_type,
        "expected_minutes": minutes,
        "original_content": True,
        "source_note": "Original Poligon text",
        "content_source": "original",
        "source_url": "",
        "source_license": "",
        "retrieved_at": None,
        "attribution_en": "",
        "attribution_pl": "",
        "category_en": cat_en,
        "category_pl": cat_pl,
        "content_en": "",
        "content_pl": "",
    }


def options(correct: tuple[str, str], wrongs: list[tuple[str, str]]) -> list[dict]:
    rows = [{"text_en": correct[0], "text_pl": correct[1], "is_correct": True}]
    rows.extend({"text_en": en, "text_pl": pl, "is_correct": False} for en, pl in wrongs)
    return rows


def listening_and_reading(level: int, kind: str) -> list[dict]:
    rows = []
    skill = "L" if kind == "listening" else "R"
    exercise_type = "listening" if kind == "listening" else "mcq"
    for index in range(COUNTS[level]):
        topic = TOPICS[index % len(TOPICS)]
        key, word_en, word_pl, _cat_en, _cat_pl = topic
        other = TOPICS[(index + 1) % len(TOPICS)]
        third = TOPICS[(index + 2) % len(TOPICS)]
        fourth = TOPICS[(index + 3) % len(TOPICS)]
        slug = f"l{level}-{skill.lower()}-{index:02d}-{key}"
        row = base_exercise(level, slug, skill, exercise_type, 6 if skill == "R" else 7, topic)
        if level == 0 and skill == "L":
            row["title_en"] = f"Hear the word: {word_en}"
            row["title_pl"] = f"Usłysz słowo: {word_pl}"
            row["instructions_en"] = "Listen once and choose the word you heard."
            row["instructions_pl"] = "Posłuchaj raz i wybierz słowo, które usłyszałeś."
            row["prompt_en"] = "Which word was said?"
            row["prompt_pl"] = "Które słowo padło?"
            row["content_en"] = word_en
            row["content_pl"] = word_pl
        elif level == 0:
            row["title_en"] = f"Read the word: {word_en}"
            row["title_pl"] = f"Przeczytaj słowo: {word_pl}"
            row["instructions_en"] = "Choose the word written in the note."
            row["instructions_pl"] = "Wybierz słowo zapisane w notatce."
            row["prompt_en"] = word_en
            row["prompt_pl"] = word_pl
        elif level == 1:
            row["title_en"] = f"A short note about {word_en}"
            row["title_pl"] = f"Krótka notatka o: {word_pl}"
            row["instructions_en"] = "Catch the one fact, then choose."
            row["instructions_pl"] = "Złap jeden fakt i wybierz."
            row["prompt_en"] = f"The {word_en} is ready at seven."
            row["prompt_pl"] = f"{word_pl[:1].upper()}{word_pl[1:]} jest gotowe o siódmej."
            row["content_en"] = row["prompt_en"]
            row["content_pl"] = row["prompt_pl"]
        else:
            row["title_en"] = f"Level {level} note: {word_en}"
            row["title_pl"] = f"Notatka poziomu {level}: {word_pl}"
            row["instructions_en"] = "Read or listen for the practical consequence."
            row["instructions_pl"] = "Wychwyć praktyczną konsekwencję."
            row["prompt_en"] = (
                f"The team cannot start until the {word_en} is confirmed. "
                f"If it is late, use the backup and tell the shift leader."
            )
            row["prompt_pl"] = (
                f"Zespół nie zaczyna, dopóki nie ma potwierdzenia: {word_pl}. "
                f"Jeśli to się spóźnia, użyj zapasu i powiedz dowódcy zmiany."
            )
            row["content_en"] = row["prompt_en"]
            row["content_pl"] = row["prompt_pl"]
        if skill == "R":
            row["content_en"] = ""
            row["content_pl"] = ""
        if level == 0:
            correct = (word_en, word_pl)
            wrongs = [(other[1], other[2]), (third[1], third[2]), (fourth[1], fourth[2])]
        else:
            correct = (f"It is about the {word_en}.", f"Chodzi o: {word_pl}.")
            wrongs = [
                (f"It is about the {other[1]}.", f"Chodzi o: {other[2]}."),
                (f"It is about the {third[1]}.", f"Chodzi o: {third[2]}."),
                (f"It is about the {fourth[1]}.", f"Chodzi o: {fourth[2]}."),
            ]
        row["options"] = options(correct, wrongs)
        rows.append(row)
    return rows


def apply_wikipedia(level: int, rows: list[dict]) -> None:
    titles = WIKI_TITLES.get(level, [])
    for index, title in enumerate(titles):
        if index >= len(rows):
            break
        try:
            summary = fetch_summary(title)
        except Exception as exc:  # noqa: BLE001 — keep the original item if the source is unavailable
            print("wiki skip", title, exc)
            continue
        if not summary:
            print("wiki skip", title)
            continue
        row = rows[index]
        choice = WIKI_CHOICES[title]
        row["slug"] = f"l{level}-r-wiki-{index:02d}"
        row["title_en"] = summary["title"]
        row["title_pl"] = summary["title"]
        row["instructions_en"] = "Read the English paragraph and choose the best description."
        row["instructions_pl"] = "Przeczytaj angielski akapit i wybierz najlepszy opis."
        row["original_content"] = False
        row["content_source"] = "wikipedia"
        row["source_url"] = summary["url"]
        row["source_license"] = summary["license"]
        row["retrieved_at"] = RETRIEVED
        row["source_note"] = "English stimulus from Wikipedia. Question and choices are original."
        row["prompt_en"] = summary["extract"]
        row["prompt_pl"] = "Przeczytaj angielski akapit. Pytanie i odpowiedzi są oryginalne."
        row["attribution_en"] = clip(
            f"Shortened English text from the Wikipedia article “{summary['title']}”, CC BY-SA 4.0. "
            "Question and choices are original.",
            300,
        )
        row["attribution_pl"] = clip(
            f"Skrócony angielski tekst z artykułu Wikipedii „{summary['title']}”, CC BY-SA 4.0. "
            "Pytanie i odpowiedzi są oryginalne.",
            300,
        )
        row["options"] = options(choice, WIKI_WRONGS)
        print("wiki", title)
        time.sleep(0.6)


def speaking_and_writing(level: int, kind: str) -> list[dict]:
    rows = []
    skill = "S" if kind == "speaking" else "W"
    for index in range(COUNTS[level]):
        topic = TOPICS[index % len(TOPICS)]
        key, word_en, word_pl, _cat_en, _cat_pl = topic
        slug = f"l{level}-{skill.lower()}-{index:02d}-{key}"
        row = base_exercise(level, slug, skill, kind, 8, topic)
        row["source_note"] = "Original Poligon prompt"
        if kind == "speaking":
            row["title_en"] = f"Say something about {word_en}"
            row["title_pl"] = f"Powiedz coś o: {word_pl}"
            row["instructions_en"] = "Speak in English. The heuristic scores English."
            row["instructions_pl"] = "Mów po angielsku. Heurystyka ocenia angielski."
            row["prompt_en"] = f"In a few connected sentences, explain when you need {word_en} and what you do if it is missing."
            row["prompt_pl"] = f"W kilku powiązanych zdaniach wyjaśnij, kiedy potrzebujesz: {word_pl}, i co robisz, gdy tego brakuje."
        else:
            row["title_en"] = f"Write about {word_en}"
            row["title_pl"] = f"Napisz o: {word_pl}"
            row["instructions_en"] = "Write in English. The heuristic scores English."
            row["instructions_pl"] = "Pisz po angielsku. Heurystyka ocenia angielski."
            row["prompt_en"] = (
                f"Write a short note. Mention {word_en}, one time, and one person who should confirm it."
            )
            row["prompt_pl"] = (
                f"Napisz krótką notatkę. Wspomnij: {word_pl}, jedną godzinę i jedną osobę, która ma to potwierdzić."
            )
        if level >= 4:
            row["prompt_en"] += " Give a reason and a backup plan."
            row["prompt_pl"] += " Podaj powód i plan zastępczy."
        rows.append(row)
    return rows


def vocabulary_for(level: int, cache: dict[str, str]) -> list[dict]:
    rows = []
    for term in WORDS[level]:
        gloss = GLOSSES[term]
        example_en = f"Please check the {term} before you leave."
        example_pl = f"Sprawdź proszę ({gloss}), zanim wyjdziesz."
        definition = ""
        try:
            definition = fetch_definition(term, cache)
        except Exception as exc:  # noqa: BLE001
            print("wiki-dict skip", term, exc)
        sentence = None
        try:
            sentence = fetch_sentence(term)
            time.sleep(0.4)
        except Exception as exc:  # noqa: BLE001
            print("tatoeba skip", term, exc)
        row = {
            "term": term,
            "translation": gloss,
            "explanation_en": definition or f"A useful word at this practice level: {term}.",
            "explanation_pl": f"W tym zestawie: {gloss}.",
            "example_en": sentence["text"] if sentence else example_en,
            "example_pl": example_pl,
            "category_en": "general",
            "category_pl": "ogólny",
            "level": level,
            "content_source": "wiktionary" if definition else "original",
            "source_url": f"https://en.wiktionary.org/wiki/{term.replace(' ', '_')}" if definition else "",
            "source_license": LICENSE if definition else "",
            "retrieved_at": RETRIEVED if definition else None,
            "attribution_en": ATTR_EN if definition else "",
            "attribution_pl": ATTR_PL if definition else "",
        }
        if sentence and definition:
            row["attribution_en"] = clip(
                "English definition from Wiktionary contributors, CC BY-SA 4.0. "
                f"Example from Tatoeba #{sentence['id']} by {sentence['author']}, {sentence['license']}.",
                240,
            )
            row["attribution_pl"] = clip(
                "Angielska definicja: współtwórcy Wiktionary, CC BY-SA 4.0. "
                f"Przykład z Tatoeby #{sentence['id']}, autor: {sentence['author']}, {sentence['license']}.",
                240,
            )
        elif sentence:
            row["attribution_en"] = clip(
                f"Example from Tatoeba #{sentence['id']} by {sentence['author']}, {sentence['license']}.",
                240,
            )
            row["attribution_pl"] = clip(
                f"Przykład z Tatoeby #{sentence['id']}, autor: {sentence['author']}, {sentence['license']}.",
                240,
            )
            if not definition:
                row["content_source"] = "tatoeba"
                row["source_url"] = sentence["url"]
                row["source_license"] = sentence["license"]
                row["retrieved_at"] = RETRIEVED
        rows.append(row)
        print("word", level, term, "wiki" if definition else "-", "tatoeba" if sentence else "-")
    return rows


def taken_terms() -> set[str]:
    taken: set[str] = set()
    for name in ("original.json", "wiktionary.json"):
        for row in json.loads((ROOT / "vocabulary" / name).read_text(encoding="utf-8")):
            taken.add(row["term"])
    return taken


def main() -> None:
    planned = [term for words in WORDS.values() for term in words]
    if len(planned) != len(set(planned)):
        raise SystemExit("duplicate terms in the new level lists")
    overlap = set(planned) & taken_terms()
    if overlap:
        raise SystemExit(f"terms already in the level-2 catalog: {sorted(overlap)}")
    missing = [term for term in planned if term not in GLOSSES]
    if missing:
        raise SystemExit(f"missing Polish glosses: {missing}")
    cache = load_cache()
    manifest_exercises = [
        "exercises/listening.json",
        "exercises/reading.json",
        "exercises/speaking.json",
        "exercises/writing.json",
    ]
    manifest_vocab = ["vocabulary/original.json", "vocabulary/wiktionary.json"]
    for level, count in COUNTS.items():
        listening = listening_and_reading(level, "listening")
        reading = listening_and_reading(level, "reading")
        apply_wikipedia(level, reading)
        speaking = speaking_and_writing(level, "speaking")
        writing = speaking_and_writing(level, "writing")
        assert len(listening) == count
        paths = {
            f"exercises/level-{level}-listening.json": listening,
            f"exercises/level-{level}-reading.json": reading,
            f"exercises/level-{level}-speaking.json": speaking,
            f"exercises/level-{level}-writing.json": writing,
        }
        for relative, payload in paths.items():
            write_json(ROOT / relative, payload)
            manifest_exercises.append(relative)
        vocab_name = f"vocabulary/level-{level}.json"
        write_json(ROOT / vocab_name, vocabulary_for(level, cache))
        manifest_vocab.append(vocab_name)
    write_json(ROOT / "manifest.json", {"exercises": manifest_exercises, "vocabulary": manifest_vocab})
    print("levels written")


if __name__ == "__main__":
    main()
