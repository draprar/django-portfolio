"""World Rugby passport rules used on the learn module. checked_on = date verified in repo."""

CHECKED_ON = "2026-10-11"

LAWS: list[dict] = [
    {
        "topic": "Czas meczu",
        "variant": "sevens",
        "law_ref": "Sevens Law 5",
        "source_url": "https://passport.world.rugby/laws-of-the-game/variations-7s-10s-u19-game-on/sevens/5-time/",
        "checked_on": CHECKED_ON,
        "summary_pl": "Mecz trwa 14 minut: dwie połowy do 7 minut, przerwa do 2 minut.",
        "consequence_pl": "Dogrywka to okresy do 5 minut; finał turniejowy może trwać do 20 minut.",
        "uncertainty": "",
    },
    {
        "topic": "Czas meczu",
        "variant": "xv",
        "law_ref": "Law 5",
        "source_url": "https://passport.world.rugby/laws-of-the-game/",
        "checked_on": CHECKED_ON,
        "summary_pl": "Mecz XV to dwie połowy po 40 minut (w większości rozgrywek amatorskich i zawodowych).",
        "consequence_pl": "Więcej czasu na zmianę tempa i ustawienie po przerwie.",
        "uncertainty": "Dokładny czas połowy zależy od regulaminu rozgrywek — tu podstawowy wzorzec XV.",
    },
    {
        "topic": "Konwersja",
        "variant": "sevens",
        "law_ref": "Sevens Law 8",
        "source_url": "https://passport.world.rugby/laws-of-the-game/variations-7s-10s-u19-game-on/sevens/8-scoring/",
        "checked_on": CHECKED_ON,
        "summary_pl": "Konwersja musi być drop kickiem, w ciągu 30 sekund od przyłożenia.",
        "consequence_pl": "W dogrywce wygrywa pierwszy zdobywca punktów.",
        "uncertainty": "",
    },
    {
        "topic": "Żółta kartka",
        "variant": "sevens",
        "law_ref": "Law 9 / Regulation 17.2.2 (sevens)",
        "source_url": "https://passport.world.rugby/laws-of-the-game/variations-7s-10s-u19-game-on/sevens/9-foul-play/",
        "checked_on": CHECKED_ON,
        "summary_pl": "Zawieszenie po żółtej kartce trwa 2 minuty.",
        "consequence_pl": "Czas po przerwie wlicza się do zawieszenia.",
        "uncertainty": "",
    },
    {
        "topic": "Żółta kartka",
        "variant": "xv",
        "law_ref": "Law 9 / Regulation 17.2.2",
        "source_url": "https://passport.world.rugby/laws-of-the-game/",
        "checked_on": CHECKED_ON,
        "summary_pl": "Zawieszenie po żółtej kartce trwa 10 minut.",
        "consequence_pl": "Drużyna gra krótko w osłabieniu liczebnym.",
        "uncertainty": "",
    },
    {
        "topic": "Liczba zawodników",
        "variant": "sevens",
        "law_ref": "Sevens variations",
        "source_url": "https://passport.world.rugby/laws-of-the-game/variations-7s-10s-u19-game-on/sevens/",
        "checked_on": CHECKED_ON,
        "summary_pl": "Na boisku jest siedem zawodników z każdej strony.",
        "consequence_pl": "Więcej pustej przestrzeni niż w XV — tempo i bieganie w bok mają większą wagę.",
        "uncertainty": "Interpretacja taktyczna, nie sama liczba z przepisu.",
    },
    {
        "topic": "Liczba zawodników",
        "variant": "xv",
        "law_ref": "Law 3",
        "source_url": "https://passport.world.rugby/laws-of-the-game/",
        "checked_on": CHECKED_ON,
        "summary_pl": "Na boisku jest piętnaście zawodników z każdej strony.",
        "consequence_pl": "Więcej kontaktu i młynów; linie ataku są gęstsze.",
        "uncertainty": "Interpretacja taktyczna.",
    },
]

DISCLAIMER = (
    "To nie jest egzamin World Rugby, certyfikat, szkolenie trenerskie ani rekomendacja taktyki. "
    "Sprawdź przepisy na stronie World Rugby przed meczem oficjalnym."
)
