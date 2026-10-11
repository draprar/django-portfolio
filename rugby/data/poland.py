"""Polish rugby today — cards and links. Numbers only when stable."""

from datetime import date

FRESHNESS_DAYS = 90

LINKS = {
    "clubs": "https://polskie.rugby/kluby",
    "extraliga": "https://polskie.rugby/sezon/39/ekstraliga-rugby-20262027",
    "rugby_europe": "https://www.rugbyeurope.eu/competitions/",
    "rankings_men": "https://www.world.rugby/rankings/mru",
    "rankings_women": "https://www.world.rugby/rankings/wru",
}

CARDS: list[dict] = [
    {
        "slug": "xv-men",
        "title": "Reprezentacja XV — mężczyźni",
        "variant": "XV",
        "competition": "World Rugby Rankings",
        "season": "bieżący",
        "checked_on": "2026-10-11",
        "volatile": True,
        "position": None,
        "points": None,
        "context_pl": "Ranking XV to nie to samo co miejsce w turnieju siódemek. Sprawdź tabelę na World Rugby.",
        "source_url": LINKS["rankings_men"],
    },
    {
        "slug": "xv-women",
        "title": "Reprezentacja XV — kobiety",
        "variant": "XV",
        "competition": "World Rugby Rankings",
        "season": "bieżący",
        "checked_on": "2026-10-11",
        "volatile": True,
        "position": None,
        "points": None,
        "context_pl": "Osobna tabela rankingowa dla kobiet.",
        "source_url": LINKS["rankings_women"],
    },
    {
        "slug": "7-men",
        "title": "Rugby 7 — mężczyźni",
        "variant": "7",
        "competition": "Seria europejska / SVNS (zależnie od sezonu)",
        "season": "bieżący",
        "checked_on": "2026-10-11",
        "volatile": True,
        "position": None,
        "points": None,
        "context_pl": "To nie jest „ranking światowy” — to klasyfikacja w nazwanej serii rozgrywek.",
        "source_url": LINKS["rugby_europe"],
    },
    {
        "slug": "7-women",
        "title": "Rugby 7 — kobiety",
        "variant": "7",
        "competition": "Rugby Europe Women's 7s Championship Series 2026",
        "season": "2026",
        "checked_on": "2026-07-26",
        "volatile": False,
        "position": "1.",
        "points": "36 (18 + 18)",
        "context_pl": (
            "Hamburg 3–5 VII, Split 24–26 VII. W finale w Splicie Polska przegrała z Irlandią 26:12. "
            "Zakończona seria — liczby z oficjalnej relacji Rugby Europe."
        ),
        "source_url": "https://www.rugbyeurope.eu/",
    },
]

SCENE_NOTE = (
    "Ranking XV i tabela turnieju siódemek mierzą co innego. "
    "Szukasz drużyny w Polsce — zacznij od katalogu klubów PZR."
)


def card_display(card: dict, today: date | None = None) -> dict:
    """Return card with show_numbers flag for templates."""
    today = today or date.today()
    checked = date.fromisoformat(card["checked_on"])
    age = (today - checked).days
    stale = card.get("volatile", True) and age > FRESHNESS_DAYS
    show_numbers = bool(card.get("position")) and not stale
    return {**card, "show_numbers": show_numbers, "stale": stale}
