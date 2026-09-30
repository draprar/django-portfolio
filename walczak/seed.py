"""Starter catalog and quiz. A data migration calls load() with historical models."""

from __future__ import annotations

from typing import Any

STYLES: list[dict[str, Any]] = [
    {
        "slug": "boks",
        "sort_order": 1,
        "family": "uderzenia",
        "name_pl": "Boks",
        "name_en": "Boxing",
        "joke_pl": "Masz sprawę do załatwienia i nie lubisz, gdy ktoś jej nie kończy.",
        "joke_en": "You have a thing to settle and you dislike it when someone will not finish it.",
        "summary_pl": "Boks to walka na pięści w ringu, w rękawicach, na punkty albo przed czasem. Ciosy idą w głowę i tułów. Klincz się rozdziela, a nogi służą do pracy nóg, nie do kopnięć.",
        "summary_en": "Boxing is a gloved fist fight in a ring, scored on points or ended early. Punches go to the head and the torso. The clinch is broken, and the feet are for footwork, not for kicks.",
        "history_pl": "Nowoczesny boks wyrósł z walk na gołe pięści w Anglii. Reguły markiza Queensberry z 1867 roku wprowadziły rękawice i rundy. Stąd wzięła się forma, którą dziś widać na ringu amatorskim i zawodowym.",
        "history_en": "Modern boxing grew out of bare-knuckle fights in England. The 1867 Marquess of Queensberry rules brought in gloves and rounds. That is the form you see today in the amateur ring and in the professional game.",
        "practice_pl": "Stoisz w gardzie, pracujesz nogami i szukasz prostego, sierpowego albo haka. Obrona to unik, blok i klincz. Trening to łapy, worek i sparing.",
        "practice_en": "You stand in a guard, move your feet, and look for the jab, the cross, or the hook. Defense is the slip, the block, and the clinch. Training is pads, the bag, and sparring.",
        "sources": [
            {
                "author": "Encyclopaedia Britannica",
                "title": "Boxing",
                "url": "https://www.britannica.com/sports/boxing",
            }
        ],
    },
    {
        "slug": "kickboxing",
        "sort_order": 2,
        "family": "uderzenia",
        "name_pl": "Kickboxing",
        "name_en": "Kickboxing",
        "joke_pl": "Ręce to za mało. Nogi i tak wchodzą do rozmowy.",
        "joke_en": "Hands are not enough. The legs join the conversation anyway.",
        "summary_pl": "Kickboxing łączy pięści z kopnięciami, zwykle powyżej pasa. Stójka jest bliska boksowi, tylko tarcza jest większa, bo dochodzi goleń i stopa. Parteru nie ma.",
        "summary_en": "Kickboxing joins punches with kicks, usually above the waist. The stance is close to boxing, but the target is larger, because the shin and the foot are in play. There is no ground fight.",
        "history_pl": "W XX wieku japońskie i amerykańskie formuły pełnokontaktowe złożyły boks z kopnięciami karate. Nazwa została przy walkach w ringu, bez klinczu muay thai i bez walki w parterze.",
        "history_en": "In the twentieth century Japanese and American full-contact formats folded boxing together with karate kicks. The name stuck to ring fights without the Muay Thai clinch and without ground fighting.",
        "practice_pl": "Zostajesz w stójce. Kopnięcia okrężne, frontalne i niskie, plus pięści. Sprawdzenie to osłona i odskok, nie zejście na ziemię.",
        "practice_en": "You stay standing. Round kicks, front kicks, and the low kick, plus punches. Defense is the shell and the step-out, not a trip to the ground.",
        "sources": [
            {
                "author": "Encyclopaedia Britannica",
                "title": "Kickboxing",
                "url": "https://www.britannica.com/sports/kickboxing",
            }
        ],
    },
    {
        "slug": "muay-thai",
        "sort_order": 3,
        "family": "uderzenia",
        "name_pl": "Muay thai",
        "name_en": "Muay Thai",
        "joke_pl": "Blisko, łokcie, kolana. Grzeczność zostaje w szatni.",
        "joke_en": "Close range, elbows, knees. Manners stay in the locker room.",
        "summary_pl": "Muay thai to tajski boks: pięści, łokcie, kolana i golenie. Wolno trzymać w klinczu i stamtąd uderzać kolanem. Parteru nie ma.",
        "summary_en": "Muay Thai is Thai boxing: fists, elbows, knees, and shins. You may hold in the clinch and strike with the knee from there. There is no ground fight.",
        "history_pl": "Korzenie są w tajskim treningu wojskowym i w walkach na lokalnych festynach. W XX wieku doszły rękawice, rundy i ring, ale rytuał przed walką, ram muay, został.",
        "history_en": "The roots are in Thai military training and in bouts at local fairs. The twentieth century added gloves, rounds, and the ring, but the pre-fight ritual, the ram muay, stayed.",
        "practice_pl": "Dużo klinczu i kopnięć golenią w udo. Łokieć schodzi z bliska. Na początek zostaje ciężki worek, tarcze i technika bez pełnej mocy.",
        "practice_en": "A lot of clinch work and shin kicks to the thigh. The elbow comes in from close range. The start is the heavy bag, the pads, and technique without full power.",
        "sources": [
            {
                "author": "Encyclopaedia Britannica",
                "title": "Thailand: Sports and recreation",
                "url": "https://www.britannica.com/place/Thailand/Sports-and-recreation",
            }
        ],
    },
    {
        "slug": "karate",
        "sort_order": 4,
        "family": "uderzenia",
        "name_pl": "Karate",
        "name_en": "Karate",
        "joke_pl": "Lubisz, gdy ruch ma kształt, a sala ma rząd.",
        "joke_en": "You like it when a movement has a shape and the hall has a line.",
        "summary_pl": "Karate to okinawska i japońska sztuka uderzeń: pięść, otwarta dłoń, łokieć, kolano i kopnięcie. W zależności od stylu jest forma (kata), umówiony sparring albo walka na punkty.",
        "summary_en": "Karate is an Okinawan and Japanese striking art: fist, open hand, elbow, knee, and kick. Depending on the style there is the form (kata), agreed sparring, or a points contest.",
        "history_pl": "Na Okinawie lokalne metody bicia złożyły się z chińskimi wpływami. W XX wieku Funakoshi i inni przenieśli karate do Japonii, a stamtąd na sale całego świata.",
        "history_en": "On Okinawa local striking methods mixed with Chinese influence. In the twentieth century Funakoshi and others carried karate to Japan, and from there into halls worldwide.",
        "practice_pl": "Najpierw pozycja i kata, potem kumite. Cios ma dojść i wrócić, a nie zostać w klinczu. W wersji sportowej często wygrywa czyste trafienie.",
        "practice_en": "First the stance and the kata, then kumite. A strike is meant to land and return, not to stay in a clinch. In the sporting version a clean hit often wins.",
        "sources": [
            {
                "author": "Encyclopaedia Britannica",
                "title": "Karate",
                "url": "https://www.britannica.com/sports/karate",
            }
        ],
    },
    {
        "slug": "judo",
        "sort_order": 5,
        "family": "chwyty",
        "name_pl": "Judo",
        "name_en": "Judo",
        "joke_pl": "Wolisz rzucić problem na ziemię niż go tłumaczyć.",
        "joke_en": "You would rather throw the problem to the ground than explain it.",
        "summary_pl": "Judo jest japońską walką w chwycie. Wygrywa rzut na plecy, trzymanie albo dźwignia na rękę. Uderzeń nie ma.",
        "summary_en": "Judo is a Japanese grappling contest. A win is a throw onto the back, a hold-down, or an armlock. There are no strikes.",
        "history_pl": "Jigoro Kano ułożył judo pod koniec XIX wieku ze starszego jujutsu, z myślą o szkole, nie o ulicy. Judogi i kategorie wagowe to już warstwa sportowa.",
        "history_en": "Jigoro Kano arranged judo at the end of the nineteenth century out of older jujutsu, with school in mind, not the street. The judogi and the weight classes are the sporting layer.",
        "practice_pl": "Łapiesz za kimono, burzysz równowagę i rzucasz. Na ziemi trzymasz albo szukasz dźwigni, która jest w regulaminie. Randori to sparring, w którym oboje polują na rzut.",
        "practice_en": "You grip the jacket, break the balance, and throw. On the ground you hold or look for a legal armlock. Randori is sparring in which both of you hunt the throw.",
        "sources": [
            {
                "author": "Encyclopaedia Britannica",
                "title": "Judo",
                "url": "https://www.britannica.com/sports/judo",
            }
        ],
    },
    {
        "slug": "zapasy",
        "sort_order": 6,
        "family": "chwyty",
        "name_pl": "Zapasy",
        "name_en": "Wrestling",
        "joke_pl": "Lubisz się trzymać. Czasem dosłownie.",
        "joke_en": "You like to hold on. Sometimes literally.",
        "summary_pl": "Zapasy to walka o przewrócenie albo o przyciśnięcie łopatek, bez uderzeń. W stylu klasycznym pracują ramiona i tułów. W wolnym dochodzą nogi.",
        "summary_en": "Wrestling is a contest to take someone down or to pin the shoulders, without strikes. In Greco-Roman the arms and the torso do the work. In freestyle the legs join in.",
        "history_pl": "Zapasy są starsze niż regulamin. Wersja olimpijska ułożyła się w XIX i XX wieku w dwa style: klasyczny i wolny. Trykot i mata zastąpiły gołą ziemię.",
        "history_en": "Wrestling is older than the rulebook. The Olympic version settled in the nineteenth and twentieth centuries into two styles: Greco-Roman and freestyle. The singlet and the mat replaced bare ground.",
        "practice_pl": "Schodzisz niżej, łapiesz za kark, ramię albo nogę i ściągasz ciężar za swoje biodro. Potem albo przytrzymujesz, albo wstajesz do kolejnej akcji.",
        "practice_en": "You change level, catch the neck, an arm, or a leg, and pull the weight past your hip. Then you either hold the pin or stand up for the next shot.",
        "sources": [
            {
                "author": "Encyclopaedia Britannica",
                "title": "Wrestling",
                "url": "https://www.britannica.com/sports/wrestling",
            }
        ],
    },
    {
        "slug": "bjj",
        "sort_order": 7,
        "family": "chwyty",
        "name_pl": "Brazylijskie jiu-jitsu",
        "name_en": "Brazilian jiu-jitsu",
        "joke_pl": "Jak już kogoś złapiesz, to tłumaczysz leżąc.",
        "joke_en": "Once you have a hold of someone, you do the explaining from the floor.",
        "summary_pl": "Brazylijskie jiu-jitsu szuka poddania: dźwigni albo duszenia. Większość pracy jest w parterze. W sportowej formie uderzeń nie ma, chyba że dany regulamin je dopuści.",
        "summary_en": "Brazilian jiu-jitsu looks for the submission: a joint lock or a choke. Most of the work is on the ground. The sporting form has no strikes, unless that rule set allows them.",
        "history_pl": "Mitsuyo Maeda przywiózł judo i jujutsu do Brazylii. Rodzina Gracie rozwinęła z tego walkę, w której mniejszy może wygrać z pozycji na ziemi. Stąd pasy oraz turnieje w gi i bez gi.",
        "history_en": "Mitsuyo Maeda brought judo and jujutsu to Brazil. The Gracie family grew from that a fight in which a smaller person can win from the ground. Belts and both gi and no-gi tournaments come from there.",
        "practice_pl": "Przechodzisz gardę, bierzesz plecy albo montujesz i szukasz ręki lub szyi. Do tego dochodzi ucieczka, gdy to Ty jesteś pod spodem. Sparing trwa długo i bez pośpiechu.",
        "practice_en": "You pass the guard, take the back, or mount, and look for an arm or the neck. Then there is the escape, for when you are the one underneath. Sparring runs long and without a rush.",
        "sources": [
            {
                "author": "International Brazilian Jiu-Jitsu Federation",
                "title": "IBJJF",
                "url": "https://ibjjf.com/",
            }
        ],
    },
    {
        "slug": "mma",
        "sort_order": 8,
        "family": "mieszane",
        "name_pl": "MMA",
        "name_en": "MMA",
        "joke_pl": "Z ulicy, z sali, byle działało tego dnia.",
        "joke_en": "From the street or from the gym, as long as it works that day.",
        "summary_pl": "MMA składa stójkę i parter w jednej walce. Wolno bić i wolno walczyć o poddanie, w granicach regulaminu danej organizacji. To nie jest jeden styl, tylko zestaw dozwolonych narzędzi.",
        "summary_en": "MMA puts the stand-up and the ground into one fight. Striking and submission grappling are both allowed, inside that promotion rules. It is not one style. It is a set of permitted tools.",
        "history_pl": "Walki mieszane mają starszych poprzedników, od vale tudo po japońskie shoot. Współczesna forma ułożyła się w latach dziewięćdziesiątych, gdy doszły rękawice i ciaśniejszy regulamin.",
        "history_en": "Mixed fights have older predecessors, from vale tudo to Japanese shoot. The current form settled in the 1990s, when gloves and a tighter rule set arrived.",
        "practice_pl": "Trenuje się kilka rzeczy naraz: pięści, zapasy, zejście na ziemię i obronę duszenia. Wygrywa ten, kto łączy je w jednej akcji, a nie ten, kto umie tylko jedną.",
        "practice_en": "You train several things at once: punches, wrestling, the takedown, and choke defense. The win goes to the person who joins them in one sequence, not to the person who knows only one.",
        "sources": [
            {
                "author": "Encyclopaedia Britannica",
                "title": "Mixed martial arts",
                "url": "https://www.britannica.com/sports/mixed-martial-arts",
            }
        ],
    },
    {
        "slug": "szermierka",
        "sort_order": 9,
        "family": "bron",
        "name_pl": "Szermierka",
        "name_en": "Fencing",
        "joke_pl": "Wolisz dystans. Niech drugi zrobi pierwszy krok.",
        "joke_en": "You prefer the distance. Let the other one take the first step.",
        "summary_pl": "Szermierka sportowa to pojedynek na floret, szpadę albo szablę. Trafienie rejestruje lampka. Chodzi o pierwszeństwo i o dystans, nie o siłę ciosu.",
        "summary_en": "Sport fencing is a bout with the foil, the epee, or the sabre. A light records the touch. It is about right of way and distance, not about the force of the hit.",
        "history_pl": "Wyrosła z europejskiej walki bronią białą. W XIX i XX wieku maska, strój i elektryczny sędzia zamieniły pojedynek w sport olimpijski o trzech broniach.",
        "history_en": "It grew out of European sword fighting. In the nineteenth and twentieth centuries the mask, the jacket, and the electric judge turned the duel into an Olympic sport with three weapons.",
        "practice_pl": "Praca nóg, wypad i złożenia. We florecie i szabli liczy się, kto ma akcję. W szpadzie liczy się, kto trafi pierwszy, nawet gdy oboje ruszają.",
        "practice_en": "Footwork, the lunge, and compound attacks. In foil and sabre it matters who owns the phrase. In epee it matters who arrives first, even if both move.",
        "sources": [
            {
                "author": "Encyclopaedia Britannica",
                "title": "Fencing",
                "url": "https://www.britannica.com/sports/fencing",
            }
        ],
    },
    {
        "slug": "capoeira",
        "sort_order": 10,
        "family": "uderzenia",
        "name_pl": "Capoeira",
        "name_en": "Capoeira",
        "joke_pl": "Najpierw rytm, potem kopniak, i najlepiej z uśmiechem.",
        "joke_en": "Rhythm first, then the kick, and a smile if you can manage it.",
        "summary_pl": "Capoeira to afrobrazylijska gra: kopnięcia, uniki, akrobacja i muzyka. W roda ludzie wchodzą parami do koła, a berimbau nadaje tempo. Bywa zabawą i bywa walką.",
        "summary_en": "Capoeira is an Afro-Brazilian game: kicks, evasions, acrobatics, and music. In the roda people enter the circle in pairs, and the berimbau sets the pace. It can be play and it can be a fight.",
        "history_pl": "Ułożyła się w Brazylii wśród zniewolonych Afrykanów i ich potomków. Przez część XIX i XX wieku była ścigana, potem weszła do szkół i na pokazy.",
        "history_en": "It took shape in Brazil among enslaved Africans and their descendants. For part of the nineteenth and twentieth centuries it was outlawed, then it entered schools and demonstrations.",
        "practice_pl": "Ginga, czyli kołysanie, jest bazą. Z niej schodzi kopnięcie i unik. Do tego dochodzi śpiew i instrumenty, więc trening bez muzyki jest tylko połową rzeczy.",
        "practice_en": "The ginga, the sway, is the base. The kick and the evasion leave from there. Song and instruments come with it, so training without the music is only half of the thing.",
        "sources": [
            {
                "author": "Encyclopaedia Britannica",
                "title": "Capoeira",
                "url": "https://www.britannica.com/art/capoeira",
            }
        ],
    },
]

QUESTIONS: list[dict[str, Any]] = [
    {
        "sort_order": 1,
        "text_pl": "Ktoś wchodzi Ci w drogę. Co robisz?",
        "text_en": "Someone steps into your way. What do you do?",
        "choices": [
            {
                "sort_order": 1,
                "text_pl": "Idziesz prosto. Sprawa ma się skończyć.",
                "text_en": "You go straight in. The thing has to end.",
                "style": "boks",
                "points": 3,
                "extra_style": "kickboxing",
                "extra_points": 1,
            },
            {
                "sort_order": 2,
                "text_pl": "Łapiesz i nie puszczasz.",
                "text_en": "You grab on and you do not let go.",
                "style": "zapasy",
                "points": 3,
                "extra_style": "judo",
                "extra_points": 1,
            },
            {
                "sort_order": 3,
                "text_pl": "Cofasz się i czekasz na jego krok.",
                "text_en": "You step back and wait for their move.",
                "style": "szermierka",
                "points": 3,
            },
            {
                "sort_order": 4,
                "text_pl": "Uśmiechasz się i zmieniasz rytm.",
                "text_en": "You smile and change the rhythm.",
                "style": "capoeira",
                "points": 3,
            },
        ],
    },
    {
        "sort_order": 2,
        "text_pl": "Gdzie lubisz być, gdy robi się ciasno?",
        "text_en": "Where do you like to be when it gets crowded?",
        "choices": [
            {
                "sort_order": 1,
                "text_pl": "Na nogach, na dystansie pięści.",
                "text_en": "On your feet, at fist range.",
                "style": "boks",
                "points": 2,
                "extra_style": "kickboxing",
                "extra_points": 2,
            },
            {
                "sort_order": 2,
                "text_pl": "W klinczu. Łokcie i kolana.",
                "text_en": "In the clinch. Elbows and knees.",
                "style": "muay-thai",
                "points": 3,
                "extra_style": "zapasy",
                "extra_points": 1,
            },
            {
                "sort_order": 3,
                "text_pl": "Na ziemi, aż druga strona przestanie.",
                "text_en": "On the ground, until the other side stops.",
                "style": "bjj",
                "points": 3,
                "extra_style": "judo",
                "extra_points": 1,
            },
            {
                "sort_order": 4,
                "text_pl": "Tam, gdzie regulamin jest luźniejszy.",
                "text_en": "Wherever the rulebook is looser.",
                "style": "mma",
                "points": 3,
            },
        ],
    },
    {
        "sort_order": 3,
        "text_pl": "Co Cię męczy najszybciej?",
        "text_en": "What wears you out first?",
        "choices": [
            {
                "sort_order": 1,
                "text_pl": "Leżenie i siłowanie.",
                "text_en": "Lying down and grinding.",
                "style": "boks",
                "points": 2,
                "extra_style": "szermierka",
                "extra_points": 2,
            },
            {
                "sort_order": 2,
                "text_pl": "Stanie i wymienianie ciosów.",
                "text_en": "Standing there and trading shots.",
                "style": "judo",
                "points": 2,
                "extra_style": "bjj",
                "extra_points": 2,
            },
            {
                "sort_order": 3,
                "text_pl": "Sztywny rząd i ukłony.",
                "text_en": "A stiff line and the bows.",
                "style": "mma",
                "points": 2,
                "extra_style": "muay-thai",
                "extra_points": 1,
            },
            {
                "sort_order": 4,
                "text_pl": "Powaga bez muzyki.",
                "text_en": "Seriousness without music.",
                "style": "capoeira",
                "points": 3,
            },
        ],
    },
    {
        "sort_order": 4,
        "text_pl": "Skąd bierzesz ruch?",
        "text_en": "Where do you get the movement from?",
        "choices": [
            {
                "sort_order": 1,
                "text_pl": "Z sali, z formy, z pasa.",
                "text_en": "From the hall, the form, the belt.",
                "style": "karate",
                "points": 3,
                "extra_style": "judo",
                "extra_points": 1,
            },
            {
                "sort_order": 2,
                "text_pl": "Z ulicy, byle się dało.",
                "text_en": "From the street, as long as it works.",
                "style": "mma",
                "points": 3,
                "extra_style": "kickboxing",
                "extra_points": 1,
            },
            {
                "sort_order": 3,
                "text_pl": "Z ostrza i z dystansu.",
                "text_en": "From the blade and from the distance.",
                "style": "szermierka",
                "points": 3,
            },
            {
                "sort_order": 4,
                "text_pl": "Z bębna, nie z regulaminu.",
                "text_en": "From the drum, not from the rulebook.",
                "style": "capoeira",
                "points": 2,
                "extra_style": "muay-thai",
                "extra_points": 1,
            },
        ],
    },
    {
        "sort_order": 5,
        "text_pl": "Jak kończysz, gdy już trzymasz?",
        "text_en": "How do you finish once you have a hold?",
        "choices": [
            {
                "sort_order": 1,
                "text_pl": "Nie trzymam. Uderzam i odchodzę.",
                "text_en": "I do not hold. I hit and I leave.",
                "style": "kickboxing",
                "points": 2,
                "extra_style": "boks",
                "extra_points": 2,
            },
            {
                "sort_order": 2,
                "text_pl": "Rzut i koniec.",
                "text_en": "A throw, and that is the end.",
                "style": "judo",
                "points": 3,
                "extra_style": "zapasy",
                "extra_points": 1,
            },
            {
                "sort_order": 3,
                "text_pl": "Trzymam dalej i szukam dźwigni.",
                "text_en": "I keep the hold and look for a lock.",
                "style": "bjj",
                "points": 3,
            },
            {
                "sort_order": 4,
                "text_pl": "Kolanem, skoro i tak jesteśmy blisko.",
                "text_en": "With the knee, since we are already close.",
                "style": "muay-thai",
                "points": 3,
            },
        ],
    },
    {
        "sort_order": 6,
        "text_pl": "Czego szukasz w tym walczeniu?",
        "text_en": "What are you looking for in the fighting?",
        "choices": [
            {
                "sort_order": 1,
                "text_pl": "Jednej czystej rzeczy, dobrze zrobionej.",
                "text_en": "One clean thing, done well.",
                "style": "karate",
                "points": 2,
                "extra_style": "boks",
                "extra_points": 1,
            },
            {
                "sort_order": 2,
                "text_pl": "Ścisku. Ludzie i tak się trzymają, tylko bez zasad.",
                "text_en": "A clinch. People hold on anyway, only without rules.",
                "style": "zapasy",
                "points": 3,
            },
            {
                "sort_order": 3,
                "text_pl": "Żeby wolno było prawie wszystko.",
                "text_en": "For almost everything to be allowed.",
                "style": "mma",
                "points": 2,
                "extra_style": "muay-thai",
                "extra_points": 1,
            },
            {
                "sort_order": 4,
                "text_pl": "Żeby dało się odsunąć, zanim ktoś wejdzie.",
                "text_en": "To be able to step off before someone comes in.",
                "style": "szermierka",
                "points": 2,
                "extra_style": "karate",
                "extra_points": 1,
            },
        ],
    },
]


def load(style_model: Any, source_model: Any, question_model: Any, choice_model: Any) -> None:
    if style_model.objects.exists():
        return
    by_slug = {}
    for row in STYLES:
        sources = row["sources"]
        fields = {key: value for key, value in row.items() if key != "sources"}
        style = style_model.objects.create(active=True, **fields)
        by_slug[style.slug] = style
        for index, source in enumerate(sources, start=1):
            source_model.objects.create(style=style, sort_order=index, **source)
    for row in QUESTIONS:
        question = question_model.objects.create(
            text_pl=row["text_pl"],
            text_en=row["text_en"],
            sort_order=row["sort_order"],
            active=True,
        )
        for choice in row["choices"]:
            extra = choice.get("extra_style")
            choice_model.objects.create(
                question=question,
                text_pl=choice["text_pl"],
                text_en=choice["text_en"],
                sort_order=choice["sort_order"],
                style=by_slug[choice["style"]],
                points=choice["points"],
                extra_style=by_slug[extra] if extra else None,
                extra_points=choice.get("extra_points", 0),
            )
