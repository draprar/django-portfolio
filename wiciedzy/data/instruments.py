"""Preference items, public-domain IPIP stems, and the humorous archetype quiz.

Polish IPIP wording is a translation made for this project. The English stems are
IPIP public-domain items in the Mini-IPIP selection (Donnellan et al., 2006).
"""

from __future__ import annotations

TYPES: list[dict[str, str]] = [
    {"code": "combat_sport", "name_pl": "Sport walki", "name_en": "Combat sport"},
    {"code": "martial_art", "name_pl": "Sztuka walki", "name_en": "Martial art"},
    {"code": "self_defence", "name_pl": "Samoobrona", "name_en": "Self-defence"},
    {"code": "weapon_based", "name_pl": "Z bronią", "name_en": "Weapon-based"},
    {"code": "traditional", "name_pl": "Tradycyjne", "name_en": "Traditional"},
    {"code": "historical_reconstruction", "name_pl": "Rekonstrukcja historyczna", "name_en": "Historical reconstruction"},
    {"code": "hybrid", "name_pl": "Mieszane", "name_en": "Hybrid"},
]

IPIP_ATTRIBUTION = (
    "English Mini-IPIP (Donnellan et al., 2006), public-domain IPIP items. "
    "The Polish wording is my own unvalidated translation."
)

IPIP_SCALES: list[dict[str, str]] = [
    {"code": "E", "name_pl": "Ekstrawersja", "name_en": "Extraversion"},
    {"code": "A", "name_pl": "Ugodowość", "name_en": "Agreeableness"},
    {"code": "C", "name_pl": "Sumienność", "name_en": "Conscientiousness"},
    {"code": "N", "name_pl": "Neurotyczność", "name_en": "Neuroticism"},
    {"code": "O", "name_pl": "Otwartość", "name_en": "Openness"},
]

# (scale, reverse, en, pl)
IPIP_ITEMS: list[tuple[str, bool, str, str]] = [
    ("E", False, "Am the life of the party.", "Jestem duszą towarzystwa."),
    ("E", True, "Don't talk a lot.", "Mówię niewiele."),
    ("E", False, "Talk to a lot of different people at parties.", "Na imprezach gadam z wieloma różnymi ludźmi."),
    ("E", True, "Keep in the background.", "Trzymam się w tle."),
    ("A", False, "Sympathize with others' feelings.", "Współczuję innym w ich uczuciach."),
    ("A", True, "Am not interested in other people's problems.", "Cudze problemy mnie nie obchodzą."),
    ("A", False, "Feel others' emotions.", "Czuję emocje innych."),
    ("A", True, "Am not really interested in others.", "Inni ludzie specjalnie mnie nie interesują."),
    ("C", False, "Get chores done right away.", "Obowiązki załatwiam od razu."),
    ("C", True, "Often forget to put things back in their proper place.", "Często zapominam odłożyć rzeczy na miejsce."),
    ("C", False, "Like order.", "Lubię porządek."),
    ("C", True, "Make a mess of things.", "Robię bałagan."),
    ("N", False, "Have frequent mood swings.", "Często zmienia mi się nastrój."),
    ("N", True, "Am relaxed most of the time.", "Przez większość czasu jestem spokojny."),
    ("N", False, "Get upset easily.", "Łatwo się denerwuję."),
    ("N", True, "Seldom feel blue.", "Rzadko bywa mi smutno."),
    ("O", False, "Have a vivid imagination.", "Mam bujną wyobraźnię."),
    ("O", True, "Am not interested in abstract ideas.", "Abstrakcyjne idee mnie nie interesują."),
    ("O", True, "Have difficulty understanding abstract ideas.", "Trudno mi zrozumieć abstrakcyjne idee."),
    ("O", True, "Do not have a good imagination.", "Nie mam dobrej wyobraźni."),
]

PREFERENCE: list[dict] = [
    {
        "sort_order": 1,
        "kind": "scale",
        "dimension": "striking",
        "text_pl": "Jak bardzo chcesz uderzać?",
        "text_en": "How much do you want to strike?",
    },
    {
        "sort_order": 2,
        "kind": "scale",
        "dimension": "grappling",
        "text_pl": "Jak bardzo chcesz chwytać?",
        "text_en": "How much do you want to grapple?",
    },
    {
        "sort_order": 3,
        "kind": "scale",
        "dimension": "ground_fighting",
        "text_pl": "Jak bardzo chcesz walczyć w parterze?",
        "text_en": "How much do you want to fight on the ground?",
    },
    {
        "sort_order": 4,
        "kind": "scale",
        "dimension": "weapons",
        "text_pl": "Jak bardzo chcesz mieć broń na treningu?",
        "text_en": "How much do you want a weapon in training?",
    },
    {
        "sort_order": 5,
        "kind": "scale",
        "dimension": "kicks",
        "text_pl": "Jak bardzo chcesz kopać?",
        "text_en": "How much do you want to kick?",
    },
    {
        "sort_order": 6,
        "kind": "scale",
        "dimension": "contact_level",
        "text_pl": "Jak mocny ma być kontakt na treningu z partnerem?",
        "text_en": "How hard should partner contact be in training?",
        "anchor_low_pl": "bardzo lekki",
        "anchor_low_en": "very light",
        "anchor_high_pl": "bardzo mocny",
        "anchor_high_en": "very hard",
        "hint_pl": "1 oznacza bardzo lekki kontakt, 5 — bardzo mocny.",
        "hint_en": "1 means very light contact, 5 — very hard.",
    },
    {
        "sort_order": 7,
        "kind": "scale",
        "dimension": "competition_level",
        "text_pl": "Jak bardzo chcesz startować w zawodach?",
        "text_en": "How much do you want to compete?",
    },
    {
        "sort_order": 8,
        "kind": "scale",
        "dimension": "tradition_level",
        "text_pl": "Jak ważna jest dla Ciebie tradycja i zwyczaje w sali?",
        "text_en": "How much do hall custom and tradition matter to you?",
    },
    {
        "sort_order": 9,
        "kind": "scale",
        "dimension": "technical_complexity",
        "text_pl": "Jak bardzo chcesz złożonej technicznie pracy?",
        "text_en": "How much technical complexity do you want?",
        "anchor_low_pl": "bardzo prosto",
        "anchor_low_en": "very simple",
        "anchor_high_pl": "bardzo złożone",
        "anchor_high_en": "very complex",
        "hint_pl": "1 oznacza bardzo prosto, 5 — bardzo złożone.",
        "hint_en": "1 means very simple, 5 — very complex.",
    },
    {
        "sort_order": 10,
        "kind": "scale",
        "dimension": "athletic_demand",
        "text_pl": "Jak wymagający fizycznie ma być trening?",
        "text_en": "How physically demanding do you want training to be?",
        "anchor_low_pl": "bardzo lekki",
        "anchor_low_en": "very light",
        "anchor_high_pl": "bardzo wymagający",
        "anchor_high_en": "very demanding",
        "hint_pl": "1 oznacza bardzo lekki trening, 5 — bardzo wymagający.",
        "hint_en": "1 means very light training, 5 — very demanding.",
    },
    {
        "sort_order": 11,
        "kind": "ab",
        "dimension": "",
        "text_pl": "Wolisz ćwiczyć głównie sam, głównie z partnerem, czy mieszać oba?",
        "text_en": "Would you rather train mostly alone, mostly with a partner, or a mix of both?",
        "options": [
            {
                "text_pl": "Głównie sam — technika albo worek.",
                "text_en": "Mostly alone — technique or a bag.",
                "weights": [("solo_training", 2), ("partner_training", -2)],
            },
            {
                "text_pl": "Mieszanka solo i z partnerem.",
                "text_en": "A mix of solo and partner work.",
                "weights": [("solo_training", 1), ("partner_training", 1)],
            },
            {
                "text_pl": "Głównie z partnerem, który się rusza.",
                "text_en": "Mostly with a partner who moves.",
                "weights": [("solo_training", -2), ("partner_training", 2)],
            },
        ],
    },
    {
        "sort_order": 12,
        "kind": "ab",
        "dimension": "",
        "text_pl": "Wolisz zostać z daleka, wejść blisko, czy trzymać mieszankę?",
        "text_en": "Would you rather stay at range, step in close, or keep a mix?",
        "options": [
            {
                "text_pl": "Z daleka — niech noga robi robotę.",
                "text_en": "At range — let the leg do the work.",
                "weights": [("kicks", 2), ("clinch", -2)],
            },
            {
                "text_pl": "Z bliska — klincz albo chwyt.",
                "text_en": "Up close — a clinch or a grip.",
                "weights": [("clinch", 2), ("kicks", -2)],
            },
            {
                "text_pl": "Mieszanka — kopnięcia i klincz po równo.",
                "text_en": "A mix — kicks and clinch matter about equally.",
                "weights": [("kicks", 1), ("clinch", 1)],
            },
        ],
    },
    {
        "sort_order": 13,
        "kind": "situation",
        "dimension": "",
        "text_pl": "Co wolisz, gdy trening schodzi do bliskiej pracy?",
        "text_en": "What do you prefer when training moves into close work?",
        "options": [
            {
                "text_pl": "Rzut.",
                "text_en": "A throw.",
                "weights": [("throws", 2)],
            },
            {
                "text_pl": "Obalenie.",
                "text_en": "A takedown.",
                "weights": [("takedowns", 2)],
            },
            {
                "text_pl": "Schodzisz do parteru i szukasz poddania.",
                "text_en": "Ground work and a submission.",
                "weights": [("submissions", 2), ("ground_fighting", 2)],
            },
            {
                "text_pl": "Uderzenie z bliska.",
                "text_en": "A strike at close range.",
                "weights": [("striking", 1)],
            },
        ],
    },
    {
        "sort_order": 14,
        "kind": "multi",
        "dimension": "",
        "text_pl": "Zaznacz, co ma być w Twoim tygodniu treningowym. Możesz wybrać kilka rzeczy naraz; jeśli nic z tego nie ma dla Ciebie znaczenia, zaznacz wyłącznie ostatnią opcję.",
        "text_en": "Tick what should be in your training week. You can pick several; if none of it matters to you, tick only the last option.",
        "options": [
            {"text_pl": "Kolana.", "text_en": "Knees.", "weights": [("knees", 2)]},
            {"text_pl": "Łokcie.", "text_en": "Elbows.", "weights": [("elbows", 2)]},
            {"text_pl": "Zbroja albo maska.", "text_en": "Armour or a mask.", "weights": [("equipment_required", 2)]},
            {"text_pl": "Rękawice.", "text_en": "Gloves.", "weights": [("equipment_required", 1)]},
            {"text_pl": "Wytrzymałość, długie rundy.", "text_en": "Endurance, long rounds.", "weights": [("endurance_demand", 2)]},
            {"text_pl": "Eksplozywne wejście.", "text_en": "An explosive entry.", "weights": [("explosiveness", 2)]},
            {"text_pl": "Nic z powyższych.", "text_en": "None of these.", "weights": []},
        ],
    },
    {
        "sort_order": 15,
        "kind": "scale",
        "dimension": "punches",
        "required": False,
        "text_pl": "Jak ważna jest dla Ciebie konkretnie praca pięściami?",
        "text_en": "How important is punch work specifically?",
    },
]

OPTIONAL_SCALE_ORDERS = frozenset(
    row["sort_order"] for row in PREFERENCE if row.get("required") is False
)

PREFERENCE_SCALE_ANCHORS: dict[int, dict[str, str]] = {
    row["sort_order"]: row
    for row in PREFERENCE
    if row.get("kind") == "scale" and row.get("anchor_low_pl")
}
