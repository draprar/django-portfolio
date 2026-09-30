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
    "Polish wording is an unvalidated project translation."
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
    ("E", True, "Don't talk a lot.", "Niewiele mówię."),
    ("E", False, "Talk to a lot of different people at parties.", "Na spotkaniach rozmawiam z wieloma różnymi osobami."),
    ("E", True, "Keep in the background.", "Trzymam się z tyłu."),
    ("A", False, "Sympathize with others' feelings.", "Współczuję uczuciom innych."),
    ("A", True, "Am not interested in other people's problems.", "Nie interesują mnie problemy innych ludzi."),
    ("A", False, "Feel others' emotions.", "Czuję emocje innych."),
    ("A", True, "Am not really interested in others.", "Niespecjalnie interesują mnie inni."),
    ("C", False, "Get chores done right away.", "Obowiązki załatwiam od razu."),
    ("C", True, "Often forget to put things back in their proper place.", "Często zapominam odłożyć rzeczy na miejsce."),
    ("C", False, "Like order.", "Lubię porządek."),
    ("C", True, "Make a mess of things.", "Robię bałagan."),
    ("N", False, "Have frequent mood swings.", "Często zmienia mi się nastrój."),
    ("N", True, "Am relaxed most of the time.", "Przez większość czasu jestem spokojny."),
    ("N", False, "Get upset easily.", "Łatwo się denerwuję."),
    ("N", True, "Seldom feel blue.", "Rzadko jest mi smutno."),
    ("O", False, "Have a vivid imagination.", "Mam żywą wyobraźnię."),
    ("O", True, "Am not interested in abstract ideas.", "Nie interesują mnie abstrakcyjne idee."),
    ("O", True, "Have difficulty understanding abstract ideas.", "Trudno mi zrozumieć abstrakcyjne idee."),
    ("O", True, "Do not have a good imagination.", "Nie mam dobrej wyobraźni."),
]

PREFERENCE: list[dict] = [
    {
        "sort_order": 1,
        "kind": "scale",
        "dimension": "striking",
        "text_pl": "Na ile chcesz, żeby trening był o uderzeniach?",
        "text_en": "How much do you want the training to be about striking?",
    },
    {
        "sort_order": 2,
        "kind": "scale",
        "dimension": "grappling",
        "text_pl": "Na ile chcesz, żeby trening był o chwycie i trzymaniu?",
        "text_en": "How much do you want the training to be about gripping and holding?",
    },
    {
        "sort_order": 3,
        "kind": "scale",
        "dimension": "ground_fighting",
        "text_pl": "Na ile chcesz pracować w parterze?",
        "text_en": "How much do you want to work in the ground fight?",
    },
    {
        "sort_order": 4,
        "kind": "scale",
        "dimension": "weapons",
        "text_pl": "Na ile chcesz, żeby w treningu była broń?",
        "text_en": "How much do you want a weapon in the training?",
    },
    {
        "sort_order": 5,
        "kind": "scale",
        "dimension": "kicks",
        "text_pl": "Na ile chcesz kopać?",
        "text_en": "How much do you want to kick?",
    },
    {
        "sort_order": 6,
        "kind": "scale",
        "dimension": "contact_level",
        "text_pl": "Na ile chcesz twardego kontaktu?",
        "text_en": "How much hard contact do you want?",
    },
    {
        "sort_order": 7,
        "kind": "scale",
        "dimension": "competition_level",
        "text_pl": "Na ile chcesz startować w zawodach?",
        "text_en": "How much do you want to compete?",
    },
    {
        "sort_order": 8,
        "kind": "scale",
        "dimension": "tradition_level",
        "text_pl": "Na ile chcesz form i zwyczaju sali?",
        "text_en": "How much do you want forms and hall custom?",
    },
    {
        "sort_order": 9,
        "kind": "ab",
        "dimension": "",
        "text_pl": "Wolisz ćwiczyć sam, czy z kimś, kto odpowiada?",
        "text_en": "Would you rather train alone, or with someone who answers back?",
        "options": [
            {
                "text_pl": "Sam, forma albo worek.",
                "text_en": "Alone, a form or a bag.",
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
        "text_pl": "Wolisz zostać daleko, czy wejść blisko?",
        "text_en": "Would you rather stay far, or step in close?",
        "options": [
            {
                "text_pl": "Daleko. Niech noga robi robotę.",
                "text_en": "Far. Let the leg do the work.",
                "weights": [("kicks", 2), ("clinch", -2)],
            },
            {
                "text_pl": "Blisko. Klincz albo chwyt.",
                "text_en": "Close. A clinch or a grip.",
                "weights": [("clinch", 2), ("kicks", -1)],
            },
        ],
    },
    {
        "sort_order": 11,
        "kind": "situation",
        "dimension": "",
        "text_pl": "Trening, który lubisz, dochodzi do zwarcia. Co ma się stać dalej?",
        "text_en": "The training you like comes to close range. What should happen next?",
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
        "text_pl": "Zaznacz, co ma być w tygodniu treningu. Możesz zaznaczyć kilka rzeczy. Zostaw puste, jeśli żadna z nich nie jest ważna.",
        "text_en": "Tick what should be in a training week. You can tick several. Leave this blank if none of them matter.",
        "options": [
            {"text_pl": "Kolana i łokcie.", "text_en": "Knees and elbows.", "weights": [("knees", 2), ("elbows", 2)]},
            {"text_pl": "Zbroja albo maska.", "text_en": "Armour or a mask.", "weights": [("equipment_required", 2)]},
            {"text_pl": "Rękawice.", "text_en": "Gloves.", "weights": [("equipment_required", 1)]},
            {"text_pl": "Wytrzymałość, długie rundy.", "text_en": "Endurance, long rounds.", "weights": [("endurance_demand", 2)]},
            {"text_pl": "Eksplozywne wejście.", "text_en": "An explosive entry.", "weights": [("explosiveness", 2)]},
            {"text_pl": "Nic z tej listy.", "text_en": "None of these.", "weights": []},
        ],
    },
]

ARCHETYPES: list[dict] = [
    {
        "slug": "chce-miecz",
        "name_pl": "Człowiek, który chce miecz",
        "name_en": "The person who wants a sword",
        "description_pl": "Pytasz o stal, zanim zapytasz o rozgrzewkę. Sala bez broni jest dla Ciebie poczekalnią.",
        "description_en": "You ask about the steel before you ask about the warm-up. A hall without a weapon is a waiting room.",
        "styles": ["hema", "kendo", "szermierka"],
    },
    {
        "slug": "jeszcze-jedna-runda",
        "name_pl": "Człowiek jeszcze jednej rundy",
        "name_en": "One more round",
        "description_pl": "Koniec treningu jest plotką. Zostajesz, dopóki ktoś nie zgasi światła.",
        "description_en": "The end of training is a rumour. You stay until someone turns the lights off.",
        "styles": ["boks", "muay-thai", "kickboxing"],
    },
    {
        "slug": "maniak-techniki",
        "name_pl": "Maniak techniki",
        "name_en": "The technique obsessive",
        "description_pl": "Jeden detal potrafi zająć Ci cały wieczór. Wygrana jest efektem ubocznym.",
        "description_en": "One detail can take your whole evening. Winning is a side effect.",
        "styles": ["bjj", "aikido", "hema"],
    },
    {
        "slug": "mistrz-przytulania",
        "name_pl": "Mistrz przytulania",
        "name_en": "Master of the hug",
        "description_pl": "Dystans jest przereklamowany. Jak już kogoś masz, to nie wypuszczasz.",
        "description_en": "Distance is overrated. Once you have someone, you do not let go.",
        "styles": ["judo", "zapasy", "bjj"],
    },
    {
        "slug": "po-pas",
        "name_pl": "Ten, który przyszedł po pas",
        "name_en": "Here for the belt",
        "description_pl": "Lubisz, gdy sala ma drogę, a droga ma kolory. Egzamin jest częścią zabawy.",
        "description_en": "You like it when the hall has a path, and the path has colours. The exam is part of the fun.",
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
            ("Czy jest tu miecz.", "Whether there is a sword.", "chce-miecz"),
            ("Czy da się zostać po czasie.", "Whether you can stay after the hour.", "jeszcze-jedna-runda"),
            ("Czy ktoś tu tłumaczy detal.", "Whether someone explains the detail.", "maniak-techniki"),
            ("Kogo da się złapać.", "Who can be grabbed.", "mistrz-przytulania"),
        ],
    },
    {
        "sort_order": 2,
        "text_pl": "Trener mówi: koniec. Co robisz?",
        "text_en": "The coach says: that's it. What do you do?",
        "choices": [
            ("Pytasz, czy broń też się chowa.", "You ask if the weapon gets put away too.", "chce-miecz"),
            ("Prosisz o jeszcze jedną rundę.", "You ask for one more round.", "jeszcze-jedna-runda"),
            ("Zostajesz przy jednym ruchu.", "You stay with one movement.", "maniak-techniki"),
            ("Nadal kogoś trzymasz.", "You are still holding someone.", "mistrz-przytulania"),
        ],
    },
    {
        "sort_order": 3,
        "text_pl": "Co Cię cieszy po miesiącu?",
        "text_en": "What pleases you after a month?",
        "choices": [
            ("Że już wiesz, jak stać z bronią.", "That you know how to stand with a weapon.", "chce-miecz"),
            ("Że oddech wraca szybciej.", "That your breath comes back faster.", "jeszcze-jedna-runda"),
            ("Że jeden chwyt wreszcie siada.", "That one grip finally lands.", "maniak-techniki"),
            ("Że pas ma inny kolor.", "That the belt is a different colour.", "po-pas"),
        ],
    },
    {
        "sort_order": 4,
        "text_pl": "Ktoś myli zasady. Twoja pierwsza myśl?",
        "text_en": "Someone mixes up the rules. Your first thought?",
        "choices": [
            ("Regulamin jest na ścianie.", "The rulebook is on the wall.", "rycerz-regulaminu"),
            ("Nieważne, jeszcze runda.", "Never mind, another round.", "jeszcze-jedna-runda"),
            ("Pokaż to wolniej.", "Show it more slowly.", "maniak-techniki"),
            ("I tak Was zaraz złapię.", "I am going to grab you anyway.", "mistrz-przytulania"),
        ],
    },
    {
        "sort_order": 5,
        "text_pl": "Jaki prezent z sali miałby sens?",
        "text_en": "What gift from the hall would make sense?",
        "choices": [
            ("Cokolwiek z jelcem.", "Anything with a guard.", "chce-miecz"),
            ("Rękawice, które już śmierdzą.", "Gloves that already smell.", "jeszcze-jedna-runda"),
            ("Notes na detale.", "A notebook for details.", "maniak-techniki"),
            ("Kolejny pas, nawet za wcześnie.", "Another belt, even if it is early.", "po-pas"),
        ],
    },
    {
        "sort_order": 6,
        "text_pl": "Sparing się sypie. Co ratujesz?",
        "text_en": "The sparring falls apart. What do you save?",
        "choices": [
            ("Dystans i linię.", "The distance and the line.", "rycerz-regulaminu"),
            ("Tempo.", "The pace.", "jeszcze-jedna-runda"),
            ("Ten jeden detal, który jeszcze działa.", "The one detail that still works.", "maniak-techniki"),
            ("Uchwyt.", "The grip.", "mistrz-przytulania"),
        ],
    },
    {
        "sort_order": 7,
        "text_pl": "Gdzie siadasz na trybunie?",
        "text_en": "Where do you sit in the stands?",
        "choices": [
            ("Tam, gdzie widać broń.", "Where the weapon is visible.", "chce-miecz"),
            ("Jak najbliżej, żeby słyszeć rundę.", "As close as possible, to hear the round.", "jeszcze-jedna-runda"),
            ("Z kartką.", "With a piece of paper.", "maniak-techniki"),
            ("Tam, gdzie sędzia mówi przepisy.", "Where the referee states the rules.", "rycerz-regulaminu"),
        ],
    },
    {
        "sort_order": 8,
        "text_pl": "Znajomy pyta, po co Ci to. Odpowiedź?",
        "text_en": "A friend asks why you do this. Your answer?",
        "choices": [
            ("Bo chcę miecz. Tyle.", "Because I want a sword. That is all.", "chce-miecz"),
            ("Bo jeszcze jedna runda.", "Because of one more round.", "jeszcze-jedna-runda"),
            ("Bo pas wisi w domu.", "Because the belt hangs at home.", "po-pas"),
            ("Bo lubię, kiedy ktoś nie ucieka z uchwytu.", "Because I like it when someone does not slip the grip.", "mistrz-przytulania"),
        ],
    },
]
