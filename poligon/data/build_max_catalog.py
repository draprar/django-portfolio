"""Expand Poligon to 50 exercises per skill per level and 200 cards per level.

Offline only. Wikipedia, Wiktionary and Tatoeba are fetched into local caches.
A failed fetch keeps an original item. Production never runs this script.
"""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from build_catalog import ATTR_EN, ATTR_PL, LICENSE, RETRIEVED, _choose_definition, load_cache  # noqa: E402
from build_catalog import CACHE as WIKT_CACHE_PATH  # noqa: E402
from fetch_tatoeba import fetch_sentence  # noqa: E402
from fetch_tatoeba import load_cache as load_tatoeba_cache  # noqa: E402
from fetch_wikipedia import clip_at_sentence, fetch_summary  # noqa: E402
from fetch_wikipedia import load_cache as load_wiki_cache  # noqa: E402

PER_SKILL = 50
WIKI_QUOTA = {0: 0, 1: 35, 2: 25, 3: 40, 4: 45, 5: 45}
SKILLS = ("L", "R", "S", "W")
LEVEL2_FILES = {
    "L": "exercises/listening.json",
    "R": "exercises/reading.json",
    "S": "exercises/speaking.json",
    "W": "exercises/writing.json",
}


def topic_wrongs(index: int) -> list[tuple[str, str]]:
    wrongs = []
    for shift in (1, 2, 3):
        other = TOPICS[(index + shift) % len(TOPICS)]
        wrongs.append((f"It is about the {other[1]}.", f"Chodzi o: {other[2]}."))
    return wrongs


def wiki_wrongs(level: int, title: str) -> list[tuple[str, str]]:
    titles = [name for _wiki, name in CURRICULUM[level] if name != title]
    if not titles:
        return []
    start = 0
    for index, (_wiki, name) in enumerate(CURRICULUM[level]):
        if name == title:
            start = index
            break
    picked: list[tuple[str, str]] = []
    for offset in range(len(titles)):
        label = titles[(start + offset) % len(titles)].replace("_", " ").lower()
        pair = (f"It is about {label}.", f"Chodzi o: {label}.")
        if pair not in picked:
            picked.append(pair)
        if len(picked) == 3:
            break
    return picked


TOPICS = [
    ("apple", "apple", "jabłko", "food", "jedzenie"),
    ("ticket", "ticket office", "kasa", "travel", "podróż"),
    ("bridge", "bridge", "most", "movement", "przemieszczanie"),
    ("clinic", "clinic", "przychodnia", "health", "zdrowie"),
    ("office", "office", "biuro", "work", "praca"),
    ("market", "market", "targ", "town", "miasto"),
    ("river", "river", "rzeka", "place", "miejsce"),
    ("teacher", "teacher", "nauczyciel", "school", "szkoła"),
    ("engine", "engine", "silnik", "equipment", "sprzęt"),
    ("passport", "passport", "paszport", "travel", "podróż"),
    ("garden", "garden", "ogród", "home", "dom"),
    ("storm", "storm", "burza", "weather", "pogoda"),
    ("library", "library", "biblioteka", "town", "miasto"),
    ("salary", "salary", "pensja", "work", "praca"),
    ("vaccine", "vaccine", "szczepionka", "health", "zdrowie"),
    ("harbor", "harbor", "port", "movement", "przemieszczanie"),
    ("battery", "battery", "akumulator", "equipment", "sprzęt"),
    ("museum", "museum", "muzeum", "town", "miasto"),
    ("budget", "budget", "budżet", "work", "praca"),
    ("island", "island", "wyspa", "place", "miejsce"),
]

CURRICULUM: dict[int, list[tuple[str, str]]] = {
    1: [("simple", title) for title in [
        "Weather", "Breakfast", "Bus", "Hospital", "School", "City", "Family", "House", "Dog", "Cat",
        "Bird", "Tree", "River", "Mountain", "Beach", "Airport", "Bicycle", "Car", "Taxi", "Boat",
        "Computer", "Book", "Music", "Garden", "Kitchen", "Bread", "Apple", "Market", "Library", "Park",
        "Road", "Farm", "Horse", "Fish", "Clock", "Sun", "Moon", "Winter", "Summer", "Milk", "Shoe", "Hat",
    ]],
    2: [("en", title) for title in [
        "Coffee", "Tea", "Restaurant", "Newspaper", "Telephone", "Camera", "Electricity", "Agriculture",
        "University", "Museum", "Theatre", "Railway", "Factory", "Office", "Calendar", "Passport",
        "Luggage", "Traffic", "Pollution", "Recycling", "Vaccine", "Earthquake", "Volcano", "Climate",
        "Island", "Harbour", "Castle", "Church", "Village", "Bridge",
    ]],
    3: [("en", title) for title in [
        "Public_transport", "First_aid", "Democracy", "Constitution", "Inflation", "Unemployment",
        "Immigration", "Journalism", "Photography", "Architecture", "Engineering", "Mathematics",
        "Physics", "Chemistry", "Biology", "Geography", "History", "Philosophy", "Psychology",
        "Sociology", "Economics", "Accounting", "Marketing", "Insurance", "Banking", "Taxation",
        "Copyright", "Patent", "Contract", "Negotiation", "Leadership", "Teamwork", "Productivity",
        "Inventory", "Customer_service", "Quality_control", "Project_management", "Risk_management",
        "Time_management", "Public_health", "Nutrition", "Sleep", "Vaccination", "Antibiotic", "Exercise",
    ]],
    4: [("en", title) for title in [
        "Logistics", "Navigation", "Epidemiology", "Statistics", "Probability", "Algorithm", "Database",
        "Computer_network", "Renewable_energy", "Occupational_safety_and_health", "Emergency_management",
        "Meteorology", "Geology", "Astronomy", "Ecology", "Biodiversity", "Climate_change", "Sustainability",
        "Urban_planning", "Transportation", "Telecommunications", "Diplomacy", "Treaty", "International_law",
        "Human_rights", "Census", "Budget", "Monetary_policy", "Fiscal_policy", "International_trade",
        "Comparative_advantage", "Opportunity_cost", "Game_theory", "Cryptography", "Machine_learning",
        "Artificial_intelligence", "Robotics", "Automation", "Supply_chain", "Quality_assurance",
        "Seismology", "Hydrology", "Oceanography", "Paleontology", "Botany", "Climatology", "Genetics",
        "Neuroscience", "Thermodynamics", "Electromagnetism",
    ]],
    5: [("en", title) for title in [
        "Ethics", "Aesthetics", "Epistemology", "Metaphysics", "Logic", "Rhetoric", "Semantics",
        "Pragmatics", "Linguistics", "Translation", "Archaeology", "Anthropology", "Demography",
        "Macroeconomics", "Microeconomics", "Behavioral_economics", "Jurisprudence", "Constitutional_law",
        "Criminal_law", "Civil_law", "Cognitive_science", "Immunology", "Evolution", "Plate_tectonics",
        "Quantum_mechanics", "Relativity", "Optics", "Acoustics", "Volcanology", "Zoology", "Microbiology",
        "Pharmacology", "Toxicology", "Historiography", "Public_finance", "Central_bank", "Development_economics",
        "Evidence", "Tort", "Logic_gate", "Semiotics", "Hermeneutics", "Ontology", "Phenomenology",
        "Stoicism", "Utilitarianism", "Existentialism", "Rationalism", "Empiricism", "Pragmatism",
    ]],
}


def clip(text: str, limit: int) -> str:
    return clip_at_sentence(text, limit)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def skill_path(level: int, skill: str) -> Path:
    if level == 2:
        relative = LEVEL2_FILES[skill]
    else:
        names = {"L": "listening", "R": "reading", "S": "speaking", "W": "writing"}
        relative = f"exercises/level-{level}-{names[skill]}.json"
    return ROOT / relative


def protected(slug: str) -> bool:
    return slug.startswith(("listen-", "read-", "speak-", "write-"))


def options(correct: tuple[str, str], wrongs: list[tuple[str, str]]) -> list[dict]:
    rows = [{"text_en": correct[0], "text_pl": correct[1], "is_correct": True}]
    rows.extend({"text_en": en, "text_pl": pl, "is_correct": False} for en, pl in wrongs)
    return rows


def blank_provenance() -> dict:
    return {
        "original_content": True,
        "source_note": "Original Poligon text",
        "content_source": "original",
        "source_url": "",
        "source_license": "",
        "retrieved_at": None,
        "attribution_en": "",
        "attribution_pl": "",
    }


def make_original(level: int, skill: str, index: int, used: set[str]) -> dict:
    key, word_en, word_pl, cat_en, cat_pl = TOPICS[index % len(TOPICS)]
    slug = f"l{level}-{skill.lower()}-x{index:03d}-{key}"
    bump = index
    while slug in used:
        bump += 1
        slug = f"l{level}-{skill.lower()}-x{bump:03d}-{key}"
    used.add(slug)
    exercise_type = {"L": "listening", "R": "mcq", "S": "speaking", "W": "writing"}[skill]
    row = {
        "slug": slug,
        "skill": skill,
        "level": level,
        "exercise_type": exercise_type,
        "expected_minutes": 8 if skill in {"S", "W"} else 6,
        "category_en": cat_en,
        "category_pl": cat_pl,
        "content_en": "",
        "content_pl": "",
        **blank_provenance(),
    }
    if skill == "L":
        row["title_en"] = f"Hear the note: {word_en}"
        row["title_pl"] = f"Usłysz notatkę: {word_pl}"
        row["instructions_en"] = "Listen once and choose the best answer."
        row["instructions_pl"] = "Posłuchaj raz i wybierz najlepszą odpowiedź."
        row["prompt_en"] = "What is the note about?"
        row["prompt_pl"] = "O czym jest notatka?"
        row["content_en"] = f"The {word_en} is ready at seven. Tell the shift leader if it is late."
        row["content_pl"] = f"{word_pl[:1].upper()}{word_pl[1:]} jest gotowe o siódmej. Powiedz dowódcy zmiany, jeśli to się spóźnia."
        row["options"] = options(
            (f"It is about the {word_en}.", f"Chodzi o: {word_pl}."),
            topic_wrongs(index),
        )
    elif skill == "R":
        row["title_en"] = f"Read the note: {word_en}"
        row["title_pl"] = f"Przeczytaj notatkę: {word_pl}"
        row["instructions_en"] = "Read the note and choose the best answer."
        row["instructions_pl"] = "Przeczytaj notatkę i wybierz najlepszą odpowiedź."
        row["prompt_en"] = (
            f"The team cannot start until the {word_en} is confirmed. "
            "If it is late, use the backup and tell the shift leader."
        )
        row["prompt_pl"] = (
            f"Zespół nie zaczyna, dopóki nie ma potwierdzenia: {word_pl}. "
            "Jeśli to się spóźnia, użyj zapasu i powiedz dowódcy zmiany."
        )
        row["options"] = options(
            (f"It is about the {word_en}.", f"Chodzi o: {word_pl}."),
            topic_wrongs(index),
        )
    elif skill == "S":
        row["title_en"] = f"Say something about {word_en}"
        row["title_pl"] = f"Powiedz coś o: {word_pl}"
        row["instructions_en"] = "Speak in English. The heuristic scores English."
        row["instructions_pl"] = "Mów po angielsku. Heurystyka ocenia angielski."
        row["prompt_en"] = (
            f"In a few connected sentences, explain when you need {word_en} and what you do if it is missing."
        )
        row["prompt_pl"] = (
            f"W kilku powiązanych zdaniach wyjaśnij, kiedy potrzebujesz: {word_pl}, i co robisz, gdy tego brakuje."
        )
        row["source_note"] = "Original Poligon prompt"
    else:
        row["title_en"] = f"Write about {word_en}"
        row["title_pl"] = f"Napisz o: {word_pl}"
        row["instructions_en"] = "Write in English. The heuristic scores English."
        row["instructions_pl"] = "Pisz po angielsku. Heurystyka ocenia angielski."
        row["prompt_en"] = f"Write a short note. Mention {word_en}, one time, and one person who should confirm it."
        row["prompt_pl"] = f"Napisz krótką notatkę. Wspomnij: {word_pl}, jedną godzinę i jedną osobę, która ma to potwierdzić."
        row["source_note"] = "Original Poligon prompt"
    if level >= 4 and skill in {"S", "W"}:
        row["prompt_en"] += " Give a reason and a backup plan."
        row["prompt_pl"] += " Podaj powód i plan zastępczy."
    return row


def apply_wiki(row: dict, summary: dict, title: str) -> None:
    nice = summary["title"]
    row["title_en"] = nice
    row["title_pl"] = nice
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
    row["content_en"] = ""
    row["content_pl"] = ""
    row["attribution_en"] = clip(
        f"Shortened English text from the Wikipedia article “{nice}”, CC BY-SA 4.0. Question and choices are original.",
        300,
    )
    row["attribution_pl"] = clip(
        f"Skrócony angielski tekst z artykułu Wikipedii „{nice}”, CC BY-SA 4.0. Pytanie i odpowiedzi są oryginalne.",
        300,
    )
    choice = (f"It is about {title.replace('_', ' ').lower()}.", f"Chodzi o: {title.replace('_', ' ').lower()}.")
    row["options"] = options(choice, wiki_wrongs(row["level"], title))


def expand_exercises(wiki_cache: dict) -> int:
    wiki_count = 0
    used: set[str] = set()
    for level in range(6):
        for skill in SKILLS:
            path = skill_path(level, skill)
            rows = json.loads(path.read_text(encoding="utf-8"))
            for row in rows:
                used.add(row["slug"])
                row.setdefault("content_source", "original")
                row.setdefault("source_url", "")
                row.setdefault("source_license", "")
                row.setdefault("retrieved_at", None)
                row.setdefault("attribution_en", "")
                row.setdefault("attribution_pl", "")
            index = 0
            while len(rows) < PER_SKILL:
                rows.append(make_original(level, skill, index, used))
                index += 1
            if skill == "R" and WIKI_QUOTA[level]:
                have = sum(1 for row in rows if row.get("content_source") == "wikipedia")
                need = WIKI_QUOTA[level] - have
                candidates = [
                    row
                    for row in reversed(rows)
                    if row.get("content_source", "original") == "original" and not protected(row["slug"])
                ]
                for wiki, title in CURRICULUM[level]:
                    if need <= 0 or not candidates:
                        break
                    summary = fetch_summary(title, wiki=wiki, cache=wiki_cache)
                    time.sleep(0.45)
                    if not summary:
                        print("wiki skip", wiki, title)
                        continue
                    apply_wiki(candidates.pop(), summary, title)
                    need -= 1
                    print("wiki", level, title)
            wiki_count += sum(1 for row in rows if row.get("content_source") == "wikipedia")
            if len(rows) != PER_SKILL:
                raise SystemExit(f"{path.name} has {len(rows)} rows")
            write_json(path, rows)
    return wiki_count


def fetch_definition_fast(term: str, cache: dict[str, str]) -> str:
    if term in cache:
        return cache[term]
    slug = urllib.parse.quote(term.replace(" ", "_"))
    url = f"https://en.wiktionary.org/api/rest_v1/page/definition/{slug}"
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "PoligonPortfolio/1.0 (study catalog; one-shot build)"},
    )
    payload = None
    for attempt in range(6):
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                payload = json.load(response)
            break
        except urllib.error.HTTPError as exc:
            if exc.code == 429:
                time.sleep(6 + attempt * 3)
                continue
            if exc.code == 404:
                cache[term] = ""
                WIKT_CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                return ""
            raise
    if payload is None:
        cache[term] = ""
        return ""
    text = _choose_definition(payload)
    cache[term] = text
    WIKT_CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    time.sleep(0.35)
    return text


def load_vocab() -> dict[int, list[dict]]:
    by_level: dict[int, list[dict]] = {level: [] for level in range(6)}
    files = [ROOT / "vocabulary" / "original.json", ROOT / "vocabulary" / "wiktionary.json"]
    files.extend(ROOT / "vocabulary" / f"level-{level}.json" for level in (0, 1, 3, 4, 5))
    level2_extra = ROOT / "vocabulary" / "level-2.json"
    if level2_extra.exists():
        files.append(level2_extra)
    seen: set[str] = set()
    for path in files:
        if not path.exists():
            continue
        for row in json.loads(path.read_text(encoding="utf-8")):
            if row["term"].lower() in seen:
                continue
            seen.add(row["term"].lower())
            by_level[int(row["level"])].append(row)
    return by_level


def card_for(level: int, term: str, gloss: str, definition: str, sentence: dict | None) -> dict:
    row = {
        "term": term,
        "translation": gloss,
        "explanation_en": definition or f"A useful word at this practice level: {term}.",
        "explanation_pl": "",
        "example_en": sentence["text"] if sentence else f"Please check the {term} before you leave.",
        "example_pl": f"Sprawdź proszę ({gloss}), zanim wyjdziesz.",
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
        row["content_source"] = "tatoeba"
        row["source_url"] = sentence["url"]
        row["source_license"] = sentence["license"]
        row["retrieved_at"] = RETRIEVED
        row["attribution_en"] = clip(
            f"Example from Tatoeba #{sentence['id']} by {sentence['author']}, {sentence['license']}.",
            240,
        )
        row["attribution_pl"] = clip(
            f"Przykład z Tatoeby #{sentence['id']}, autor: {sentence['author']}, {sentence['license']}.",
            240,
        )
    return row


def expand_vocabulary(wikt_cache: dict[str, str], tatoeba_cache: dict) -> None:
    by_level = load_vocab()
    taken = {row["term"].lower() for rows in by_level.values() for row in rows}
    for level in range(6):
        supply = []
        for line in (ROOT / "wordlists" / f"level-{level}.txt").read_text(encoding="utf-8").splitlines():
            if not line.strip() or "\t" not in line:
                continue
            term, gloss = line.split("\t", 1)
            if term.lower() in taken:
                continue
            supply.append((term, gloss))
        added = 0
        while len(by_level[level]) < 200 and supply:
            term, gloss = supply.pop(0)
            if term.lower() in taken:
                continue
            try:
                definition = fetch_definition_fast(term, wikt_cache)
            except Exception as exc:  # noqa: BLE001
                print("dict skip", term, exc)
                definition = ""
            sentence = None
            try:
                sentence = fetch_sentence(term, tatoeba_cache)
                if term not in tatoeba_cache:
                    time.sleep(0.2)
            except Exception as exc:  # noqa: BLE001
                print("tatoeba skip", term, exc)
                tatoeba_cache[term] = None
            by_level[level].append(card_for(level, term, gloss, definition, sentence))
            taken.add(term.lower())
            added += 1
            if added % 20 == 0:
                print("vocab", level, added, "of", 200 - (len(by_level[level]) - added))
        if len(by_level[level]) != 200:
            raise SystemExit(f"level {level} vocabulary has {len(by_level[level])}")
        print("vocab level", level, "done", added, "new")
    base_terms = set()
    for name in ("original.json", "wiktionary.json"):
        for row in json.loads((ROOT / "vocabulary" / name).read_text(encoding="utf-8")):
            base_terms.add(row["term"].lower())
    for level in (0, 1, 3, 4, 5):
        write_json(ROOT / "vocabulary" / f"level-{level}.json", by_level[level])
    extra = [row for row in by_level[2] if row["term"].lower() not in base_terms]
    write_json(ROOT / "vocabulary" / "level-2.json", extra)


def write_curriculum() -> None:
    rows = []
    for level, items in CURRICULUM.items():
        for wiki, title in items:
            rows.append({"level": level, "wiki": wiki, "title": title})
    write_json(ROOT / "wiki_curriculum.json", rows)


def write_manifest() -> None:
    exercises = [LEVEL2_FILES[skill] for skill in SKILLS]
    for level in (0, 1, 3, 4, 5):
        for skill in SKILLS:
            exercises.append(str(skill_path(level, skill).relative_to(ROOT)).replace("\\", "/"))
    vocabulary = [
        "vocabulary/original.json",
        "vocabulary/wiktionary.json",
        "vocabulary/level-0.json",
        "vocabulary/level-1.json",
        "vocabulary/level-2.json",
        "vocabulary/level-3.json",
        "vocabulary/level-4.json",
        "vocabulary/level-5.json",
    ]
    write_json(ROOT / "manifest.json", {"exercises": exercises, "vocabulary": vocabulary})


def main() -> None:
    titles = [title for items in CURRICULUM.values() for _wiki, title in items]
    if len(titles) != len(set(titles)):
        raise SystemExit("duplicate wikipedia titles")
    write_curriculum()
    wiki_cache = load_wiki_cache()
    wiki_count = expand_exercises(wiki_cache)
    print("wikipedia exercises", wiki_count)
    if wiki_count < 180:
        raise SystemExit(f"only {wiki_count} wikipedia exercises; fix titles before the vocabulary fetch")
    expand_vocabulary(load_cache(), load_tatoeba_cache())
    write_manifest()
    print("catalog max written")


if __name__ == "__main__":
    main()
