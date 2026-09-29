"""One-shot catalog builder. Run from the repo root, then commit the JSON it writes.

Fetches short English definitions from the public Wiktionary REST API and stores
them with CC BY-SA attribution. Polish glosses and example sentences in this file
are original.
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEMO = ROOT / "demo_content.json"
RETRIEVED = "2026-09-26"
LICENSE = "CC BY-SA 4.0"
ATTR_EN = "English definition from Wiktionary contributors, CC BY-SA 4.0. Examples are original."
ATTR_PL = "Angielska definicja: współtwórcy Wiktionary, CC BY-SA 4.0. Przykłady są oryginalne."

# term, polish gloss, category_en, category_pl, example_en, example_pl
TERMS: list[tuple[str, str, str, str, str, str]] = [
    ("convoy", "kolumna", "movement", "przemieszczanie", "The convoy left after the equipment check.", "Kolumna ruszyła po sprawdzeniu wyposażenia."),
    ("patrol", "patrol", "operations", "działania", "The patrol returned before dark.", "Patrol wrócił przed zmrokiem."),
    ("sentry", "wartownik", "operations", "działania", "The sentry checked every identification card.", "Wartownik sprawdził każdy identyfikator."),
    ("reconnaissance", "rozpoznanie", "operations", "działania", "Reconnaissance confirmed the bridge was open.", "Rozpoznanie potwierdziło, że most jest otwarty."),
    ("mission", "zadanie", "operations", "działania", "The mission starts at dawn.", "Zadanie zaczyna się o świcie."),
    ("objective", "cel", "operations", "działania", "The objective is the northern gate.", "Celem jest brama północna."),
    ("headquarters", "sztab", "command", "dowodzenie", "Report the delay to headquarters.", "Zgłoś opóźnienie do sztabu."),
    ("platoon", "pluton", "command", "dowodzenie", "The platoon assembled at the vehicle park.", "Pluton zebrał się w parku pojazdów."),
    ("company", "kompania", "command", "dowodzenie", "The company moved to a new training area.", "Kompania przeniosła się na nowy plac ćwiczeń."),
    ("battalion", "batalion", "command", "dowodzenie", "The battalion issued a new timetable.", "Batalion wydał nowy harmonogram."),
    ("commander", "dowódca", "command", "dowodzenie", "The commander changed the meeting time.", "Dowódca zmienił godzinę spotkania."),
    ("soldier", "żołnierz", "personnel", "personel", "Each soldier brought a map and a radio.", "Każdy żołnierz zabrał mapę i radiostację."),
    ("formation", "szyk", "operations", "działania", "The formation stayed together on the main road.", "Szyk trzymał się razem na głównej drodze."),
    ("advance", "natarcie / posuwanie się", "operations", "działania", "The advance stopped at the river.", "Posuwanie się zatrzymało się nad rzeką."),
    ("withdrawal", "wycofanie", "operations", "działania", "The withdrawal used the western access road.", "Wycofanie szło zachodnią drogą dojazdową."),
    ("cover", "osłona", "operations", "działania", "The trees gave the group cover from the wind.", "Drzewa dały grupie osłonę przed wiatrem."),
    ("concealment", "maskowanie", "operations", "działania", "Concealment kept the vehicles out of sight.", "Maskowanie ukryło pojazdy przed wzrokiem."),
    ("ammunition", "amunicja", "logistics", "logistyka", "Ammunition arrives after the safety inspection.", "Amunicja przyjeżdża po kontroli bezpieczeństwa."),
    ("rations", "racje żywnościowe", "logistics", "logistyka", "Hot rations will be ready at noon.", "Ciepłe racje będą gotowe w południe."),
    ("canteen", "manierka", "equipment", "sprzęt", "Fill your canteen before the march.", "Napełnij manierkę przed marszem."),
    ("warehouse", "magazyn", "logistics", "logistyka", "The spare battery is in the warehouse.", "Zapasowy akumulator jest w magazynie."),
    ("inventory", "inwentarz", "logistics", "logistyka", "Update the inventory after the delivery.", "Zaktualizuj inwentarz po dostawie."),
    ("shipment", "przesyłka", "logistics", "logistyka", "The shipment of fuel is late.", "Przesyłka paliwa jest spóźniona."),
    ("pallet", "paleta", "logistics", "logistyka", "Leave the pallet beside the workshop.", "Zostaw paletę obok warsztatu."),
    ("crate", "skrzynia", "logistics", "logistyka", "The crate contains radio batteries.", "W skrzyni są baterie do radiostacji."),
    ("rifle", "karabin", "equipment", "sprzęt", "Clean the rifle before the inspection.", "Wyczyść karabin przed kontrolą."),
    ("helmet", "hełm", "equipment", "sprzęt", "Wear a helmet inside the vehicle park.", "Noś hełm na terenie parku pojazdów."),
    ("uniform", "mundur", "equipment", "sprzęt", "The new uniform arrives on Friday.", "Nowy mundur przyjeżdża w piątek."),
    ("compass", "kompas", "equipment", "sprzęt", "Check the compass against the map.", "Sprawdź kompas z mapą."),
    ("radio", "radiostacja", "communications", "łączność", "The radio check starts at eight.", "Sprawdzenie radiostacji zaczyna się o ósmej."),
    ("binoculars", "lornetka", "equipment", "sprzęt", "Use binoculars to confirm the landmark.", "Użyj lornetki, żeby potwierdzić punkt orientacyjny."),
    ("flashlight", "latarka", "equipment", "sprzęt", "Bring a flashlight for the night march.", "Weź latarkę na nocny marsz."),
    ("tent", "namiot", "equipment", "sprzęt", "The tent will be pitched by the tree line.", "Namiot stanie przy linii drzew."),
    ("stretcher", "nosze", "medical", "medycyna", "The stretcher is stored in the medical tent.", "Nosze leżą w namiocie medycznym."),
    ("bridge", "most", "movement", "przemieszczanie", "The bridge is open only to light vehicles.", "Most jest otwarty tylko dla lekkich pojazdów."),
    ("terrain", "teren", "movement", "przemieszczanie", "The terrain is soft after the rain.", "Teren jest miękki po deszczu."),
    ("coordinate", "współrzędna", "movement", "przemieszczanie", "Read the coordinate twice before you move.", "Odczytaj współrzędną dwa razy, zanim ruszysz."),
    ("landmark", "punkt orientacyjny", "movement", "przemieszczanie", "The tower is the landmark for the turn.", "Wieża jest punktem orientacyjnym do skrętu."),
    ("march", "marsz", "movement", "przemieszczanie", "The march begins after roll call.", "Marsz zaczyna się po apelu."),
    ("halt", "postój", "movement", "przemieszczanie", "The halt lasts ten minutes.", "Postój trwa dziesięć minut."),
    ("assembly", "zbiórka", "movement", "przemieszczanie", "Assembly is at the main gate.", "Zbiórka jest przy głównej bramie."),
    ("roster", "grafik dyżurów", "procedures", "procedury", "Check the roster before you leave.", "Sprawdź grafik, zanim wyjdziesz."),
    ("password", "hasło", "procedures", "procedury", "Give the password at the checkpoint.", "Podaj hasło na punkcie kontrolnym."),
    ("clearance", "zezwolenie", "procedures", "procedury", "You need clearance to enter the workshop.", "Do warsztatu potrzebne jest zezwolenie."),
    ("permit", "przepustka", "procedures", "procedury", "Show your permit to the sentry.", "Pokaż przepustkę wartownikowi."),
    ("curfew", "godzina policyjna", "procedures", "procedury", "Curfew starts at twenty-two hundred.", "Godzina policyjna zaczyna się o dwudziestej drugiej."),
    ("colleague", "kolega z zespołu", "workplace", "praca", "Ask a colleague to confirm the new time.", "Poproś kolegę o potwierdzenie nowej godziny."),
    ("agenda", "porządek spotkania", "workplace", "praca", "The agenda has three short points.", "Porządek spotkania ma trzy krótkie punkty."),
    ("deadline", "termin", "workplace", "praca", "The deadline for the report is Friday.", "Termin raportu to piątek."),
    ("schedule", "harmonogram", "workplace", "praca", "The schedule moved the meeting to the afternoon.", "Harmonogram przeniósł spotkanie na popołudnie."),
    ("forecast", "prognoza", "workplace", "praca", "The forecast says the rain will stop by noon.", "Prognoza mówi, że deszcz ustanie do południa."),
    ("frequency", "częstotliwość", "communications", "łączność", "Stay on the assigned frequency.", "Zostań na przydzielonej częstotliwości."),
    ("signal", "sygnał", "communications", "łączność", "Wait for the signal before you cross.", "Poczekaj na sygnał, zanim przejdziesz."),
    ("message", "wiadomość", "communications", "łączność", "Pass the message to the driver.", "Przekaż wiadomość kierowcy."),
    ("channel", "kanał", "communications", "łączność", "Switch to the backup channel.", "Przełącz się na kanał zapasowy."),
    ("call sign", "kryptonim", "communications", "łączność", "Use your call sign at the start of the call.", "Użyj kryptonimu na początku rozmowy."),
    ("hazard", "zagrożenie", "safety", "bezpieczeństwo", "Mark the hazard before the convoy arrives.", "Oznacz zagrożenie, zanim przyjedzie kolumna."),
    ("casualty", "poszkodowany", "medical", "medycyna", "Report a casualty to the medical team.", "Zgłoś poszkodowanego zespołowi medycznemu."),
    ("evacuation", "ewakuacja", "safety", "bezpieczeństwo", "The evacuation route is the western road.", "Droga ewakuacji to droga zachodnia."),
    ("alarm", "alarm", "safety", "bezpieczeństwo", "The alarm means everyone stops work.", "Alarm oznacza, że wszyscy przerywają pracę."),
    ("drill", "alarm ćwiczebny", "training", "szkolenie", "The fire drill is at ten hundred.", "Alarm pożarowy jest o dziesiątej."),
    ("visibility", "widoczność", "weather", "pogoda", "Visibility is poor because of fog.", "Widoczność jest słaba przez mgłę."),
    ("temperature", "temperatura", "weather", "pogoda", "The temperature will fall after sunset.", "Temperatura spadnie po zachodzie słońca."),
    ("driver", "kierowca", "movement", "przemieszczanie", "The driver confirmed the destination.", "Kierowca potwierdził cel jazdy."),
    ("passenger", "pasażer", "movement", "przemieszczanie", "Every passenger must wear a seat belt.", "Każdy pasażer musi mieć pas."),
    ("bunker", "schron", "facilities", "obiekty", "The bunker is the meeting point in bad weather.", "Schron jest miejscem zbiórki przy złej pogodzie."),
    ("trench", "okop", "facilities", "obiekty", "Stay clear of the trench at night.", "Omijaj okop w nocy."),
    ("camouflage", "kamuflaż", "equipment", "sprzęt", "Camouflage nets cover the parked trucks.", "Siatki maskujące przykrywają zaparkowane ciężarówki."),
    ("maneuver", "manewr", "training", "szkolenie", "The maneuver ends at the assembly area.", "Manewr kończy się w rejonie zbiórki."),
    ("order", "rozkaz", "command", "dowodzenie", "The order is to wait for fuel.", "Rozkaz każe czekać na paliwo."),
    ("map", "mapa", "movement", "przemieszczanie", "Fold the map so the route stays visible.", "Złóż mapę tak, żeby trasa była widoczna."),
    ("gate", "brama", "facilities", "obiekty", "The gate closes at eighteen hundred.", "Brama zamyka się o osiemnastej."),
    ("guard", "warta", "operations", "działania", "The guard changes every two hours.", "Warta zmienia się co dwie godziny."),
    ("weapon", "broń", "equipment", "sprzęt", "Store the weapon in the assigned rack.", "Odłóż broń na wyznaczony stojak."),
    ("battery", "akumulator", "equipment", "sprzęt", "Replace the battery before the radio check.", "Wymień akumulator przed sprawdzeniem radiostacji."),
    ("spare", "część zapasowa", "logistics", "logistyka", "A spare tyre is in the second truck.", "Zapasowa opona jest w drugiej ciężarówce."),
    ("vehicle", "pojazd", "movement", "przemieszczanie", "The vehicle returns to service on Friday.", "Pojazd wraca do służby w piątek."),
    ("fuel", "paliwo", "logistics", "logistyka", "Fuel arrives thirty minutes after the water.", "Paliwo przyjeżdża trzydzieści minut po wodzie."),
    ("delay", "opóźnienie", "workplace", "praca", "Explain the delay in one sentence.", "Wyjaśnij opóźnienie w jednym zdaniu."),
    ("report", "meldunek", "communications", "łączność", "Send the report before you leave the site.", "Wyślij meldunek, zanim opuścisz plac."),
    ("update", "aktualizacja", "communications", "łączność", "The update says the road is open.", "Aktualizacja mówi, że droga jest otwarta."),
    ("meeting", "spotkanie", "workplace", "praca", "The meeting moved to Tuesday afternoon.", "Spotkanie przeniosło się na wtorkowe popołudnie."),
    ("confirmation", "potwierdzenie", "workplace", "praca", "I need your confirmation by email.", "Potrzebuję twojego potwierdzenia mailem."),
    ("request", "prośba", "workplace", "praca", "The request for extra tents was approved.", "Prośba o dodatkowe namioty została zatwierdzona."),
    ("document", "dokument", "procedures", "procedury", "Bring the document to the main gate.", "Przynieś dokument do głównej bramy."),
    ("equipment", "wyposażenie", "equipment", "sprzęt", "Check the equipment before the convoy leaves.", "Sprawdź wyposażenie, zanim kolumna ruszy."),
    ("safety", "bezpieczeństwo", "safety", "bezpieczeństwo", "Safety rules apply on the training area.", "Na placu ćwiczeń obowiązują zasady bezpieczeństwa."),
    ("weather", "pogoda", "weather", "pogoda", "Bad weather moved the class indoors.", "Zła pogoda przeniosła zajęcia do środka."),
    ("rain", "deszcz", "weather", "pogoda", "The rain delayed the outdoor lesson.", "Deszcz opóźnił zajęcia na zewnątrz."),
    ("fog", "mgła", "weather", "pogoda", "Fog reduced visibility on the access road.", "Mgła zmniejszyła widoczność na drodze dojazdowej."),
    ("wind", "wiatr", "weather", "pogoda", "Strong wind makes the tent unsafe.", "Silny wiatr sprawia, że namiot jest niebezpieczny."),
    ("sunset", "zachód słońca", "weather", "pogoda", "Finish the march before sunset.", "Skończ marsz przed zachodem słońca."),
    ("dawn", "świt", "weather", "pogoda", "The first group leaves at dawn.", "Pierwsza grupa rusza o świcie."),
    ("noon", "południe", "workplace", "praca", "Lunch is served at noon.", "Obiad jest wydawany w południe."),
    ("shift", "zmiana", "workplace", "praca", "The night shift starts at twenty hundred.", "Zmiana nocna zaczyna się o dwudziestej."),
    ("sergeant", "sierżant", "command", "dowodzenie", "Tell the sergeant if you will be late.", "Powiedz sierżantowi, jeśli się spóźnisz."),
    ("tool", "narzędzie", "equipment", "sprzęt", "Return each tool to the workshop.", "Oddaj każde narzędzie do warsztatu."),
    ("workshop", "warsztat", "facilities", "obiekty", "The workshop opens at seven.", "Warsztat otwiera się o siódmej."),
    ("tyre", "opona", "equipment", "sprzęt", "The tyre needs a simple repair.", "Opona wymaga prostej naprawy."),
    ("engine", "silnik", "equipment", "sprzęt", "The engine starts after the battery change.", "Silnik odpala po wymianie akumulatora."),
    ("licence", "uprawnienie", "procedures", "procedury", "Bring your licence to the gate.", "Weź uprawnienie do bramy."),
    ("seat belt", "pas bezpieczeństwa", "safety", "bezpieczeństwo", "Fasten the seat belt before the vehicle moves.", "Zapnij pas, zanim pojazd ruszy."),
    ("first aid", "pierwsza pomoc", "medical", "medycyna", "The first aid kit is in the lead vehicle.", "Apteczka jest w pierwszym pojeździe."),
    ("medic", "sanitariusz", "medical", "medycyna", "Call the medic if someone feels unwell.", "Wezwij sanitariusza, jeśli ktoś źle się czuje."),
    ("water", "woda", "logistics", "logistyka", "Water is the first delivery of the morning.", "Woda jest pierwszą dostawą rano."),
    ("food", "żywność", "logistics", "logistyka", "Food for the night shift is already packed.", "Jedzenie dla zmiany nocnej jest już spakowane."),
    ("rope", "lina", "equipment", "sprzęt", "Check the rope after the wind.", "Sprawdź linę po wietrze."),
    ("signature", "podpis", "procedures", "procedury", "Your signature confirms you received the message.", "Podpis potwierdza, że odebrałeś wiadomość."),
]


def strip_html(value: str) -> str:
    text = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", " ", text).strip()


CACHE = ROOT / "_wiktionary_cache_v2.json"


def _choose_definition(payload: dict) -> str:
    scored: list[tuple[int, str]] = []
    for block in payload.get("en", []):
        noun = str(block.get("partOfSpeech", "")).lower() == "noun"
        for item in block.get("definitions", []):
            cleaned = strip_html(item.get("definition", ""))
            if len(cleaned) < 12:
                continue
            lowered = cleaned.lower()
            if "obsolete" in lowered or "archaic" in lowered:
                continue
            score = 0
            if noun:
                score += 3
            for hint in ("vehicle", "person", "people", "group", "road", "work", "equipment"):
                if hint in lowered:
                    score += 2
            if "merchant ship" in lowered or "nautical" in lowered:
                score -= 4
            scored.append((score, cleaned[:480]))
    if not scored:
        return ""
    scored.sort(key=lambda row: (-row[0], len(row[1])))
    return scored[0][1]


def load_cache() -> dict[str, str]:
    if not CACHE.exists():
        return {}
    return json.loads(CACHE.read_text(encoding="utf-8"))


def fetch_definition(term: str, cache: dict[str, str]) -> str:
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
                time.sleep(8 + attempt * 4)
                continue
            if exc.code == 404:
                return ""
            raise
    if payload is None:
        raise SystemExit(f"rate limited while fetching {term}")
    text = _choose_definition(payload)
    cache[term] = text
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    time.sleep(1.2)
    return text


def load_existing() -> dict:
    return json.loads(DEMO.read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def split_exercises() -> None:
    from extra_exercises import all_extra

    by_skill: dict[str, list[dict]] = {"L": [], "S": [], "R": [], "W": []}
    for row in load_existing()["exercises"] + all_extra():
        by_skill[row["skill"]].append(row)
    names = {"L": "listening.json", "R": "reading.json", "S": "speaking.json", "W": "writing.json"}
    for skill, rows in by_skill.items():
        if len(rows) != 20:
            raise SystemExit(f"{skill} has {len(rows)} exercises, expected 20")
        write_json(ROOT / "exercises" / names[skill], rows)
        print(skill, len(rows))


def original_vocabulary() -> list[dict]:
    rows = []
    for raw in load_existing()["vocabulary"]:
        row = dict(raw)
        row.update(
            {
                "content_source": "original",
                "source_url": "",
                "source_license": "",
                "retrieved_at": None,
                "attribution_en": "",
                "attribution_pl": "",
            }
        )
        rows.append(row)
    return rows


def wiktionary_vocabulary() -> list[dict]:
    cache = load_cache()
    rows = []
    for term, translation, cat_en, cat_pl, example_en, example_pl in TERMS:
        definition = fetch_definition(term, cache)
        if not definition:
            raise SystemExit(f"no Wiktionary definition for {term!r}")
        page = urllib.parse.quote(term.replace(" ", "_"))
        rows.append(
            {
                "term": term,
                "translation": translation,
                "explanation_en": definition,
                "explanation_pl": "",
                "example_en": example_en,
                "example_pl": example_pl,
                "category_en": cat_en,
                "category_pl": cat_pl,
                "level": 2,
                "content_source": "wiktionary",
                "source_url": f"https://en.wiktionary.org/wiki/{page}",
                "source_license": LICENSE,
                "retrieved_at": RETRIEVED,
                "attribution_en": ATTR_EN,
                "attribution_pl": ATTR_PL,
            }
        )
        print("wiki", term)
    return rows


def main() -> None:
    if len(TERMS) != 108:
        raise SystemExit(f"expected 108 terms, got {len(TERMS)}")
    if len({term for term, *_rest in TERMS}) != 108:
        raise SystemExit("duplicate terms")
    split_exercises()
    original = original_vocabulary()
    wiki = wiktionary_vocabulary()
    write_json(ROOT / "vocabulary" / "original.json", original)
    write_json(ROOT / "vocabulary" / "wiktionary.json", wiki)
    write_json(
        ROOT / "manifest.json",
        {
            "exercises": [
                "exercises/listening.json",
                "exercises/reading.json",
                "exercises/speaking.json",
                "exercises/writing.json",
            ],
            "vocabulary": ["vocabulary/original.json", "vocabulary/wiktionary.json"],
        },
    )
    print("catalog", 80, len(original) + len(wiki))


if __name__ == "__main__":
    main()
