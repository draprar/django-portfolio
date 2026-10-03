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
        "text_pl": "Jak bardzo chcesz chwytać i trzymać?",
        "text_en": "How much do you want to grapple and hold?",
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
        "text_pl": "Jak mocny ma być kontakt?",
        "text_en": "How hard should the contact be?",
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
        "text_pl": "Jak ważne są dla Ciebie formy i zwyczaje w sali?",
        "text_en": "How much do forms and hall customs matter to you?",
    },
    {
        "sort_order": 9,
        "kind": "ab",
        "dimension": "",
        "text_pl": "Wolisz ćwiczyć sam czy z partnerem?",
        "text_en": "Would you rather train alone, or with a partner?",
        "options": [
            {
                "text_pl": "Sam, forma albo worek.",
                "text_en": "Alone, with a form or a bag.",
                "weights": [("solo_training", 2), ("partner_training", -2)],
            },
            {
                "text_pl": "Z partnerem, który się rusza.",
                "text_en": "With a partner who moves.",
                "weights": [("partner_training", 2), ("solo_training", -2)],
            },
        ],
    },
    {
        "sort_order": 10,
        "kind": "ab",
        "dimension": "",
        "text_pl": "Wolisz zostać daleko czy wejść blisko?",
        "text_en": "Would you rather stay far, or step in close?",
        "options": [
            {
                "text_pl": "Z daleka, niech noga robi robotę.",
                "text_en": "At a distance, let the leg do the work.",
                "weights": [("kicks", 2), ("clinch", -2)],
            },
            {
                "text_pl": "Z bliska, klincz albo chwyt.",
                "text_en": "Up close, a clinch or a grip.",
                "weights": [("clinch", 2), ("kicks", -1)],
            },
        ],
    },
    {
        "sort_order": 11,
        "kind": "situation",
        "dimension": "",
        "text_pl": "Na treningu dochodzi do zwarcia. Co ma być dalej?",
        "text_en": "In training it comes to close range. What should happen next?",
        "options": [
            {
                "text_pl": "Rzut.",
                "text_en": "A throw.",
                "weights": [("throws", 2), ("takedowns", 1)],
            },
            {
                "text_pl": "Schodzicie do parteru i szukacie poddania.",
                "text_en": "You go to the ground and look for a submission.",
                "weights": [("submissions", 2), ("ground_fighting", 2)],
            },
            {
                "text_pl": "Uderzenie i odskok.",
                "text_en": "A strike and a step out.",
                "weights": [("punches", 2), ("striking", 1)],
            },
        ],
    },
    {
        "sort_order": 12,
        "kind": "multi",
        "dimension": "",
        "text_pl": "Zaznacz, co ma być w Twoim tygodniu treningowym. Możesz wybrać kilka rzeczy naraz, a jeśli nic z tego Cię nie rusza, zostaw puste.",
        "text_en": "Tick what should be in your training week. You can pick several, or leave it blank if none of it matters to you.",
        "options": [
            {"text_pl": "Kolana i łokcie.", "text_en": "Knees and elbows.", "weights": [("knees", 2), ("elbows", 2)]},
            {"text_pl": "Zbroja albo maska.", "text_en": "Armour or a mask.", "weights": [("equipment_required", 2)]},
            {"text_pl": "Rękawice.", "text_en": "Gloves.", "weights": [("equipment_required", 1)]},
            {"text_pl": "Wytrzymałość, długie rundy.", "text_en": "Endurance, long rounds.", "weights": [("endurance_demand", 2)]},
            {"text_pl": "Szybkie, mocne wejście.", "text_en": "An explosive entry.", "weights": [("explosiveness", 2)]},
            {"text_pl": "Nic z tego.", "text_en": "None of these.", "weights": []},
        ],
    },
]

ARCHETYPES: list[dict] = [
    {
        "slug": "chce-miecz",
        "name_pl": "Człowiek, który chce miecz",
        "name_en": "The person who wants a sword",
        "description_pl": "Najpierw pytasz o stal, dopiero potem o rozgrzewkę. Sala bez broni to dla Ciebie poczekalnia.",
        "description_en": "You ask about the steel first and the warm-up later. A hall without a weapon is just a waiting room to you.",
        "styles": ["hema", "kendo", "szermierka"],
    },
    {
        "slug": "jeszcze-jedna-runda",
        "name_pl": "Człowiek jeszcze jednej rundy",
        "name_en": "One more round",
        "description_pl": "Koniec treningu to dla Ciebie plotka, więc zostajesz, aż ktoś zgasi światło.",
        "description_en": "The end of training is a rumour to you, so you stay until someone turns the lights off.",
        "styles": ["boks", "muay-thai", "kickboxing"],
    },
    {
        "slug": "maniak-techniki",
        "name_pl": "Maniak techniki",
        "name_en": "The technique obsessive",
        "description_pl": "Jeden detal potrafi zająć Ci cały wieczór, a wygrana to tylko efekt uboczny.",
        "description_en": "One detail can take up your whole evening, and winning is just a side effect.",
        "styles": ["bjj", "aikido", "hema"],
    },
    {
        "slug": "mistrz-przytulania",
        "name_pl": "Mistrz przytulania",
        "name_en": "Master of the hug",
        "description_pl": "Dystans jest przereklamowany. Jak już kogoś masz, to go nie wypuszczasz.",
        "description_en": "Distance is overrated. Once you've got someone, you don't let go.",
        "styles": ["judo", "zapasy", "bjj"],
    },
    {
        "slug": "po-pas",
        "name_pl": "Ten, który przyszedł po pas",
        "name_en": "Here for the belt",
        "description_pl": "Lubisz, kiedy sala ma swoją drogę, a droga ma kolory. Egzamin jest częścią zabawy.",
        "description_en": "You like it when the hall has a path and the path has colours. The exam is part of the fun.",
        "styles": ["karate", "taekwondo", "judo"],
    },
    {
        "slug": "rycerz-regulaminu",
        "name_pl": "Rycerz regulaminu",
        "name_en": "Knight of the rulebook",
        "description_pl": "Linia, komenda, punkt. Chaos zostawiasz za drzwiami szatni.",
        "description_en": "A line, a command, a point. You leave the chaos outside the locker room.",
        "styles": ["judo", "szermierka", "taekwondo"],
    },
]

HUMOR: list[dict] = [
    {
        "sort_order": 1,
        "text_pl": "Wchodzisz na salę pierwszy raz. Czego szukasz wzrokiem?",
        "text_en": "You walk into a hall for the first time. What do your eyes look for?",
        "choices": [
            ("Czy jest tu miecz?", "Whether there's a sword.", "chce-miecz"),
            ("Czy da się zostać po treningu?", "Whether you can stay after class.", "jeszcze-jedna-runda"),
            ("Czy ktoś tu tłumaczy każdy szczegół?", "Whether someone explains every detail.", "maniak-techniki"),
            ("Kogo da się złapać?", "Who you can grab.", "mistrz-przytulania"),
        ],
    },
    {
        "sort_order": 2,
        "text_pl": "Trener mówi: koniec. Co robisz?",
        "text_en": "The coach says: that's it. What do you do?",
        "choices": [
            ("Pytasz, czy broń też się odkłada.", "You ask if the weapon gets put away too.", "chce-miecz"),
            ("Prosisz o jeszcze jedną rundę.", "You ask for one more round.", "jeszcze-jedna-runda"),
            ("Powtarzasz ten jeden ruch, aż wreszcie siądzie.", "You keep repeating the one move until it finally lands.", "maniak-techniki"),
            ("Nadal kogoś trzymasz.", "You're still holding someone.", "mistrz-przytulania"),
        ],
    },
    {
        "sort_order": 3,
        "text_pl": "Z czego najbardziej cieszysz się po miesiącu?",
        "text_en": "What makes you happiest after a month?",
        "choices": [
            ("Że już wiesz, jak stać z bronią.", "That you know how to stand with a weapon.", "chce-miecz"),
            ("Że oddech wraca szybciej.", "That your breath comes back faster.", "jeszcze-jedna-runda"),
            ("Że jeden chwyt wreszcie siada.", "That one grip finally lands.", "maniak-techniki"),
            ("Że pas ma inny kolor.", "That the belt is a different colour.", "po-pas"),
        ],
    },
    {
        "sort_order": 4,
        "text_pl": "Sparing leci, a ktoś robi coś poza zasadami. Co wtedy?",
        "text_en": "Sparring is on, and someone does something outside the rules. Then what?",
        "choices": [
            ("Przypominasz, co wolno, a czego nie.", "You remind them what's allowed and what isn't.", "rycerz-regulaminu"),
            ("Olej, leci następna runda.", "Never mind, the next round is on.", "jeszcze-jedna-runda"),
            ("Pokaż to jeszcze raz, wolniej.", "Show it again, slower.", "maniak-techniki"),
            ("I tak cię zaraz złapię.", "I'm going to grab you anyway.", "mistrz-przytulania"),
        ],
    },
    {
        "sort_order": 5,
        "text_pl": "Co z tej sali zabrałbyś do domu?",
        "text_en": "What would you take home from this hall?",
        "choices": [
            ("Miecz. Albo cokolwiek z jelcem.", "A sword. Or anything with a guard.", "chce-miecz"),
            ("Rękawice, nawet jeśli już śmierdzą.", "The gloves, even if they already smell.", "jeszcze-jedna-runda"),
            ("Notes na detale.", "A notebook for the details.", "maniak-techniki"),
            ("Kolejny pas, nawet za wcześnie.", "Another belt, even if it's early.", "po-pas"),
        ],
    },
    {
        "sort_order": 6,
        "text_pl": "Sparing leci w krzaki. Na czym się skupiasz?",
        "text_en": "The sparring is going off the rails. What do you focus on?",
        "choices": [
            ("Dystans i linia.", "Distance and the line.", "rycerz-regulaminu"),
            ("Tempo. Niech leci.", "The pace. Keep it moving.", "jeszcze-jedna-runda"),
            ("Ten jeden detal, który jeszcze działa.", "The one detail that still works.", "maniak-techniki"),
            ("Uchwyt. Nie puszczam.", "The grip. I'm not letting go.", "mistrz-przytulania"),
        ],
    },
    {
        "sort_order": 7,
        "text_pl": "Oglądasz walkę. Gdzie chcesz siedzieć?",
        "text_en": "You're watching a bout. Where do you want to sit?",
        "choices": [
            ("Tam, skąd widać broń.", "Where you can see the weapon.", "chce-miecz"),
            ("Jak najbliżej, żeby czuć rundę.", "As close as possible, to feel the round.", "jeszcze-jedna-runda"),
            ("Z notesem, żebym widział detale.", "With a notebook, so I can see the details.", "maniak-techniki"),
            ("Tam, gdzie sędzia gada o przepisach.", "Where the referee talks about the rules.", "rycerz-regulaminu"),
        ],
    },
    {
        "sort_order": 8,
        "text_pl": "Znajomy pyta, po co Ci to. Co mu mówisz?",
        "text_en": "A friend asks why you do this. What do you tell them?",
        "choices": [
            ("Bo chcę miecz. Tyle.", "Because I want a sword. That's all.", "chce-miecz"),
            ("Bo chcę jeszcze jedną rundę.", "Because I want one more round.", "jeszcze-jedna-runda"),
            ("Bo pas wisi w domu.", "Because the belt hangs at home.", "po-pas"),
            ("Bo lubię, kiedy ktoś nie ucieka z uchwytu.", "Because I like it when someone doesn't slip the grip.", "mistrz-przytulania"),
        ],
    },
]
