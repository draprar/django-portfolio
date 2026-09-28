"""Reference sheets shown next to the exercises.

Nothing here is graded, scored or stored. On duty these three things trip people
up long before grammar does: spelling a call sign, catching a number on the
radio, and asking the other side to say it again.

A cell is either English material the interface must leave alone, or a label
the PL/EN switch may translate.
"""

from __future__ import annotations


def _english(text: str) -> dict:
    """English material. The language switch never rewrites it."""
    return {"text": text, "english_only": True}


def _label(en: str, pl: str) -> dict:
    return {"en": en, "pl": pl, "english_only": False}


ALPHABET = [
    ("A", "Alpha", "AL-fah", "AL-fa"),
    ("B", "Bravo", "BRAH-voh", "BRA-wo"),
    ("C", "Charlie", "CHAR-lee", "CZAR-li"),
    ("D", "Delta", "DELL-tah", "DEL-ta"),
    ("E", "Echo", "ECK-oh", "E-ko"),
    ("F", "Foxtrot", "FOKS-trot", "FOKS-trot"),
    ("G", "Golf", "GOLF", "GOLF"),
    ("H", "Hotel", "hoh-TELL", "ho-TEL"),
    ("I", "India", "IN-dee-ah", "IN-dia"),
    ("J", "Juliett", "JEW-lee-ETT", "DŻU-li-ET"),
    ("K", "Kilo", "KEY-loh", "KI-lo"),
    ("L", "Lima", "LEE-mah", "LI-ma"),
    ("M", "Mike", "MIKE", "MAJK"),
    ("N", "November", "no-VEM-ber", "no-WEM-ber"),
    ("O", "Oscar", "OSS-cah", "OS-kar"),
    ("P", "Papa", "pah-PAH", "pa-PA"),
    ("Q", "Quebec", "keh-BECK", "ke-BEK"),
    ("R", "Romeo", "ROW-me-oh", "RO-me-o"),
    ("S", "Sierra", "see-AIR-rah", "si-E-ra"),
    ("T", "Tango", "TANG-go", "TAN-go"),
    ("U", "Uniform", "YOU-nee-form", "JU-ni-form"),
    ("V", "Victor", "VIK-tah", "WIK-tor"),
    ("W", "Whiskey", "WISS-key", "ŁIS-ki"),
    ("X", "X-ray", "ECKS-ray", "EKS-rej"),
    ("Y", "Yankee", "YANG-key", "JAN-ki"),
    ("Z", "Zulu", "ZOO-loo", "ZU-lu"),
]

NUMBERS = [
    ("13", "thirteen", "Stress the end: thir-TEEN.", "Akcent na końcu: ther-TIN. Inaczej zabrzmi jak 30."),
    ("30", "thirty", "Stress the start: THIR-ty.", "Akcent na początku: THER-ti."),
    ("0", "zero, oh", "On the radio it is often “oh”.", "Na łączności częściej „oł”."),
    ("07:30", "zero seven thirty", "Half past seven in plain speech.", "Potocznie: half past seven."),
    ("15:30", "fifteen thirty", "The 24-hour clock is read in pairs.", "Zegar wojskowy czyta się parami."),
    ("12:00", "midday, noon", "Not “twelve a.m.”.", "Nie „twelve a.m.” — to północ."),
    ("2.5", "two point five", "A dot, not a comma.", "Po angielsku kropka dziesiętna, nie przecinek."),
    ("1,000", "one thousand", "The comma groups thousands.", "Przecinek oddziela tysiące."),
    ("21st", "the twenty-first", "Days of the month are ordinals.", "Dni miesiąca to liczebniki porządkowe."),
    ("2026", "twenty twenty-six", "Years go in pairs.", "Lata czyta się parami."),
]

ASKING = [
    ("Could you say that again, please?", "Coś umknęło na łączności", "Something slipped by on the radio.", "Coś umknęło na łączności."),
    ("Could you slow down a little, please?", "Za szybko", "The transmission is too fast.", "Nadaje za szybko."),
    ("Could you spell that, please?", "Znak wywoławczy, nazwisko", "A call sign or a name.", "Znak wywoławczy albo nazwisko."),
    ("Do I understand correctly that…?", "Sprawdzam rozkaz", "Check what you heard.", "Sprawdzasz, czy dobrze zrozumiałeś rozkaz."),
    ("Let me confirm the time: fifteen thirty.", "Potwierdzam godzinę", "Repeat the number back.", "Powtarzasz godzinę, żeby ją potwierdzić."),
    ("What does that word mean?", "Nieznane słowo", "One word is missing.", "Brakuje jednego słowa."),
    ("Let me write that down.", "Zapisuję meldunek", "Buy yourself a moment.", "Kupujesz sobie chwilę na zapis."),
    ("Let me put it another way.", "Zacinasz się", "Your own sentence went wrong.", "Twoje zdanie się zacięło."),
]

REFERENCE_TABLES = [
    {
        "anchor": "alfabet",
        "title_en": "Spelling alphabet",
        "title_pl": "Alfabet do literowania",
        "lead_en": "On the radio you say the word, not the letter, so a call sign survives a weak signal.",
        "lead_pl": "Na łączności mówisz słowo, nie literę, żeby znak wywoławczy przeszedł przez słaby sygnał.",
        "columns": [_label("Letter", "Litera"), _label("Word", "Słowo"), _label("How to say it", "Jak to czytać")],
        "rows": [[_english(letter), _english(word), _label(en, pl)] for letter, word, en, pl in ALPHABET],
    },
    {
        "anchor": "liczby",
        "title_en": "Numbers and the clock",
        "title_pl": "Liczby i godzina",
        "lead_en": "Most misunderstandings on duty are a number, not a word.",
        "lead_pl": "Większość nieporozumień na służbie bierze się z liczby, nie ze słowa.",
        "columns": [_label("Written", "Zapis"), _label("Said", "Jak się mówi"), _label("Watch out", "Uwaga")],
        "rows": [[_english(written), _english(said), _label(en, pl)] for written, said, en, pl in NUMBERS],
    },
    {
        "anchor": "dopytaj",
        "title_en": "Asking again",
        "title_pl": "Dopytywanie na łączności",
        "lead_en": "Asking again keeps the net clear. It is not a failure.",
        "lead_pl": "Dopytanie utrzymuje łączność. To nie jest wpadka.",
        "columns": [_label("Say this", "Powiedz to"), _label("When", "Kiedy")],
        "rows": [[_english(phrase), _label(en, pl)] for phrase, _short, en, pl in ASKING],
    },
]
