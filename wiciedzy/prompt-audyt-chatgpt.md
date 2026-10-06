# Prompt audytu wiciędze (ChatGPT) — stan po drugim przejściu korekcyjnym

Wklej **cały ten plik** do ChatGPT (lub załącz jako plik). Model ma przeprowadzić audyt jak na początku projektu, ale na **aktualnym** materiale.

---

## Kontekst techniczny (nie oceniaj kodu Django, tylko treść i spójność)

- Aplikacja: **wiciędze** (`/wiciedze/`), katalog **40** stylów w bazie (30 core + 10 golden). Import: `CORE` + `GOLDEN` z `styles.py`, pola About/History/Practice **nadpisuje** `PROSE` z `prose.py`.
- **Lustro redakcyjne:** `katalog-opisy.md` ma **46** opisów stylów + sekcje „Do sprawdzenia” i meta; **6 kart jest tylko w MD** (nie w imporcie): Taekkyeon, Taijiquan, Catch wrestling, Luta livre esportiva, Iaido, Kyudo.
- **Fakty** i **relacje** między kartami są tylko w `styles.py` (6 faktów, 4 relacje w imporcie). Notatka Zapasy→Catch jest w MD przy Wrestling; w bazie relacji zapasy→catch **nie ma** (brak sluga catch).
- **5 kart** ma flagę `sources_disagree` (baner: źródła niejasne): taekwondo, wushu, hapkido, hema, kalaripayattu.
- Parasole (umbrella): karate, wushu, arnis, jujutsu, silat.
- Quiz dopasowania: preferencje + profile 22 osi (nie pokazywane użytkowniku jako liczby). Osobny plik quizu poniżej.
- Język: pary **EN nad PL** w katalogu MD; na stronie domyślnie PL z `data-en` / `data-pl`. Nie proponuj profilu 1–5 ani „niski/średni/wysoki” w opisach kart.

---



## Zadanie — przeprowadź pełny audyt (wszystkie aspekty)



### I. Katalog stylów (priorytet: sekcja B = MD; sekcja A = co faktycznie widzi użytkownik)

1. **Wiarygodność merytoryczna.** Przy każdej uwadze: karta (nazwa PL), zdanie lub teza, co jest słabe, **źródło** (federacja, UNESCO, regulamin, encyklopedia). Oznacz też zdania poprawne (bez cytowania całych akapitów). Sprawdź m.in. ostatnie poprawki: PERSILAT 2026 (Tanding/Jurus), WT/ITF, zapasy olimpijskie (kobiety = freestyle), lethwei (owijki vs rękawice), bökh (lokalne zasady końca), brak „seni” jako kategorii nadrzędnej.
2. **Granice kart i parasole.** Co słusznie w jednej karcie, co zdublowane, co jedna nazwa a wiele regulaminów. Odnieś się do 40 vs 46: czy 6 kart „tylko MD” powinno wejść do aplikacji, czy zostać w MD.
3. **Braki.** Propozycje sportów/sztuk których nie ma — odmiana istniejącej karty vs nowa karta. Bez inflacji nazw szkół.
4. **PL wobec EN.** Gdzie polski gubi, zaostrza lub przekręca angielski. Nie wygładzaj stylu jeśli sens się zgadza.
5. **Głos i forma.** Krótkie zdania sprawdzalne; bez żartów w opisach kart; bez ocen „jak bardzo kontaktowe”.
6. **Źródła i „Do sprawdzenia”.** Czy drugie źródło to discovery; czy fakty mają sensowne URL; czy sekcja „Do sprawdzenia” w B jest aktualna (arnis + RA 9850, lethwei Unified Ruleset SOURCE GAP, itd.).
7. **Spójność warstw.** Różnice między **A (eksport UI)** a **B (katalog-opisy.md)** dla tych samych slugów — czy PROSE/import zgadza się z lustrem redakcyjnym.
8. **Fakty i relacje (sekcja D).** Czy 6 faktów i 4 relacje są trafne; czego brakuje (np. catch przy zapasach); czy `is_legend` jest używane uczciwie.



### II. Quizopasowanie (sekcja C)

Wykonaj **dokładnie** polecenie z nagłówka pliku quizu (4 punkty: mechanizm, jakość pytań i zdań wyniku, PL/EN, rozszerzenia tylko gdy zmieniają listę). Nie przepisuj quizu. Nie dodawaj testu osobowości ani skali skuteczności.

### III. Teksty UI poza kartami (sekcja A — home, spis, test, dopasowanie, porównaj, 404)

1. **UI i obietnice.** Czy home/quiz/katalog nie obiecują więcej niż mechanizm daje; ton PL (np. „se poklikaj”, tagline); dostępność sensu bez kontekstu kodu.
2. **Porównanie i dopasowanie.** Czy copy przy legendzie, „do poczytania”, brak psychometrii — spójne i uczciwe.



### IV. Humor / IPIP (jeśli występują w eksportie A)

1. Jeśli eksport zawiera pytania IPIP lub humor — krótko: czy nie mylą się z quizem dopasowania i czy PL/EN jest spójne. Jeśli brak w eksportcie — pomiń.

---



## Format odpowiedzi ChatGPT

Pogrupuj:

1. **Błędy merytoryczne** (karta → problem → źródło lub SOURCE GAP)
2. **Sporne granice kart / 40 vs 46**
3. **Rozjazdy PL/EN**
4. **Niespójność A (UI) vs B (MD) vs D (fakty/relacje)**
5. **Quiz — błędy mechanizmu / słabe pytania / propozycje**
6. **UI i obietnice**
7. **Propozycje braków** (odmiana vs nowa karta)
8. **Co jest w porządku** (krótko)
9. **Nie dało się sprawdzić** (lista)

Nie przepisuj całego katalogu. Nie dodawaj profilu liczbowego 1–5 do opisów.

---



# DANE DO AUDYTU



## Sekcja D — fakty i relacje (import)

```python
RELATIONS: list[dict] = [
    {
        "from": "kyokushin",
        "to": "karate",
        "kind": "variant",
        "note_pl": "Kyokushin to pełnokontaktowa odmiana karate, a nie osobna tradycja spoza karate.",
        "note_en": "Kyokushin is a full-contact style of karate, not a tradition from outside karate.",
        "source_urls": ["https://en.wikipedia.org/wiki/Kyokushin", "https://www.britannica.com/sports/karate"],
    },
    {
        "from": "sanda",
        "to": "wushu",
        "kind": "modern_form",
        "note_pl": "Sanda to współczesny sport związany z wushu, a nie podstyl równy wszystkim tradycyjnym formom kung fu.",
        "note_en": "Sanda is a contemporary sport tied to wushu, not a substyle equal to every traditional kung fu form.",
        "source_urls": ["https://www.iwuf.org/"],
    },
    {
        "from": "bjj",
        "to": "judo",
        "kind": "influenced",
        "note_pl": "Część opracowań wiąże początki BJJ z judo i jujutsu, które ćwiczył Maeda. To nie jest jeden bezsporny rodowód, a dzisiejsze zawody BJJ to nie judo.",
        "note_en": "Some accounts tie the start of BJJ to the judo and jujutsu Maeda practiced. That isn't one undisputed origin, and today's BJJ contests are not judo.",
        "source_urls": ["https://en.wikipedia.org/wiki/Brazilian_jiu-jitsu", "https://www.britannica.com/sports/judo"],
    },
    {
        "from": "hema",
        "to": "szermierka",
        "kind": "related",
        "note_pl": "Szermierka sportowa i HEMA to dwie różne praktyki: w szermierce trafienia rejestruje aparatura, a HEMA odtwarza historyczne techniki z traktatów.",
        "note_en": "Both practices work with European bladed weapons, but HEMA reconstructs techniques from historical treatises, while sport fencing has three weapons and its own rules. It is not the same training.",
        "source_urls": ["https://www.hemaalliance.com/", "https://www.britannica.com/sports/fencing"],
    },
]

FACTS: list[dict] = [
    {
        "text_pl": "Reguły Queensberry z 1867 roku ujednoliciły model walki w rękawicach i rundach oraz zakazały zapasów. Wcześniejsze walki na gołe pięści dopuszczały więcej chwytów.",
        "text_en": "The 1867 Queensberry rules standardised gloved, round-based fighting and banned wrestling. Earlier bare-knuckle bouts had allowed more holding.",
        "is_legend": False,
        "styles": ["boks"],
        "source_urls": ["https://www.britannica.com/sports/boxing"],
    },
    {
        "text_pl": "Opowieść o Ng Mui i Yim Wing-chun należy do tradycji szkoły wing chun, a nie do udokumentowanej historii, na której można oprzeć dokładną datę powstania stylu.",
        "text_en": "The story of Ng Mui and Yim Wing-chun belongs to Wing Chun school tradition, not to documented history you can use to pin down an exact founding date.",
        "is_legend": True,
        "styles": ["wing-chun"],
        "source_urls": ["https://en.wikipedia.org/wiki/Wing_Chun"],
    },
    {
        "text_pl": "Naadam w Mongolii to zapasy, łucznictwo i wyścigi konne. Bökh jest jedną z tych trzech konkurencji, a nie całym świętem.",
        "text_en": "Naadam in Mongolia is wrestling, archery and horse racing. Bökh is one of those three contests, not the whole festival.",
        "is_legend": False,
        "styles": ["bokh"],
        "source_urls": ["https://en.wikipedia.org/wiki/Mongolian_wrestling"],
    },
    {
        "text_pl": "W szermierce sportowej trafienie rejestruje aparatura elektryczna. HEMA próbuje odtworzyć techniki opisane w dawnych traktatach. To dwie różne praktyki.",
        "text_en": "Sport fencing records a touch with electrical kit. HEMA tries to reconstruct techniques described in old treatises. They are two different practices.",
        "is_legend": False,
        "styles": ["szermierka", "hema"],
        "source_urls": ["https://www.britannica.com/sports/fencing", "https://www.hemaalliance.com/"],
    },
    {
        "text_pl": "W regulaminie zawodów PERSILAT z 2026 roku główne kategorie to Tanding i Jurus; Jurus obejmuje Tunggal, Ganda i Regu.",
        "text_en": "In the 2026 PERSILAT competition regulations, the main competition categories are Tanding and Jurus; Jurus includes Tunggal, Ganda and Regu.",
        "is_legend": False,
        "styles": ["silat"],
        "source_urls": [
            "https://worldpencaksilat.org/rules-regulations/",
            "https://ich.unesco.org/en/RL/traditions-of-pencak-silat-01391",
        ],
    },
    {
        "text_pl": "World Taekwondo i ITF nie stosują tego samego regulaminu. W kyorugi WT zawodnicy walczą w ochraniaczach i z elektronicznym systemem punktowania, a ITF ma własne układy i regulamin sparingu.",
        "text_en": "World Taekwondo and the ITF do not use the same rules. WT kyorugi is fought with body armour and electronic scoring, while ITF uses its own patterns and sparring rules.",
        "is_legend": False,
        "styles": ["taekwondo"],
        "source_urls": [
            "https://www.worldtaekwondo.org/",
            "https://www.itftkd.org/",
        ],
    },
]
```



## Sekcja A — eksport tekstów widocznych pod /wiciedze/ (UI + 40 kart po PROSE)



# wiciędze — teksty na stronie (obecny UI)

Wygenerowano: **2026-10-06 15:37 UTC** poleceniem `python manage.py export_wiciedzy_texts`.

Źródło: aktywne trasy w `wiciedzy/urls.py`, szablony, modele `Style` (`active=True`), `PreferenceQuestion` (`active=True`), teksty z `dimensions.py` / `display.py`.

**Nie wchodzi:** `/wiciedze/quiz/`, archetyp, `joke_`*, `_quick.html`, stary `teksty.md`. Sekcja 1 = treść w przeglądarce; SEO na końcu.

---



## 1. Teksty widoczne w przeglądarce (PL/EN)



### Wspólne: nawigacja i stopka

- Marka: **wiciędze** (bez przełącznika języka)
- Przełącznik: **PL** / **EN**

**PL:** Przejdź do treści
**EN:** Skip to content

### `/wiciedze/`

*Szablon:* `home.html` — stałe napisy; nazwy stylów i opisy z sekcji katalogu.

**PL:** Boks boks, albo kop kop
**EN:** Boxing boxing, or kick kick

**PL:** a jak już musisz to se ogarnij inne.
**EN:** and if you have to go figure out the rest.

**PL:** Katalog
**EN:** Catalog

**PL:** Obczaj różne sporty i sztuki walki. Możesz je też porównywać.
**EN:** Check out all kinds of combat sports and martial arts. You can compare them too.

**PL:** Quizopasowanie
**EN:** Quizmatch

**PL:** Se poklikaj, a dostaniesz krótką listę stylów dopasowanych do Twoich odpowiedzi.
**EN:** Click around and you get a short list of styles matched to your answers.

### `/wiciedze/spis/`

*Szablon:* `list.html` — stałe napisy; nazwy stylów i opisy z sekcji katalogu.

**PL:** Katalog
**EN:** Catalog

**PL:** Obczaj różne sporty i sztuki walki — możesz je też porównywać.
**EN:** Check out all kinds of combat sports and martial arts — you can compare them too.

**PL:** Se porównaj:
**EN:** Go on, compare:

**PL:** Pierwszy
**EN:** First

**PL:** Drugi
**EN:** Second

**PL:** Porównaj
**EN:** Compare

**PL:** Wszystkie tagi
**EN:** All tags

**PL:** Żaden styl nie ma tego tagu.
**EN:** No style has this tag.

**PL:** Pokaż wszystkie
**EN:** Show all

### `/wiciedze/spis/<styl>/`

*Szablon:* `detail.html` — stałe napisy; nazwy stylów i opisy z sekcji katalogu.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** O stylu
**EN:** About

**PL:** To nazwa zbiorcza, nie jeden regulamin, więc ten opis nie pasuje do każdej szkoły ani sali.
**EN:** It's an umbrella name, not one rule set, so this description doesn't fit every school or hall.

**PL:** Rodzaj
**EN:** Type

**PL:** Tagi
**EN:** Tags

**PL:** Pochodzenie
**EN:** Origin

**PL:** Okres
**EN:** Period

**PL:** Region
**EN:** Region

**PL:** Historia
**EN:** History

**PL:** Nie da się uczciwie podać jednej wersji, źródła są niejasne.
**EN:** There's no honest single version — the sources are unclear.

**PL:** Opis jest krótszy, bo drugie źródło tylko wspomina o tym temacie.
**EN:** The description is shorter because the second source only mentions this topic.

**PL:** Jak się walczy
**EN:** How it is fought

**PL:** Charakter treningu
**EN:** Training character

**PL:** Pokaż pełny profil
**EN:** Show the full profile

**PL:** Relacje
**EN:** Relations

**PL:** Fakty
**EN:** Facts

**PL:** Późniejsza tradycja / legenda.
**EN:** Later tradition / legend.

**PL:** Źródła
**EN:** Sources

### `/wiciedze/test/`

*Szablon:* `test.html` — stałe napisy; nazwy stylów i opisy z sekcji katalogu.

**PL:** Quizopasowanie
**EN:** Quizmatch

**PL:** Se poklikaj, a dostaniesz krótką listę stylów dopasowanych do Twoich odpowiedzi.
**EN:** Click around and you get a short list of styles matched to your answers.

**PL:** Zaznacz każdą skalę, oba wybory i sytuację. Dopiero wtedy pokaże się lista.
**EN:** Mark every scale, both choices and the situation. Only then does the list show up.

**PL:** Wymagane.
**EN:** Required.

**PL:** , wcale
**EN:** , not at all

**PL:** , bardzo
**EN:** , very much

**PL:** 1 oznacza wcale, 5 — bardzo.
**EN:** 1 means not at all, 5 — very much.

**PL:** Pokaż listę
**EN:** Show the list

### `/wiciedze/dopasowanie/`

*Szablon:* `match.html` — stałe napisy; nazwy stylów i opisy z sekcji katalogu.

**PL:** Quizopasowanie
**EN:** Quizmatch

**PL:** Do poczytania
**EN:** To read

**PL:** Pięć stylów do poczytania — od tego, który najbardziej pasuje do Twoich odpowiedzi.
**EN:** Five styles to read about — starting with the one that best matches your answers.

**PL:** To nazwa zbiorcza, nie jeden regulamin, więc ten opis nie pasuje do każdej szkoły ani sali.
**EN:** It's an umbrella name, not one rule set, so this description doesn't fit every school or hall.

**PL:** Mniej oczywiste
**EN:** Less obvious

**PL:** Blisko tego jest
**EN:** Next to this sits

### `/wiciedze/porownaj/`

*Szablon:* `compare_form.html` — stałe napisy; nazwy stylów i opisy z sekcji katalogu.

**PL:** Porównaj
**EN:** Compare

**PL:** Dwa style z zestawu głównego, jeden obok drugiego.
**EN:** Two core styles, one next to the other.

**PL:** Wybierz dwa różne style z zestawu głównego.
**EN:** Pick two different styles from the core set.

**PL:** Se porównaj:
**EN:** Go on, compare:

**PL:** Pierwszy
**EN:** First

**PL:** Drugi
**EN:** Second

### `/wiciedze/porownaj/<a>/<b>/`

*Szablon:* `compare.html` — stałe napisy; nazwy stylów i opisy z sekcji katalogu.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Historia i typ
**EN:** History and type

**PL:** To nazwa zbiorcza, nie jeden regulamin, więc ten opis nie pasuje do każdej szkoły ani sali.
**EN:** It's an umbrella name, not one rule set, so this description doesn't fit every school or hall.

**PL:** Najważniejsze różnice
**EN:** Main differences

**PL:** Techniki i trening
**EN:** Technique and training

**PL:** Psychologia / badania
**EN:** Psychology / research

### `/wiciedze/test/ (brak pytań)`

*Szablon:* `empty.html` — stałe napisy; nazwy stylów i opisy z sekcji katalogu.

**PL:** Brak pytań
**EN:** No questions

**PL:** Na razie nie mam dla Ciebie pytań. Katalog dalej czeka.
**EN:** I don't have any questions for you right now. The catalog is still waiting.

**PL:** Katalog
**EN:** Catalog

### `404 w wiciędze`

*Szablon:* `404.html` — stałe napisy; nazwy stylów i opisy z sekcji katalogu.

**PL:** Tu nic nie ma.
**EN:** There's nothing here.

**PL:** Adres nie pasuje do żadnej strony w wiciędze. Wróć na start albo obczaj katalog.
**EN:** The address doesn't match any page in wiciędze. Go back to the start or check out the catalog.

**PL:** Start
**EN:** Start

**PL:** Katalog
**EN:** Catalog

## 2. Tagi

**PL:** Broń
**EN:** Weapons

**PL:** Chwyt
**EN:** Grappling

**PL:** Historia
**EN:** Historical

**PL:** Kontakt
**EN:** Contact

**PL:** Obalenia
**EN:** Takedowns

**PL:** Parter
**EN:** Ground

**PL:** Partner
**EN:** Partner

**PL:** Rzuty
**EN:** Throws

**PL:** Samoobrona
**EN:** Self-defence

**PL:** Solo
**EN:** Solo

**PL:** Tradycja
**EN:** Tradition

**PL:** Uderzenia
**EN:** Striking

**PL:** Zawody
**EN:** Competition

## 3. Typy stylu

**PL:** Mieszane
**EN:** Hybrid

**PL:** Rekonstrukcja historyczna
**EN:** Historical reconstruction

**PL:** Samoobrona
**EN:** Self-defence

**PL:** Sport walki
**EN:** Combat sport

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Z bronią
**EN:** Weapon-based

## 4. Katalog stylów



### boks — Boks

**PL:** Boks
**EN:** Boxing

**PL:** Uderzenia
**EN:** Striking

**PL:** Boks to sport walki na pięści, rozgrywany w ringu — w rękawicach. W typowym boksie sportowym dozwolone ciosy pięścią kieruje się w określone strefy głowy i tułowia. W typowym regulaminie boksu sportowego nie ma też kopnięć ani kontynuowania walki w parterze.
**EN:** Boxing is a fist sport fought in a ring — in gloves. In typical sporting boxing, legal punches go to set zones of the head and torso. A typical sporting boxing rulebook also has no kicks and no continuing the fight on the ground.

**PL:** Anglia, walki na gołe pięści
**EN:** England, bare-knuckle prize fights

**PL:** Nowoczesne reguły od 1867
**EN:** Modern rules from 1867

**PL:** Europa
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Współczesny boks wykształcił się w Anglii z wcześniejszych walk na gołe pięści. Reguły Queensberry z 1867 roku ujednoliciły model walki w rękawicach i rundach oraz zakazały zapasów. Z czasem wykształcił się z tego osobny sport, dziś zarówno olimpijski, jak i zawodowy.
**EN:** Modern boxing took shape in England out of earlier bare-knuckle fights. The 1867 Queensberry rules standardised gloved, round-based fighting and banned wrestling. Over time that became a sport in its own right, Olympic and professional.

**PL:** Na treningu ćwiczy się trzymanie gardy, pracę nóg, uderzenia na tarczach i worku oraz sparing. W obronie liczą się uniki, bloki i krótki klincz, który rozdziela sędzia.
**EN:** Training works on holding the guard, footwork, punching on pads and the bag, and sparring. Defence means slips, blocks and a short clinch that the referee breaks.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: wysoko
**EN:** Striking: high

**PL:** Pięści: wysoko
**EN:** Punches: high

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: nisko
**EN:** Grappling: low

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: średnio
**EN:** Tradition: medium

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: wysoko
**EN:** Endurance: high

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: wysoko
**EN:** Equipment: high

**PL:** Zawody
**EN:** Competition

**PL:** Bez broni
**EN:** No weapon

**PL:** Reguły Queensberry z 1867 roku ujednoliciły model walki w rękawicach i rundach oraz zakazały zapasów. Wcześniejsze walki na gołe pięści dopuszczały więcej chwytów.
**EN:** The 1867 Queensberry rules standardised gloved, round-based fighting and banned wrestling. Earlier bare-knuckle bouts had allowed more holding.

**PL:** Boxing — Encyclopaedia Britannica
**EN:** 

**PL:** International Boxing Association — IBA
**EN:** 

### muay-thai — Muay thai

**PL:** Muay thai
**EN:** Muay Thai

**PL:** Uderzenia
**EN:** Striking

**PL:** Muay thai to tajski boks. Bywa popularyzatorsko nazywane sztuką ośmiu kończyn, ponieważ wykorzystuje pięści, łokcie, kolana i golenie. W klinczu można trzymać rywala i atakować kolanami, a w typowej walce sportowej nie ma parteru.
**EN:** Muay Thai is Thai boxing. It is often popularly called the art of eight limbs, because it uses fists, elbows, knees and shins. In the clinch you can hold your opponent and attack with knees, and in a typical sporting bout there is no ground fighting.

**PL:** Tajlandia
**EN:** Thailand

**PL:** Tradycja lokalna, sportowa forma w XX wieku
**EN:** Local tradition, sporting form in the 20th century

**PL:** Azja Południowo-Wschodnia
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Korzenie muay thai wiążą się z tajskimi tradycjami walki, treningiem wojskowym i lokalnymi zawodami; szczegóły najdawniejszego rozwoju są przedmiotem dyskusji. W XX wieku rozwinęła się współczesna forma sportowa z ringiem, rundami i rękawicami, a rytuał ram muay pozostał częścią praktyki.
**EN:** The roots of Muay Thai are tied to Thai fighting traditions, military training and local contests; the earliest development is still debated. In the twentieth century a modern sporting form grew with the ring, rounds and gloves, and the ram muay ritual stayed part of the practice.

**PL:** Pięści, kopnięcia, kolana, łokcie oraz klincz, w którym wolno trzymać rywala i atakować kolanami. Ram muay jest tańcem przed walką, nie rundą. Na macie nie ma parteru. Lethwei dokłada głowę jako broń i, w tradycyjnych formułach, używa owijek zamiast rękawic bokserskich. Kickboxing ma różne zasady dotyczące klinczu i kolan zależnie od formuły.
**EN:** Punches, kicks, knees, elbows and clinch work in which the fighter may hold and attack with knees. The ram muay is the dance before the fight, not a round. There is no ground game on the mat. Lethwei adds the head as a weapon and, in traditional formats, uses hand wraps instead of boxing gloves. Kickboxing has different rules for clinching and knees depending on the format.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: wysoko
**EN:** Striking: high

**PL:** Pięści: wysoko
**EN:** Punches: high

**PL:** Kopnięcia: wysoko
**EN:** Kicks: high

**PL:** Kolana: wysoko
**EN:** Knees: high

**PL:** Łokcie: wysoko
**EN:** Elbows: high

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: średnio
**EN:** Grappling: medium

**PL:** Klincz: wysoko
**EN:** Clinch: high

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: wysoko
**EN:** Endurance: high

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Bez broni
**EN:** No weapon

**PL:** Lethwei
**EN:** Lethwei

**PL:** Lethwei i muay thai używają podobnych kończyn, ale tradycyjne lethwei dokłada głowę i często zdejmuje rękawicę.
**EN:** Lethwei and Muay Thai use a similar set of limbs, but traditional lethwei adds the head and often takes the glove away.

**PL:** Kickboxing
**EN:** Kickboxing

**PL:** Część formuł kickboxingu jest bliżej muay thai, a część nie ma tego klinczu ani kolan.
**EN:** Some kickboxing formats sit closer to Muay Thai, and some have neither this clinch nor the knees.

**PL:** Muay Thai — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** International Federation of Muaythai Associations — IFMA
**EN:** 

### kickboxing — Kickboxing

**PL:** Kickboxing
**EN:** Kickboxing

**PL:** Uderzenia
**EN:** Striking

**PL:** Kickboxing to określenie obejmujące kilka formuł walki na pięści i kopnięcia oraz tradycje treningowe, a nie jeden uniwersalny regulamin. Full Contact, Low Kick i K1 Style są odrębnymi formułami ringowymi, a kickboxing holenderski jest przede wszystkim stylem walki i treningu, a nie jednym uniwersalnym regulaminem międzynarodowym. Formuły różnią się zasadami klinczu, kolan i dozwolonych celów.
**EN:** Kickboxing is an umbrella term for several striking rulesets and training traditions, not one universal sport rulebook. Full Contact, Low Kick and K1 Style are separate ring disciplines, while Dutch kickboxing is chiefly a training and fighting style rather than one universal international ruleset. Clinch rules, knees and legal targets divide the formats.

**PL:** Japonia i Stany Zjednoczone, formuły pełnokontaktowe
**EN:** Japan and the United States, full-contact formats

**PL:** XX wiek
**EN:** 20th century

**PL:** Globalny
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** W Stanach Zjednoczonych full-contact kickboxing rozwijał się obok karate punktowego. W Japonii kickboxing rozwinął się jako odrębna formuła walki na uderzenia. K-1 spopularyzowało określone połączenie pięści, kopnięć i kolan. Kickboxing holenderski stał się rozpoznawalnym stylem treningu i walki, a nie jednym międzynarodowym regulaminem.
**EN:** In the United States, full-contact kickboxing developed alongside point karate. In Japan, kickboxing developed as a distinct striking ruleset. K-1 later popularised a particular combination of punches, kicks and knees. Dutch kickboxing became a recognisable training and fighting style rather than a single international rulebook.

**PL:** Full Contact zasadniczo dopuszcza kopnięcia powyżej pasa i ogranicza klincz. Low Kick dopuszcza kopnięcia w uda. K1 Style dopuszcza kolana i ogranicza klincz zgodnie z własnym regulaminem. Szczegóły zależą od organizacji; tych formuł nie należy traktować jako wymiennych.
**EN:** Full Contact generally allows kicks above the waist and restricts the clinch. Low Kick adds legal kicks to the thighs. K1 Style permits knees and limits clinching under its rules. The details vary by organisation; these formats should not be treated as interchangeable.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: wysoko
**EN:** Striking: high

**PL:** Pięści: wysoko
**EN:** Punches: high

**PL:** Kopnięcia: wysoko
**EN:** Kicks: high

**PL:** Kolana: średnio
**EN:** Knees: medium

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: nisko
**EN:** Grappling: low

**PL:** Klincz: nisko
**EN:** Clinch: low

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: średnio
**EN:** Tradition: medium

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: wysoko
**EN:** Endurance: high

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Zawody
**EN:** Competition

**PL:** Bez broni
**EN:** No weapon

**PL:** Kickboxing — Encyclopaedia Britannica
**EN:** 

**PL:** World Association of Kickboxing Organizations — WAKO
**EN:** 

### mma — MMA

**PL:** MMA
**EN:** Mixed martial arts

**PL:** Mieszane
**EN:** Mixed

**PL:** MMA to sport, w którym w jednej walce wolno uderzać i walczyć w parterze, w granicach regulaminu organizacji. Nie ma jednej szkoły. Typowy trening składa boks albo muay thai, zapasy i brazylijskie jiu-jitsu.
**EN:** MMA is a sport in which one fight allows striking and ground fighting, inside a promotion's rules. There is no single school. A typical camp puts together boxing or Muay Thai, wrestling and Brazilian jiu-jitsu.

**PL:** Wiele starszych formuł, współczesna forma od lat 90.
**EN:** Many older formats, current form from the 1990s

**PL:** Współczesna forma od lat 90. XX wieku
**EN:** Current form from the 1990s

**PL:** Globalny
**EN:** 

**PL:** Mieszane
**EN:** Hybrid

**PL:** Sport walki
**EN:** Combat sport

**PL:** Vale tudo w Brazylii i wczesne gale w Japonii, w tym PRIDE, mieszały style, zanim nazwa MMA się utarła. Pierwsze edycje UFC nie miały standardowego podziału na kategorie wagowe i miały formułę turniejową, a lista fauli była krótsza niż we współczesnym MMA. Współczesne MMA ma rękawice, rundy, kategorie wagowe i listę fauli.
**EN:** Vale tudo in Brazil and early Japanese cards, including PRIDE, mixed styles before the name MMA stuck. The early UFC events had no standard weight classes and used a tournament format, with fewer fouls than modern MMA. Modern MMA has gloves, rounds, weight divisions and a foul list.

**PL:** Na sali osobno idą stójka, wejścia w obalenie, kontrola i poddania, a potem sparing, który to składa. Kickboxing bez obaleń albo BJJ bez ciosów nie są jeszcze walką MMA, nawet jeśli dają jej narzędzia.
**EN:** In the gym, striking, takedown entries, control and submissions are drilled apart, then sparring puts them together. Kickboxing without takedowns, or BJJ without punches, is not yet an MMA fight, even when it supplies the tools.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: wysoko
**EN:** Striking: high

**PL:** Pięści: wysoko
**EN:** Punches: high

**PL:** Kopnięcia: wysoko
**EN:** Kicks: high

**PL:** Kolana: średnio
**EN:** Knees: medium

**PL:** Łokcie: średnio
**EN:** Elbows: medium

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: wysoko
**EN:** Clinch: high

**PL:** Rzuty: średnio
**EN:** Throws: medium

**PL:** Obalenia: wysoko
**EN:** Takedowns: high

**PL:** Parter: wysoko
**EN:** Ground fighting: high

**PL:** Poddania: wysoko
**EN:** Submissions: high

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: nisko
**EN:** Tradition: low

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: wysoko
**EN:** Endurance: high

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: wysoko
**EN:** Equipment: high

**PL:** Zawody
**EN:** Competition

**PL:** Bez broni
**EN:** No weapon

**PL:** Brazylijskie jiu-jitsu
**EN:** Brazilian jiu-jitsu

**PL:** W typowym treningu MMA parter bierze się z BJJ, obok zapasów i stójki.
**EN:** In a typical MMA camp the ground game is taken from BJJ, beside wrestling and the stand-up.

**PL:** Zapasy
**EN:** Wrestling

**PL:** Zapasy są jednym z głównych źródeł obaleń w MMA, choć zawodnicy używają też judo, sambo i innych systemów grapplingowych.
**EN:** Wrestling is one of the main sources of MMA takedowns, although fighters also use judo, sambo and other grappling systems.

**PL:** Muay thai
**EN:** Muay Thai

**PL:** Stójka w MMA często bierze boks albo muay thai. Klincz kolanem nie jest jeszcze całą walką MMA.
**EN:** The stand-up in MMA often takes boxing or Muay Thai. A knee clinch is not yet the whole MMA fight.

**PL:** Mixed martial arts — Encyclopaedia Britannica
**EN:** 

**PL:** International Mixed Martial Arts Federation — IMMAF
**EN:** 

### zapasy — Zapasy

**PL:** Zapasy
**EN:** Wrestling

**PL:** Chwyty
**EN:** Grappling

**PL:** W zapasach olimpijskich mężczyźni rywalizują w stylu wolnym i klasycznym, a zapasy kobiet stosują reguły stylu wolnego. Folkstyle, catch wrestling i różne zapasy ludowe należą do szerszej rodziny zapasów, ale nie są tymi dwoma stylami olimpijskimi.
**EN:** Olympic wrestling uses freestyle and Greco-Roman for men, while women's wrestling follows freestyle rules. Folkstyle, catch wrestling and various folk wrestling traditions belong to the broader wrestling family, but they are not the two Olympic styles.

**PL:** Wiele tradycji, sport olimpijski w dwóch stylach
**EN:** Many traditions, Olympic sport in two styles

**PL:** Sportowa forma z XIX i XX wieku
**EN:** Sporting form from the 19th and 20th centuries

**PL:** Globalny
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** United World Wrestling prowadzi styl wolny i klasyczny jako sport olimpijski. Folkstyle to szkolna i akademicka formuła w Stanach, z innymi punktami za sprowadzenie i przytrzymanie. Catch wrestling to osobna linia, w której obok rzutu jest poddanie.
**EN:** United World Wrestling runs freestyle and Greco-Roman as Olympic sports. Folkstyle is the scholastic and collegiate format in the United States, with different points for a takedown and a hold. Catch wrestling is a separate line, where a submission sits beside the throw.

**PL:** W stylu wolnym chwyt może zejść na nogę. W klasycznym atak poniżej pasa jest błędem. W obu stylach przytrzymanie obu barków na macie (fall/pin) może zakończyć walkę, a regulamin przewiduje także zwycięstwo przez przewagę techniczną; w pozostałych przypadkach decydują punkty. Ciosów nie ma.
**EN:** In freestyle the grip may go to the leg. In Greco-Roman an attack below the waist is a foul. In both styles a fall (pin) can end the bout, and technical superiority can also end it under the rules; otherwise the points decide. There are no strikes.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: nisko
**EN:** Striking: low

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: średnio
**EN:** Throws: medium

**PL:** Obalenia: wysoko
**EN:** Takedowns: high

**PL:** Parter: wysoko
**EN:** Ground fighting: high

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: średnio
**EN:** Tradition: medium

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: wysoko
**EN:** Endurance: high

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Zawody
**EN:** Competition

**PL:** Bez broni
**EN:** No weapon

**PL:** Catch wrestling
**EN:** Catch wrestling

**PL:** Catch dokłada poddania. Styl wolny i klasyczny kończą się na rzucie i punktach.
**EN:** Catch adds submissions. Freestyle and Greco-Roman end on the throw and the points.

**PL:** Wrestling — Encyclopaedia Britannica
**EN:** 

**PL:** United World Wrestling — UWW
**EN:** 

### judo — Judo

**PL:** Judo
**EN:** Judo

**PL:** Chwyty
**EN:** Grappling

**PL:** Judo to japońska sztuka walki w judogi. W sportowym judo zwycięstwo może przynieść między innymi rzut, unieruchomienie albo dozwolone poddanie, zależnie od regulaminu. Uderzeń nie ma w typowej walce sportowej.
**EN:** Judo is a Japanese art fought in a judogi. In sporting judo a win can come from a throw, a hold-down or a legal submission, depending on the rules. There are no strikes in a typical sporting bout.

**PL:** Japonia, Jigoro Kano
**EN:** Japan, Jigoro Kano

**PL:** Koniec XIX wieku
**EN:** Late 19th century

**PL:** Azja Wschodnia
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Jigoro Kano ułożył judo pod koniec XIX wieku na bazie starszych szkół jujutsu, między innymi z myślą o edukacji i wychowaniu. Późniejszy sport wyczynowy zawęził część tego, co wolno na zawodach.
**EN:** Jigoro Kano arranged judo at the end of the nineteenth century out of older jujutsu schools, among other things with education in mind. Later competitive sport narrowed some of what is legal in contest.

**PL:** Chwytasz judogi przeciwnika, wytrącasz go z równowagi i rzucasz. Na ziemi możesz go unieruchomić albo szukać poddania dopuszczonego przez regulamin.
**EN:** You grip the opponent's judogi, break their balance and throw. On the ground you can hold them or look for a submission the rules allow.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: nisko
**EN:** Striking: low

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: wysoko
**EN:** Throws: high

**PL:** Obalenia: wysoko
**EN:** Takedowns: high

**PL:** Parter: średnio
**EN:** Ground fighting: medium

**PL:** Poddania: średnio
**EN:** Submissions: medium

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Bez broni
**EN:** No weapon

**PL:** Judo — Encyclopaedia Britannica
**EN:** 

**PL:** International Judo Federation — IJF
**EN:** 

### bjj — Brazylijskie jiu-jitsu

**PL:** Brazylijskie jiu-jitsu
**EN:** Brazilian jiu-jitsu

**PL:** Chwyty
**EN:** Grappling

**PL:** Brazylijskie jiu-jitsu (BJJ) szuka poddania rywala przez dźwignię albo duszenie. Większość pracy odbywa się w parterze, a w sportowym gi i no-gi uderzeń zwykle nie ma.
**EN:** Brazilian jiu-jitsu (BJJ) looks for a submission by a joint lock or a choke. Most of the work is on the ground, and sporting gi and no-gi usually have no strikes.

**PL:** Brazylia, XX wiek. Źródła wiążą początki z judo i jujutsu, które ćwiczył Maeda.
**EN:** Brazil, 20th century. Sources tie the start to judo and jujutsu practiced by Maeda.

**PL:** XX wiek
**EN:** 20th century

**PL:** Ameryka Południowa
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Część opracowań wiąże początki z judo i jujutsu, które do Brazylii przywiózł Mitsuyo Maeda, oraz z późniejszą pracą rodziny Gracie nad parterem. Nie jest to jeden bezsporny rodowód, a dzisiejsze zawody BJJ to nie judo. Szczegóły rodzinnych opowieści bywają późniejszą tradycją.
**EN:** Some accounts tie the start to the judo and jujutsu Mitsuyo Maeda brought to Brazil, and to later Gracie work on the ground. That isn't one undisputed origin, and today's BJJ contests are not judo. Details of family stories are sometimes later tradition.

**PL:** Przechodzisz gardę, bierzesz plecy albo wchodzisz w dosiad i szukasz dźwigni lub duszenia. Sparingi opierają się na ciągłej pracy z partnerem.
**EN:** You pass the guard, take the back or mount, and look for a lock or a choke. Sparring is built around continuous work with a partner.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: nisko
**EN:** Striking: low

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: średnio
**EN:** Throws: medium

**PL:** Obalenia: średnio
**EN:** Takedowns: medium

**PL:** Parter: wysoko
**EN:** Ground fighting: high

**PL:** Poddania: wysoko
**EN:** Submissions: high

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: średnio
**EN:** Tradition: medium

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: średnio
**EN:** Athletic demand: medium

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Zawody
**EN:** Competition

**PL:** Bez broni
**EN:** No weapon

**PL:** Judo
**EN:** Judo

**PL:** Część opracowań wiąże początki BJJ z judo i jujutsu, które ćwiczył Maeda. To nie jest jeden bezsporny rodowód, a dzisiejsze zawody BJJ to nie judo.
**EN:** Some accounts tie the start of BJJ to the judo and jujutsu Maeda practiced. That isn't one undisputed origin, and today's BJJ contests are not judo.

**PL:** Luta livre esportiva
**EN:** Luta livre esportiva

**PL:** Luta livre esportiva to brazylijski grappling bez kimona, historycznie obok BJJ, a nie jego reguła no-gi.
**EN:** Luta livre esportiva is Brazilian grappling without the gi, historically beside BJJ, not its no-gi rule.

**PL:** International Brazilian Jiu-Jitsu Federation — IBJJF
**EN:** 

**PL:** Brazilian jiu-jitsu — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

### karate — Karate

**PL:** Karate
**EN:** Karate

**PL:** Uderzenia
**EN:** Striking

**PL:** To nazwa zbiorcza, nie jeden regulamin, więc ten opis nie pasuje do każdej szkoły ani sali.
**EN:** It's an umbrella name, not one rule set, so this description doesn't fit every school or hall.

**PL:** Karate to rodzina sztuk uderzeń wywodzących się z Okinawy i rozwiniętych następnie w Japonii, a nie jeden regulamin. WKF punktuje kontrolowane kumite, w tym ciosy w głowę, a formuły knockdown, jak kyokushin, nie dopuszczają ciosów ręką na głowę, pozostawiając kopnięcia na głowę. Kyokushin jest stylem karate, nie sztuką obok karate.
**EN:** Karate is a family of striking arts rooted in Okinawa and later developed in Japan, not one rule set. WKF scores controlled kumite, including punches to the head, while knockdown formats such as Kyokushin leave the head for kicks. Kyokushin is a karate style, not an art beside karate.

**PL:** Okinawa, potem Japonia
**EN:** Okinawa, then Japan

**PL:** Tradycja okinawska, upowszechnienie w XX wieku
**EN:** Okinawan tradition, spread in the 20th century

**PL:** Azja Wschodnia
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Na Okinawie karate wyrosło z lokalnych sztuk uderzeń, a w XX wieku weszło do Japonii i rozeszło się na szkoły. Shotokan, goju-ryu, shito-ryu i wado-ryu to cztery duże nurty, które WKF traktuje jako osobne style, nie jako jeden worek technik.
**EN:** In Okinawa karate grew out of local striking arts, then entered Japan in the twentieth century and split into schools. Shotokan, Goju-ryu, Shito-ryu and Wado-ryu are four large currents that the WKF treats as separate styles, not one bag of techniques.

**PL:** Wspólny trening to kihon, kata i kumite, ale sparing zależy od szkoły. W kumite WKF liczą się kontrolowane trafienia, także pięścią w głowę. W knockdownzie kontakt jest pełniejszy, a ciosy ręką w głowę odpadają. Kata zostaje formą solo albo w grupie, nie walką.
**EN:** Shared training is kihon, kata and kumite, but sparring depends on the school. In WKF kumite the score is a controlled hit, including a punch to the head. In knockdown the contact is fuller and hand strikes to the head drop out. Kata stays a solo or group form, not a fight.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: wysoko
**EN:** Striking: high

**PL:** Pięści: wysoko
**EN:** Punches: high

**PL:** Kopnięcia: wysoko
**EN:** Kicks: high

**PL:** Kolana: średnio
**EN:** Knees: medium

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: nisko
**EN:** Grappling: low

**PL:** Klincz: nisko
**EN:** Clinch: low

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: wysoko
**EN:** Solo training: high

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: średnio
**EN:** Athletic demand: medium

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Broń opcjonalna
**EN:** Optional weapon

**PL:** Karate — Encyclopaedia Britannica
**EN:** 

**PL:** World Karate Federation — WKF
**EN:** 

### taekwondo — Taekwondo

**PL:** Taekwondo
**EN:** Taekwondo

**PL:** Uderzenia
**EN:** Striking

**PL:** Nie da się uczciwie podać jednej wersji, źródła są niejasne.
**EN:** There's no honest single version — the sources are unclear.

**PL:** Taekwondo to koreańska sztuka walki z mocnym naciskiem na kopnięcia, ale WT i ITF nie są tym samym sportem. W kyorugi World Taekwondo zawodnicy walczą w zatwierdzonych ochraniaczach i z elektronicznym systemem punktowania. ITF ma własne układy i regulamin sparingu. Taekkyeon to osobna, starsza tradycja.
**EN:** Taekwondo is a Korean martial art with a strong emphasis on kicks, but WT and ITF are not the same sport. World Taekwondo kyorugi is fought with approved protective equipment and electronic scoring. ITF uses its own patterns and sparring rules. Taekkyeon is a separate, older tradition.

**PL:** Korea
**EN:** Korea

**PL:** XX wiek, sport olimpijski jako dyscyplina medalowa od 2000
**EN:** 20th century, Olympic medal sport from 2000

**PL:** Azja Wschodnia
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Po wojnie koreańskiej kilka szkół zeszło się pod nazwą taekwondo. ITF powstała w 1966 roku, a federacja znana dziś jako World Taekwondo w 1973 roku. Z czasem rozwinęły odrębne regulaminy zawodów i odmienne ramy treningu. Hapkido bywa nauczane obok, ale to inna sztuka, z chwytami i dźwigniami.
**EN:** After the Korean War several schools came together under the name taekwondo. The ITF was founded in 1966, while the federation now known as World Taekwondo was founded in 1973. They developed distinct competition rules and training frameworks. Hapkido is sometimes taught next door, but it is a different art, with grips and locks.

**PL:** W WT zawodnicy walczą w kamizelce i nagolennikach, a punkt za kopnięcie w głowę jest wyższy niż za cios pięścią. W ITF zostają wzorce, układ sine wave i sparing, w którym ręce mają większą rolę. Formy to tul albo poomsae, zależnie od federacji, i nie są walką.
**EN:** In WT the fight goes through a chest guard and foot protectors, and a kick to the head scores higher than a punch. ITF keeps patterns, the sine-wave movement and sparring in which the hands have a larger role. Forms are tul or poomsae, depending on the federation, and they are not the fight.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: wysoko
**EN:** Striking: high

**PL:** Pięści: średnio
**EN:** Punches: medium

**PL:** Kopnięcia: wysoko
**EN:** Kicks: high

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: nisko
**EN:** Grappling: low

**PL:** Klincz: nisko
**EN:** Clinch: low

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: wysoko
**EN:** Endurance: high

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Bez broni
**EN:** No weapon

**PL:** Hapkido
**EN:** Hapkido

**PL:** Hapkido bywa nauczane obok taekwondo, ale osią są chwyt i dźwignia, nie kopnięcie na kamizelkę.
**EN:** Hapkido is sometimes taught beside taekwondo, but the axis is the grip and the lock, not the kick to a chest guard.

**PL:** Taekkyeon
**EN:** Taekkyeon

**PL:** Taekkyeon to osobna tradycja wpisana przez UNESCO, nie regulamin World Taekwondo.
**EN:** Taekkyeon is a separate tradition inscribed by UNESCO, not the World Taekwondo rulebook.

**PL:** World Taekwondo i ITF nie stosują tego samego regulaminu. W kyorugi WT zawodnicy walczą w ochraniaczach i z elektronicznym systemem punktowania, a ITF ma własne układy i regulamin sparingu.
**EN:** World Taekwondo and the ITF do not use the same rules. WT kyorugi is fought with body armour and electronic scoring, while ITF uses its own patterns and sparring rules.

**PL:** Taekwondo — Encyclopaedia Britannica
**EN:** 

**PL:** World Taekwondo — World Taekwondo
**EN:** 

**PL:** International Taekwon-Do Federation — ITF
**EN:** 

### sumo — Sumo

**PL:** Sumo
**EN:** Sumo

**PL:** Chwyty
**EN:** Grappling

**PL:** Sumo rozstrzyga się w kole: trzeba wypchnąć rywala albo sprawić, by dotknął ziemi czymś innym niż podeszwa stopy. Dozwolone są między innymi uderzenia otwartą dłonią, ale walki w parterze nie ma.
**EN:** Sumo is decided in a ring: you push the opponent out, or make them touch the ground with anything but the sole of the foot. Open-hand strikes, among other things, are allowed, but there's no ground fight.

**PL:** Japonia
**EN:** Japan

**PL:** Tradycja dworska i świątynna, zawodowy sport nowożytny
**EN:** Court and shrine tradition, modern professional sport

**PL:** Azja Wschodnia
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Sumo ma w Japonii długą historię jako rytuał i widowisko, a zawodowa organizacja i ranking powstały później. Rytuał przed walką jest częścią praktyki, a nie ozdobą dorzuconą po drodze.
**EN:** Sumo has a long history in Japan as ritual and spectacle, and the professional organisation and the ranking came later. The pre-bout ritual is part of the practice, not a decoration added along the way.

**PL:** Niska pozycja, zderzenie, chwyt za mawashi i próba wypchnięcia albo rzutu. Trening jest ciężki i mocno opiera się na pracy z partnerem.
**EN:** A low stance, the charge, a grip on the mawashi, and an attempt to push out or throw. Training is heavy and leans hard on work with a partner.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: nisko
**EN:** Striking: low

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: wysoko
**EN:** Clinch: high

**PL:** Rzuty: wysoko
**EN:** Throws: high

**PL:** Obalenia: wysoko
**EN:** Takedowns: high

**PL:** Parter: średnio
**EN:** Ground fighting: medium

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Bez broni
**EN:** No weapon

**PL:** Sumo — Encyclopaedia Britannica
**EN:** 

**PL:** Nihon Sumo Kyokai — Japan Sumo Association
**EN:** 

### sambo — Sambo

**PL:** Sambo
**EN:** Sambo

**PL:** Mieszane
**EN:** Mixed

**PL:** Sambo to rodzina sportów walki wywodzących się z tradycji radzieckiej, z odrębnymi formułami sportową i bojową. Sportowe sambo skupia się na rzutach, trzymaniach i dozwolonych dźwigniach, bez uderzeń. Combat sambo dokłada uderzenia do rzutów, trzymań, dźwigni i walki w parterze. To nie jest judo i nie jest tożsame z zapasami olimpijskimi.
**EN:** Sambo is a Soviet-origin combat-sport family with separate sport and combat formats. Sport sambo centres on throws, holds and legal locks, with no strikes. Combat sambo adds striking to throws, holds, locks and ground fighting. It is not judo and it is not Olympic wrestling.

**PL:** Związek Radziecki
**EN:** Soviet Union

**PL:** Lata 20.–30. XX wieku
**EN:** 1920s–1930s

**PL:** Europa Wschodnia
**EN:** 

**PL:** Mieszane
**EN:** Hybrid

**PL:** Sport walki
**EN:** Combat sport

**PL:** W ZSRR materiał z zapasów ludowych, judo i innych systemów chwytów połączono w jeden system. FIAS prowadzi dziś sportowe i bojowe sambo jako odrębne formuły. Kurtka sambowa jest narzędziem chwytu, podobnie jak w judo, ale techniki dozwolone przez regulamin są inne: sportowe sambo dopuszcza dźwignie na nogi i nie dopuszcza duszeń.
**EN:** In the USSR, material from folk wrestling, judo and other grappling systems was combined into a single system. FIAS now runs sport and combat sambo as separate formats. The sambo jacket is a gripping tool, as in judo, but the legal techniques differ: sport sambo allows leg locks and forbids chokes under its rules.

**PL:** W sportowym sambo walczy się w kurtce: rzuty, trzymania i dźwignie. Combat sambo dokłada uderzenia w stójce i w parterze, nadal w kurtce, według własnego regulaminu. Te formuły są ze sobą powiązane, ale nie są tą samą walką.
**EN:** In sport sambo you fight in a jacket: throws, holds and locks. Combat sambo adds strikes standing and on the ground, still in the jacket, under its own rules. These formats are related but are not the same fight.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: średnio
**EN:** Striking: medium

**PL:** Pięści: średnio
**EN:** Punches: medium

**PL:** Kopnięcia: średnio
**EN:** Kicks: medium

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: wysoko
**EN:** Throws: high

**PL:** Obalenia: wysoko
**EN:** Takedowns: high

**PL:** Parter: wysoko
**EN:** Ground fighting: high

**PL:** Poddania: wysoko
**EN:** Submissions: high

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: średnio
**EN:** Tradition: medium

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: wysoko
**EN:** Endurance: high

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Zawody
**EN:** Competition

**PL:** Bez broni
**EN:** No weapon

**PL:** Judo
**EN:** Judo

**PL:** Sportowe sambo dzieli z judo chwyt za kurtkę i rzuty, ale ma inne przepisy, m.in. dotyczące dźwigni na nogi i punktowania.
**EN:** Sport sambo shares the jacket grip and throws with judo, but its rules allow leg locks and differ in other techniques and scoring.

**PL:** Zapasy
**EN:** Wrestling

**PL:** Sambo obejmuje rzuty i grappling, ale ma własną kurtkę i własny regulamin.
**EN:** Sambo includes throws and grappling, but uses its own jacket and rules.

**PL:** MMA
**EN:** Mixed martial arts

**PL:** Combat sambo obejmuje uderzenia i walkę w parterze, ale pozostaje odrębnym regulaminem z kurtką i własnym katalogiem technik.
**EN:** Combat sambo includes striking and ground fighting, but remains a distinct ruleset with a jacket and its own technique list.

**PL:** Sambo (martial art) — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** International Sambo Federation — FIAS
**EN:** 

### wushu — Wushu / kung fu

**PL:** Wushu / kung fu
**EN:** Wushu / kung fu

**PL:** Uderzenia
**EN:** Striking

**PL:** To nazwa zbiorcza, nie jeden regulamin, więc ten opis nie pasuje do każdej szkoły ani sali.
**EN:** It's an umbrella name, not one rule set, so this description doesn't fit every school or hall.

**PL:** Nie da się uczciwie podać jednej wersji, źródła są niejasne.
**EN:** There's no honest single version — the sources are unclear.

**PL:** Wushu to szerokie określenie chińskich sztuk walki, podczas gdy sportowe wushu w ramach IWUF jest współczesną strukturą zawodniczą obejmującą taolu i sanda. Tradycyjne style i szkoły istnieją obok tej sportowej struktury. Sanda, wing chun i taijiquan są z nią powiązane, ale nie są synonimami całego wushu.
**EN:** Wushu is a broad label for Chinese martial arts, while sport wushu under IWUF is a modern competition framework with taolu and sanda. Traditional styles and schools sit alongside that sport framework. Sanda, Wing Chun and Taijiquan are related but are not synonyms for all wushu.

**PL:** Chiny, wiele szkół
**EN:** China, many schools

**PL:** Tradycje lokalne, nowoczesne wushu od XX wieku
**EN:** Local traditions, modern wushu from the 20th century

**PL:** Azja Wschodnia
**EN:** 

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Pod jedną etykietą mieszczą się szkoły południowe i północne, między innymi hung gar, choy li fut, bajiquan i xingyiquan. W XX wieku państwo uporządkowało część tego materiału jako wushu sportowe: formy taolu i walkę sanda. Tradycyjna szkoła nie staje się przez to sandą.
**EN:** One label covers southern and northern schools, among them Hung Gar, Choy Li Fut, Bajiquan and Xingyiquan. In the twentieth century the state organised part of that material as sport wushu: taolu forms and sanda fighting. A traditional school does not become sanda because of that.

**PL:** Taolu to układ z bronią albo bez, oceniany jak forma. W tradycyjnej szkole dochodzą zastosowania w parze i własna broń. Sanda jest osobną walką na platformie. Taijiquan ma tu własną kartę, bo formy, pchnięcia rąk i sport to już inny zestaw.
**EN:** Taolu is a routine with or without a weapon, judged as a form. A traditional school adds paired applications and its own weapons. Sanda is a separate fight on a platform. Taijiquan has its own card here, because forms, push-hands and the sport version are already a different set.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: wysoko
**EN:** Striking: high

**PL:** Pięści: średnio
**EN:** Punches: medium

**PL:** Kopnięcia: wysoko
**EN:** Kicks: high

**PL:** Kolana: średnio
**EN:** Knees: medium

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: średnio
**EN:** Grappling: medium

**PL:** Klincz: nisko
**EN:** Clinch: low

**PL:** Rzuty: średnio
**EN:** Throws: medium

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: średnio
**EN:** Weapons: medium

**PL:** Trening
**EN:** Training

**PL:** Trening solo: wysoko
**EN:** Solo training: high

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Broń opcjonalna
**EN:** Optional weapon

**PL:** Wing Chun
**EN:** Wing Chun

**PL:** Wing chun jest jedną ze szkół w rodzinie kung fu, nie formą taolu IWUF i nie sandą.
**EN:** Wing chun is one school in the kung fu family, not an IWUF taolu routine and not sanda.

**PL:** Taijiquan
**EN:** Taijiquan

**PL:** Taijiquan ma własne szkoły, formy i pchnięcia rąk. Nie jest synonimem całego wushu.
**EN:** Taijiquan has its own schools, forms and push-hands. It is not a synonym for all of wushu.

**PL:** Kung fu — Encyclopaedia Britannica
**EN:** 

**PL:** International Wushu Federation — IWUF
**EN:** 

### sanda — Sanda

**PL:** Sanda
**EN:** Sanda

**PL:** Mieszane
**EN:** Mixed

**PL:** Sanda to współczesny chiński sport walki związany ze sportowym wushu, zwykle rozgrywany na podwyższonej platformie i łączący pięści, kopnięcia oraz rzuty. Nie jest nazwą hung gar ani wing chun. Z shuai jiao łączy ją stosowanie rzutów, ale sanda dokłada uderzenia i inną płaszczyznę walki.
**EN:** Sanda is a modern Chinese combat sport associated with sport wushu, usually contested on a raised platform and combining punches, kicks and throws. It is not the name of Hung Gar or Wing Chun. It shares throws with shuai jiao, but adds strikes and a different fighting surface.

**PL:** Chiny, współczesny sport związany z wushu
**EN:** China, a contemporary sport tied to wushu

**PL:** XX wiek
**EN:** 20th century

**PL:** Azja Wschodnia
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** W XX wieku sanda urosła przy wushu jako sparring, a potem jako dyscyplina IWUF. Platforma i rzut z niej są częścią przepisu. To nie jest ring muay thai: klincz kolanami nie jest tu osią, a zepchnięcie z platformy może kończyć akcję.
**EN:** In the twentieth century sanda grew up beside wushu as sparring, then as an IWUF discipline. The platform and the throw off it are part of the rule. This is not a Muay Thai ring: the knee clinch is not the axis, and forcing someone off the platform can end the action.

**PL:** Stoisz na podwyższeniu, uderzasz i szukasz rzutu. Parter nie jest kontynuowany po rzucie; akcja kończy się zgodnie z regulaminem sanda. Pełny klincz muay thai, z kolanami przy głowie, nie jest opisem sandowej wymiany. Shuai jiao zostaje przy chwycie za kurtkę, bez tego zestawu ciosów.
**EN:** You stand on a raised platform, you strike and you look for a throw. There is no continuing ground fighting after a throw; the action ends under the sanda rules. A full Muay Thai clinch, with knees to the head, is not a description of a sanda exchange. Shuai jiao stays with the jacket grip, without this set of strikes.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: wysoko
**EN:** Striking: high

**PL:** Pięści: wysoko
**EN:** Punches: high

**PL:** Kopnięcia: wysoko
**EN:** Kicks: high

**PL:** Kolana: średnio
**EN:** Knees: medium

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: średnio
**EN:** Grappling: medium

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: średnio
**EN:** Throws: medium

**PL:** Obalenia: wysoko
**EN:** Takedowns: high

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: średnio
**EN:** Tradition: medium

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: wysoko
**EN:** Endurance: high

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Zawody
**EN:** Competition

**PL:** Bez broni
**EN:** No weapon

**PL:** Wushu / kung fu
**EN:** Wushu / kung fu

**PL:** Sanda to współczesny sport związany z wushu, a nie podstyl równy wszystkim tradycyjnym formom kung fu.
**EN:** Sanda is a contemporary sport tied to wushu, not a substyle equal to every traditional kung fu form.

**PL:** Shuai Jiao
**EN:** Shuai jiao

**PL:** Sanda dokłada do rzutu uderzenia i platformę. Shuai jiao zostaje przy kurtce, bez tego zestawu ciosów.
**EN:** Sanda adds strikes and a platform to the throw. Shuai jiao stays with the jacket, without that set of strikes.

**PL:** International Wushu Federation — IWUF
**EN:** 

**PL:** Sanda (sport) — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

### aikido — Aikido

**PL:** Aikido
**EN:** Aikido

**PL:** Chwyty
**EN:** Grappling

**PL:** Aikido ćwiczy zejście z linii, rzuty i dźwignie, zwykle z partnerem, który podaje uchwyt. W większości głównych organizacji rywalizacja turniejowa nie jest centrum treningu, choć istnieją odmiany z zawodami lub randori. Broń treningowa to między innymi jo i bokken.
**EN:** Aikido practises getting off the line, throws and locks, usually with a partner who offers a grip. In most of the main organisations tournament fighting is not the centre of training, though there are forms with contests or randori. Training weapons include the jo and the bokken.

**PL:** Japonia, Morihei Ueshiba
**EN:** Japan, Morihei Ueshiba

**PL:** XX wiek
**EN:** 20th century

**PL:** Azja Wschodnia
**EN:** 

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Morihei Ueshiba rozwijał aikido w XX wieku na bazie sztuk, które sam ćwiczył, w tym Daito-ryu. Późniejsze organizacje różnią się tempem, podejściem do broni i tym, czy w ogóle sparingują, więc jedna sala nie reprezentuje wszystkich.
**EN:** Morihei Ueshiba developed aikido in the twentieth century out of arts he himself trained, including Daito-ryu. Later organisations differ on pace, weapons and whether they spar at all, so one hall doesn't stand for all of them.

**PL:** Ćwiczy się formy w parach, upadki i pracę z bronią drewnianą. Kontakt bywa z góry ustalony, a w wielu szkołach nie jest to sparing na wynik.
**EN:** You practise paired forms, falling and work with a wooden weapon. Contact is often set in advance, and in many schools it is not sparring for a score.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: nisko
**EN:** Striking: low

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: wysoko
**EN:** Throws: high

**PL:** Obalenia: średnio
**EN:** Takedowns: medium

**PL:** Parter: średnio
**EN:** Ground fighting: medium

**PL:** Poddania: średnio
**EN:** Submissions: medium

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: nisko
**EN:** Competition: low

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: średnio
**EN:** Athletic demand: medium

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Praktyka tradycyjna
**EN:** Traditional practice

**PL:** Broń treningowa
**EN:** Training weapon

**PL:** Aikido — Encyclopaedia Britannica
**EN:** 

**PL:** Aikido — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

### krav-maga — Krav maga

**PL:** Krav maga
**EN:** Krav Maga

**PL:** Mieszane
**EN:** Mixed

**PL:** Krav maga to nazwa używana przez kilka programów samoobrony, nie jednej federacji. Organizacje i instruktorzy związani ze szkoleniem wojskowym lub policyjnym uczą pod tym samym szyldem różnych sylabusów. Wspólne jest zadanie: prosta reakcja na atak, bez sportowego punktowania.
**EN:** Krav maga is the name used by several self-defence programmes, not one federation. Organisations and instructors associated with military or law-enforcement training teach different syllabuses under the same label. What they share is the job: a plain response to an attack, with no sporting score.

**PL:** Izrael / Europa Środkowa, Imi Lichtenfeld
**EN:** Israel / Central Europe, Imi Lichtenfeld

**PL:** XX wiek
**EN:** 20th century

**PL:** Bliski Wschód
**EN:** 

**PL:** Samoobrona
**EN:** Self-defence

**PL:** Imi Lichtenfeld ułożył system w połowie XX wieku, najpierw przy realnych bójkach, potem przy szkoleniu. Później organizacje rozeszły się i każda trzyma własny program. Nie ma jednego światowego regulaminu, który dałoby się tu zacytować jak w boksie.
**EN:** Imi Lichtenfeld put the system together in the mid twentieth century, first around real fights, then around training. Later the organisations split, and each one keeps its own programme. There is no single world rulebook to quote here the way there is for boxing.

**PL:** Trening idzie przez scenariusze: cios, chwyt, zagrożenie nożem albo kijem, i wyjście z tego. Sparingu sportowego na punkty zwykle nie ma. Różnice między IKMF, KMG i programami wojskowymi widać w tym, co wchodzi do kursu, nie w nazwie na drzwiach.
**EN:** Training goes through scenarios: a strike, a grab, a knife or a stick, and a way out. A points spar is usually absent. The differences between IKMF, KMG and military programmes show up in what the course includes, not in the name on the door.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: wysoko
**EN:** Striking: high

**PL:** Pięści: wysoko
**EN:** Punches: high

**PL:** Kopnięcia: średnio
**EN:** Kicks: medium

**PL:** Kolana: średnio
**EN:** Knees: medium

**PL:** Łokcie: średnio
**EN:** Elbows: medium

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: średnio
**EN:** Grappling: medium

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: średnio
**EN:** Takedowns: medium

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: nisko
**EN:** Competition: low

**PL:** Tradycja: nisko
**EN:** Tradition: low

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: średnio
**EN:** Athletic demand: medium

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: nisko
**EN:** Equipment: low

**PL:** Bez zawodów
**EN:** No competition

**PL:** Broń opcjonalna
**EN:** Optional weapon

**PL:** Krav Maga — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Martial art — Encyclopaedia Britannica
**EN:** 

### hapkido — Hapkido

**PL:** Hapkido
**EN:** Hapkido

**PL:** Mieszane
**EN:** Mixed

**PL:** Nie da się uczciwie podać jednej wersji, źródła są niejasne.
**EN:** There's no honest single version — the sources are unclear.

**PL:** Hapkido to koreańska sztuka dźwigni, rzutów i kopnięć. Od taekwondo dzieli je cel: w hapkido chwyt i dźwignia są podstawą, a nie przerwą w walce na kopnięcia. Linie szkół różnią się tym, ile zostawiają uderzeń, a ile chwytów.
**EN:** Hapkido is a Korean art of locks, throws and kicks. What separates it from taekwondo is the aim: in hapkido the grip and the lock are the base, not a pause in a kicking match. School lines differ in how much striking they keep and how much grappling.

**PL:** Korea
**EN:** Korea

**PL:** XX wiek
**EN:** 20th century

**PL:** Azja Wschodnia
**EN:** 

**PL:** Samoobrona
**EN:** Self-defence

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Współczesne hapkido rozwinęło się w Korei w XX wieku. Organizacje różnią się w rodowodzie, więc ta karta nie wskazuje jednego mistrza jako jedynego źródła. Taekwondo ma federacje sportowe i ochraniacze. Hapkido częściej pozostaje przy technikach wykonywanych w parach i samoobronie.
**EN:** Modern hapkido grew in Korea in the twentieth century. Organisations differ in the lineage, so this card does not name one master as the only source. Taekwondo has sport federations and protective equipment. Hapkido more often stays with paired techniques and self-defence.

**PL:** Typowa technika w parach to chwyt nadgarstka albo rękawa, dźwignia i rzut, plus kopnięcia z dystansu. Nie ma tu kamizelki WT ani punktowania ITF. Trening zależy od linii: jedne dokładają broń, inne zostają przy pustej ręce.
**EN:** A typical pair is a wrist or sleeve grip, a lock and a throw, plus kicks from a distance. There is no WT chest guard and no ITF scoring. Training depends on the line: some add weapons, others stay with the empty hand.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: średnio
**EN:** Striking: medium

**PL:** Pięści: średnio
**EN:** Punches: medium

**PL:** Kopnięcia: średnio
**EN:** Kicks: medium

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: średnio
**EN:** Throws: medium

**PL:** Obalenia: średnio
**EN:** Takedowns: medium

**PL:** Parter: średnio
**EN:** Ground fighting: medium

**PL:** Poddania: średnio
**EN:** Submissions: medium

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: średnio
**EN:** Competition: medium

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: średnio
**EN:** Athletic demand: medium

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Praktyka tradycyjna
**EN:** Traditional practice

**PL:** Broń opcjonalna
**EN:** Optional weapon

**PL:** Hapkido — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Martial art — Encyclopaedia Britannica
**EN:** 

### savate — Savate

**PL:** Savate
**EN:** Savate

**PL:** Uderzenia
**EN:** Striking

**PL:** Savate to francuski boks nogą i pięścią, w butach. Osobno istnieje canne de combat, sport na lasce, który federacja trzyma obok, a nie jako rundę savate. But i kopnięcie zmieniają biodro względem kickboxingu bez obuwia.
**EN:** Savate is French boxing with the foot and the fist, in shoes. Canne de combat, a stick sport, sits beside it in the federation, not as a round of savate. The shoe and the kick change the hip compared with barefoot kickboxing.

**PL:** Francja
**EN:** France

**PL:** XIX wiek
**EN:** 19th century

**PL:** Europa
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** W XIX wieku paryski boks uliczny złożył się z angielskim boksem w sport, który dziś prowadzi francuska federacja. Canne i bâton to osobna praca laską i kijem, ze wspólną instytucją, nie z wspólną walką.
**EN:** In the nineteenth century Parisian street boxing combined with English boxing into the sport that the French federation runs today. Canne and bâton are separate work with a cane and a staff, under a shared institution, not in a shared fight.

**PL:** W savate kopie się czubkiem, podeszwą i podbiciem, w butach, a pięści zostają bokserskie. Formy assaut i combat różnią się dopuszczonym kontaktem. Canne ocenia się jako wymianę lasek w masce, nie jako kopnięcia.
**EN:** In savate you kick with the toe, the sole and the instep, in shoes, and the fists stay boxing fists. Assaut and combat differ in how much contact is allowed. Canne is judged as an exchange of canes in a mask, not as kicks.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: wysoko
**EN:** Striking: high

**PL:** Pięści: wysoko
**EN:** Punches: high

**PL:** Kopnięcia: wysoko
**EN:** Kicks: high

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: nisko
**EN:** Grappling: low

**PL:** Klincz: nisko
**EN:** Clinch: low

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: średnio
**EN:** Tradition: medium

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: wysoko
**EN:** Endurance: high

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: wysoko
**EN:** Equipment: high

**PL:** Zawody
**EN:** Competition

**PL:** Bez broni
**EN:** No weapon

**PL:** Savate — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Fédération Française de Savate — FFSavate
**EN:** 

### capoeira — Capoeira

**PL:** Capoeira
**EN:** Capoeira

**PL:** Uderzenia
**EN:** Striking

**PL:** Capoeira to afrobrazylijska sztuka walki, która łączy ruch, kopnięcia, uniki i muzykę w kręgu zwanym roda. Choć bywa mylona z kickboxingiem, jej korzenie sięgają czasów niewolnictwa w Brazylii, gdzie rozwijała się wśród zniewolonych Afrykanów i ich potomków.
**EN:** Capoeira is an Afro-Brazilian game joining movement, kicks, evasions and music in the circle, the roda. Depending on the group it can lean more on play, acrobatics, tradition or sparring, but it is not simply kickboxing.

**PL:** Brazylia
**EN:** Brazil

**PL:** Czasy niewoli oraz XIX i XX wiek
**EN:** Slavery era and the 19th–20th centuries

**PL:** Ameryka Południowa
**EN:** 

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** W XIX i XX wieku capoeira była prześladowana, ale później zyskała popularność i trafiła do szkół. Źródła różnią się w szczegółach dotyczących jej początków.
**EN:** It took shape in Brazil among enslaved Africans and their descendants. For part of the nineteenth and twentieth centuries it was outlawed, then it entered schools. Sources differ on the details of its beginnings.

**PL:** Bazą capoeiry jest ginga — płynny ruch, z którego wyprowadza się kopnięcia, uniki i przejścia. Muzyka i rytm są integralną częścią praktyki, nie tylko tłem.
**EN:** The ginga is the base, and the kicks, evasions and transitions come out of it. Music and rhythm are part of the practice, not just background.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: wysoko
**EN:** Striking: high

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: wysoko
**EN:** Kicks: high

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: nisko
**EN:** Grappling: low

**PL:** Klincz: nisko
**EN:** Clinch: low

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: średnio
**EN:** Competition: medium

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: wysoko
**EN:** Endurance: high

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Praktyka tradycyjna
**EN:** Traditional practice

**PL:** Bez broni
**EN:** No weapon

**PL:** Capoeira — Encyclopaedia Britannica
**EN:** 

**PL:** Capoeira — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Capoeira circle — UNESCO
**EN:** 

### kendo — Kendo

**PL:** Kendo
**EN:** Kendo

**PL:** Broń
**EN:** Weapons

**PL:** Kendo to japońska szermierka na shinai, w zbroi bogu, rozgrywana na punkty. Iaido i kenjutsu są obok, nie wewnątrz tego punktowania: iaido to formy z mieczem, kenjutsu to starsze szkoły miecza.
**EN:** Kendo is Japanese fencing with a shinai, in bogu armour, scored on points. Iaido and kenjutsu sit beside it, not inside that scoring: iaido is sword forms, kenjutsu is the older sword schools.

**PL:** Japonia, z ćwiczeń mieczem
**EN:** Japan, from sword practice

**PL:** Nowoczesna forma od XIX i XX wieku
**EN:** Modern form from the 19th–20th centuries

**PL:** Azja Wschodnia
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Z bronią
**EN:** Weapon-based

**PL:** Kendo ułożyło w XX wieku materiał ze szkół kenjutsu w sport z japońskim związkiem i egzaminami na stopnie. Iaido poszło w inną stronę: wyciągnięcie miecza i kata, bez walki na shinai. Kenjutsu nie jest kategorią kendo.
**EN:** In the twentieth century kendo arranged material from kenjutsu schools into a sport with a Japanese federation and grade exams. Iaido went another way: drawing the sword and kata, with no shinai fight. Kenjutsu is not a kendo division.

**PL:** W kendo liczy się poprawne trafienie w dozwoloną strefę, z krzykiem i z dobrą postawą, na shinai. Iaido ćwiczy się katalogiem form, często na mieczu treningowym, bez punktu za cios w men. Kenjutsu zostaje przy szkole i jej parach, nie przy turnieju kendo.
**EN:** In kendo a valid hit to a target, with a shout and good posture, scores on the shinai. Iaido is practised as a catalogue of forms, often with a training sword, and there is no point for a strike to the men. Kenjutsu stays with the school and its pairs, not with a kendo tournament.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: średnio
**EN:** Striking: medium

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: nisko
**EN:** Grappling: low

**PL:** Klincz: nisko
**EN:** Clinch: low

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: wysoko
**EN:** Weapons: high

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: wysoko
**EN:** Endurance: high

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: wysoko
**EN:** Equipment: high

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Broń treningowa
**EN:** Training weapon

**PL:** Iaido
**EN:** Iaido

**PL:** Kendo punktuje trafienie shinai w zbroi. Iaido ćwiczy dobywanie miecza w formach i nie jest kategorią kendo.
**EN:** Kendo scores a shinai hit in armour. Iaido practises drawing the sword in forms and is not a kendo division.

**PL:** All Japan Kendo Federation — AJKF
**EN:** 

**PL:** Kendo — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

### szermierka — Szermierka sportowa

**PL:** Szermierka sportowa
**EN:** Sport fencing

**PL:** Broń
**EN:** Weapons

**PL:** Szermierka sportowa obejmuje trzy konkurencje: floret, szpadę i szablę. Trafienia są rejestrowane przez elektroniczną aparaturę. Kluczowe znaczenie mają dystans, timing i przestrzeganie zasad danej broni.
**EN:** Sport fencing covers foil, epee and sabre, and electrical kit records the touches. Distance, timing and a hit under that weapon's rules are what count. Foil and sabre use right of way; epee has different rules.

**PL:** Europa, pojedynki i sale szermiercze
**EN:** Europe, the duel and the salle

**PL:** Sportowa forma z XIX i XX wieku
**EN:** Sporting form, 19th–20th century

**PL:** Europa
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Z bronią
**EN:** Weapon-based

**PL:** Szermierka sportowa wywodzi się z europejskiej tradycji broni białej i XIX-wiecznych sal szermierczych. Wprowadzenie maski, sprzętu ochronnego i elektronicznego sędziowania pozwoliło przekształcić ją w nowoczesny sport olimpijski.
**EN:** It grew out of the European bladed-weapon tradition and the nineteenth-century salle. The mask, protective kit and electrical judging helped turn it into a modern Olympic sport.

**PL:** Trening obejmuje lekcje z trenerem, pracę nóg, wypad i sparing na planszy.
**EN:** A lesson with a coach, footwork, the lunge and sparring on the piste.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: nisko
**EN:** Striking: low

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: nisko
**EN:** Grappling: low

**PL:** Klincz: nisko
**EN:** Clinch: low

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: wysoko
**EN:** Weapons: high

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: średnio
**EN:** Tradition: medium

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: średnio
**EN:** Athletic demand: medium

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: wysoko
**EN:** Equipment: high

**PL:** Zawody
**EN:** Competition

**PL:** Broń treningowa
**EN:** Training weapon

**PL:** W szermierce sportowej trafienie rejestruje aparatura elektryczna. HEMA próbuje odtworzyć techniki opisane w dawnych traktatach. To dwie różne praktyki.
**EN:** Sport fencing records a touch with electrical kit. HEMA tries to reconstruct techniques described in old treatises. They are two different practices.

**PL:** Fencing — Encyclopaedia Britannica
**EN:** 

**PL:** International Fencing Federation — FIE
**EN:** 

### hema — HEMA (Historical European Martial Arts)

**PL:** HEMA (Historical European Martial Arts)
**EN:** HEMA

**PL:** Broń
**EN:** Weapons

**PL:** Nie da się uczciwie podać jednej wersji, źródła są niejasne.
**EN:** There's no honest single version — the sources are unclear.

**PL:** HEMA to współczesna próba odtworzenia europejskich sztuk broni z traktatów: miecz długi, rapier, miecz boczny, dussack i inne. To nie jest szermierka olimpijska i nie jest japońskie kenjutsu.
**EN:** HEMA is a modern attempt to reconstruct European weapon arts from treatises: the longsword, the rapier, the sidesword, the dussack and others. It is not Olympic fencing and it is not Japanese kenjutsu.

**PL:** Współczesna rekonstrukcja europejskich sztuk broni
**EN:** A modern reconstruction of European weapon arts

**PL:** Rekonstrukcja od końca XX wieku, źródła od średniowiecza
**EN:** Reconstruction from the late 20th century, sources from the Middle Ages

**PL:** Europa
**EN:** 

**PL:** Rekonstrukcja historyczna
**EN:** Historical reconstruction

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Z bronią
**EN:** Weapon-based

**PL:** Traktaty są historyczne, a kluby i turnieje, które dziś z nich trenują, są w większości z końca XX wieku. Czytanie tego samego źródła bywa sporne. Kenjutsu to sąsiednia, japońska praktyka miecza, z własnych szkół, nie dział HEMA.
**EN:** The treatises are historical, and the clubs and tournaments that train from them today are mostly from the late twentieth century. Readings of the same source are sometimes disputed. Kenjutsu is a neighbouring Japanese sword practice, from its own schools, not a branch of HEMA.

**PL:** Ćwiczy się zestawy z traktatu, pary i sparing na broni tępej w ochraniaczach dobranych do broni. Szermierka sportowa ma floret, szpadę i szablę oraz elektroniczne sędziowanie trafień. Tutaj sposób interpretacji technik i trafień zależy od źródeł historycznych oraz regulaminu turnieju; nie ma jednego systemu punktowania HEMA.
**EN:** You drill sets from a treatise, pairs and sparring with blunt weapons in protection matched to the weapon. Sport fencing has foil, épée and sabre, with electrical scoring. Here historical sources and tournament rules determine how techniques and hits are interpreted; there is no single HEMA scoring system.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: średnio
**EN:** Striking: medium

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: średnio
**EN:** Grappling: medium

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: wysoko
**EN:** Weapons: high

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: średnio
**EN:** Competition: medium

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: wysoko
**EN:** Endurance: high

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: wysoko
**EN:** Equipment: high

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Broń treningowa
**EN:** Training weapon

**PL:** Szermierka sportowa
**EN:** Sport fencing

**PL:** Szermierka sportowa i HEMA to dwie różne praktyki: w szermierce trafienia rejestruje aparatura, a HEMA odtwarza historyczne techniki z traktatów.
**EN:** Both practices work with European bladed weapons, but HEMA reconstructs techniques from historical treatises, while sport fencing has three weapons and its own rules. It is not the same training.

**PL:** W szermierce sportowej trafienie rejestruje aparatura elektryczna. HEMA próbuje odtworzyć techniki opisane w dawnych traktatach. To dwie różne praktyki.
**EN:** Sport fencing records a touch with electrical kit. HEMA tries to reconstruct techniques described in old treatises. They are two different practices.

**PL:** HEMA Alliance — HEMA Alliance
**EN:** 

**PL:** Historical European martial arts — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

### arnis — Arnis / Kali / Eskrima

**PL:** Arnis / Kali / Eskrima
**EN:** Arnis / kali / eskrima

**PL:** Broń
**EN:** Weapons

**PL:** To nazwa zbiorcza, nie jeden regulamin, więc ten opis nie pasuje do każdej szkoły ani sali.
**EN:** It's an umbrella name, not one rule set, so this description doesn't fit every school or hall.

**PL:** Arnis, kali i eskrima to filipińskie sztuki z kijem, nożem i pustą ręką. Nazwy zależą od regionu i szkoły, nie od trzech różnych sportów. Obok tradycji są też formuły sportowe na kij.
**EN:** Arnis, kali and eskrima are Philippine arts with stick, knife and empty hand. The names depend on the region and the school, not on three different sports. Sport formats for the stick sit beside the tradition.

**PL:** Filipiny
**EN:** The Philippines

**PL:** Tradycje lokalne, nazwy nowożytne
**EN:** Local traditions, modern names

**PL:** Azja Południowo-Wschodnia
**EN:** 

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Z bronią
**EN:** Weapon-based

**PL:** Broń krótka jest osią, a pusta ręka dochodzi jako kontynuacja tych samych kątów. Znane nurty to między innymi Modern Arnis, Doce Pares i Balintawak. Każdy układa inaczej kij, nóż i wejście na dystans ręki. W 2009 roku Filipiny uznały arnis za narodową sztukę walki i sport na mocy Republic Act No. 9850.
**EN:** The short weapon is the axis, and the empty hand comes in as a continuation of the same angles. Known currents include Modern Arnis, Doce Pares and Balintawak. Each one arranges the stick, the knife and the entry to empty-hand range differently. In 2009, the Philippines declared arnis the national martial art and sport through Republic Act No. 9850.

**PL:** Trening zaczyna się od kijów: kąty, blok i kontra. Potem nóż, dwie bronie albo pusta ręka. W sporcie liczy się zwykle kij i ochraniacze. Szkoła tradycyjna nie kończy się na punktach za trafienie piankowym kijem.
**EN:** Training starts with sticks: angles, a block and a counter. Then the knife, two weapons or the empty hand. In sport the usual tools are a stick and protection. A traditional school does not end at points for hitting with a foam stick.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: średnio
**EN:** Striking: medium

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: nisko
**EN:** Grappling: low

**PL:** Klincz: nisko
**EN:** Clinch: low

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: wysoko
**EN:** Weapons: high

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: średnio
**EN:** Competition: medium

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: średnio
**EN:** Athletic demand: medium

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: wysoko
**EN:** Equipment: high

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Broń główna
**EN:** Weapon first

**PL:** Arnis — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Martial art — Encyclopaedia Britannica
**EN:** 

**PL:** Republic Act No. 9850 — Lawphil
**EN:** 

### silat — Silat

**PL:** Silat
**EN:** Silat

**PL:** Mieszane
**EN:** Mixed

**PL:** To nazwa zbiorcza, nie jeden regulamin, więc ten opis nie pasuje do każdej szkoły ani sali.
**EN:** It's an umbrella name, not one rule set, so this description doesn't fit every school or hall.

**PL:** Pencak silat to rodzina sztuk z Indonezji, Malezji i pobliskich regionów, nie jeden regulamin. Są nurty regionalne i broń, a w zawodach PERSILAT główne kategorie to tanding i jurus, przy czym jurus obejmuje tunggal, ganda i regu.
**EN:** Pencak silat is a family of arts from Indonesia, Malaysia and nearby regions, not one rule set. There are regional traditions and weapons, and in PERSILAT competition the main categories are tanding and jurus, with jurus including tunggal, ganda and regu.

**PL:** Archipelag Malajski
**EN:** The Malay archipelago

**PL:** Tradycje lokalne, sport pencak silat w XX wieku
**EN:** Local traditions, pencak silat sport in the 20th century

**PL:** Azja Południowo-Wschodnia
**EN:** 

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Nazwa zbiera style wysp i dworów, z pustą ręką i z bronią. UNESCO w 2019 roku wpisało tradycje pencak silat jako dziedzictwo, a nie regulamin turnieju. Zasady walki sportowej trzyma PERSILAT i federacje krajowe.
**EN:** The name gathers island and court styles, empty hand and weapons. In 2019 UNESCO inscribed the traditions of pencak silat as heritage, not as a tournament rulebook. PERSILAT and national federations hold the sporting rules.

**PL:** Jurus oznacza formy lub sekwencje ruchów w praktyce i jest także kategorią zawodów według regulaminu PERSILAT. Kategorie jurus obejmują tunggal, ganda i regu, a tanding jest kategorią walki. Trening szkoły może też obejmować broń. Formy nie są walką.
**EN:** Jurus refers to forms or movement sequences in the practice and is also a competition category under the PERSILAT rules. The jurus categories include tunggal, ganda and regu; tanding is the combat category. A school's training can also include weapons. Forms are not the match.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: wysoko
**EN:** Striking: high

**PL:** Pięści: średnio
**EN:** Punches: medium

**PL:** Kopnięcia: wysoko
**EN:** Kicks: high

**PL:** Kolana: średnio
**EN:** Knees: medium

**PL:** Łokcie: średnio
**EN:** Elbows: medium

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: średnio
**EN:** Grappling: medium

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: średnio
**EN:** Throws: medium

**PL:** Obalenia: średnio
**EN:** Takedowns: medium

**PL:** Parter: średnio
**EN:** Ground fighting: medium

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: średnio
**EN:** Weapons: medium

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: średnio
**EN:** Competition: medium

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: średnio
**EN:** Athletic demand: medium

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Broń opcjonalna
**EN:** Optional weapon

**PL:** W regulaminie zawodów PERSILAT z 2026 roku główne kategorie to Tanding i Jurus; Jurus obejmuje Tunggal, Ganda i Regu.
**EN:** In the 2026 PERSILAT competition regulations, the main competition categories are Tanding and Jurus; Jurus includes Tunggal, Ganda and Regu.

**PL:** Pencak silat — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Traditions of Pencak Silat — UNESCO
**EN:** 

**PL:** Pencak Silat Competition Rules and Regulations — PERSILAT
**EN:** 

### lethwei — Lethwei

**PL:** Lethwei
**EN:** Lethwei

**PL:** Uderzenia
**EN:** Striking

**PL:** Lethwei to birmański boks: pięści, nogi, kolana, łokcie i, w tradycyjnych formułach, głowa. Tradycyjne formuły używają owijek zamiast rękawic bokserskich; współczesne gale lethwei mogą stosować inne regulaminy i wyposażenie. To nie jest muay thai, mimo podobnego zestawu kończyn.
**EN:** Lethwei is Burmese boxing: fists, legs, knees, elbows and, in traditional formats, the head. Traditional formats use hand wraps rather than boxing gloves; modern Lethwei events can use different rules and equipment. It is not Muay Thai, even with a similar set of limbs.

**PL:** Mjanma
**EN:** Myanmar

**PL:** Tradycja lokalna, współczesne gale XX–XXI wiek
**EN:** Local tradition, modern cards in the 20th–21st centuries

**PL:** Azja Południowo-Wschodnia
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Lokalne walki są starsze niż dzisiejsze gale. Współczesne federacje doprecyzowały rundy i sprzęt, ale tradycyjne formuły używają owijek zamiast rękawic bokserskich; współczesne gale lethwei mogą stosować inne regulaminy i wyposażenie. Podobieństwo do muay thai nie zrównało przepisów.
**EN:** Local fights are older than today's cards. Modern federations have tightened rounds and kit, but traditional formats use hand wraps rather than boxing gloves; modern Lethwei events can use different rules and equipment. Looking like Muay Thai did not make the rules the same.

**PL:** Wymiana jest twarda i stoi. Głowa wchodzi jako uderzenie, gdy regulamin jej nie wyłączy. Brak grubej rękawicy zmienia pięść względem muay thai i K-1. Parteru tu nie ma.
**EN:** The exchange is hard and stays standing. The head comes in as a strike when the rules do not switch it off. The lack of a thick glove changes the fist compared with Muay Thai and K-1. There is no ground game.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: wysoko
**EN:** Striking: high

**PL:** Pięści: wysoko
**EN:** Punches: high

**PL:** Kopnięcia: wysoko
**EN:** Kicks: high

**PL:** Kolana: wysoko
**EN:** Knees: high

**PL:** Łokcie: wysoko
**EN:** Elbows: high

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: średnio
**EN:** Grappling: medium

**PL:** Klincz: wysoko
**EN:** Clinch: high

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: wysoko
**EN:** Endurance: high

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Zawody
**EN:** Competition

**PL:** Bez broni
**EN:** No weapon

**PL:** Lethwei — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Myanmar — Encyclopaedia Britannica
**EN:** 

**PL:** International Lethwei Unified Ruleset — Lethwei Fighting Championship
**EN:** 

### kyokushin — Kyokushin

**PL:** Kyokushin
**EN:** Kyokushin karate

**PL:** Uderzenia
**EN:** Striking

**PL:** Kyokushin to pełnokontaktowy styl karate, założony w połowie XX wieku przez Masutatsu Oyamę jako twarda odmiana karate. W klasycznych i wielu współczesnych formułach knock-down ciosy pięścią na głowę są zazwyczaj zakazane, a kopnięcia na głowę dozwolone, choć szczegóły zależą od organizacji i regulaminu.
**EN:** Kyokushin is a full-contact karate style. In classic and many modern knockdown formats punches to the head are illegal and kicks to the head are allowed. The details still depend on the organisation and the rules.

**PL:** Japonia, Masutatsu Oyama, w obrębie karate
**EN:** Japan, Masutatsu Oyama, inside karate

**PL:** Połowa XX wieku
**EN:** Mid 20th century

**PL:** Azja Wschodnia
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Masutatsu Oyama założył kyokushin w połowie XX wieku jako twardą odmianę karate. Kyokushin pozostaje odmianą karate, a nie osobną tradycją spoza karate.
**EN:** Masutatsu Oyama founded Kyokushin in the mid twentieth century as a hard form of karate, and organisations began to split after his death. Kyokushin remains a form of karate, not a tradition from outside karate.

**PL:** Trening kyokushin obejmuje kihon (ćwiczenia podstaw), kata (formy) oraz kumite (sparing z kontaktem). Nacisk kładzie się na kondycję i sparing, a nie tylko na formę.
**EN:** You practise kihon, kata and kumite with contact. Conditioning and sparring are the axis, not the form alone.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: wysoko
**EN:** Striking: high

**PL:** Pięści: wysoko
**EN:** Punches: high

**PL:** Kopnięcia: wysoko
**EN:** Kicks: high

**PL:** Kolana: średnio
**EN:** Knees: medium

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: nisko
**EN:** Grappling: low

**PL:** Klincz: nisko
**EN:** Clinch: low

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: wysoko
**EN:** Endurance: high

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Zawody
**EN:** Competition

**PL:** Bez broni
**EN:** No weapon

**PL:** Karate
**EN:** Karate

**PL:** Kyokushin to pełnokontaktowa odmiana karate, a nie osobna tradycja spoza karate.
**EN:** Kyokushin is a full-contact style of karate, not a tradition from outside karate.

**PL:** Kyokushin — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Karate — Encyclopaedia Britannica
**EN:** 

**PL:** KWU kumite and kata rules — Kyokushin World Union
**EN:** 

### wing-chun — Wing Chun

**PL:** Wing Chun
**EN:** Wing Chun

**PL:** Uderzenia
**EN:** Striking

**PL:** Wing Chun to południowochińska sztuka walki krótkiego dystansu, charakteryzująca się prostymi uderzeniami i ćwiczeniem chi sao („klejące ręce”). Opowieść o założycielce, Yim Wing-chun, należy do tradycji szkoły, a nie do udokumentowanej historii.
**EN:** Wing Chun is a southern Chinese short-range art: structure, straight strikes and chi sao, the sticking hands. The story of a founding woman belongs to school tradition, not to a documented biography.

**PL:** Południowe Chiny
**EN:** Southern China

**PL:** Tradycja południowochińska, popularyzacja w XX wieku
**EN:** Southern Chinese tradition, popularised in the 20th century

**PL:** Azja Wschodnia
**EN:** 

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Praktyka wiąże się z południowymi Chinami i XX-wiecznym nauczaniem, w tym linią Ip Mana. Legenda o Ng Mui i Yim Wing-chun należy do późniejszej tradycji szkoły i tak ją tutaj oznaczam.
**EN:** The practice is tied to southern China and to twentieth-century teaching, including the Ip Man line. The legend of Ng Mui and Yim Wing-chun belongs to the school's later tradition, and that's how I mark it.

**PL:** Trening obejmuje ćwiczenie form na drewnianym manekinie, chi sao oraz uderzeń z bliska. Sparing może występować, ale zależy to od konkretnej szkoły lub instruktora.
**EN:** You practise forms on the wooden dummy, chi sao and close strikes. Sparring depends on the hall.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: wysoko
**EN:** Striking: high

**PL:** Pięści: wysoko
**EN:** Punches: high

**PL:** Kopnięcia: średnio
**EN:** Kicks: medium

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: średnio
**EN:** Elbows: medium

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: średnio
**EN:** Grappling: medium

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: wysoko
**EN:** Solo training: high

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: nisko
**EN:** Competition: low

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: średnio
**EN:** Athletic demand: medium

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: nisko
**EN:** Equipment: low

**PL:** Praktyka tradycyjna
**EN:** Traditional practice

**PL:** Broń opcjonalna
**EN:** Optional weapon

**PL:** Opowieść o Ng Mui i Yim Wing-chun należy do tradycji szkoły wing chun, a nie do udokumentowanej historii, na której można oprzeć dokładną datę powstania stylu.
**EN:** The story of Ng Mui and Yim Wing-chun belongs to Wing Chun school tradition, not to documented history you can use to pin down an exact founding date.

**PL:** Późniejsza tradycja / legenda.
**EN:** Later tradition / legend.

**PL:** Wing Chun — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Kung fu — Encyclopaedia Britannica
**EN:** 

### jeet-kune-do — Jeet Kune Do (JKD)

**PL:** Jeet Kune Do (JKD)
**EN:** Jeet Kune Do

**PL:** Mieszane
**EN:** Mixed

**PL:** Jeet Kune Do (JKD) to koncepcja stworzona przez Bruce'a Lee, polegająca na wybieraniu najskuteczniejszych technik z różnych stylów walki, bez tworzenia zamkniętego systemu. JKD nie jest federacją sportową ani stylem z jednolitym regulaminem turniejowym.
**EN:** Jeet Kune Do is Bruce Lee's approach: take what works, without one closed catalogue of forms. It is not a sport federation and not a style with one tournament rulebook.

**PL:** Stany Zjednoczone, Bruce Lee
**EN:** United States, Bruce Lee

**PL:** Lata 60. XX wieku
**EN:** 1960s

**PL:** Ameryka Północna
**EN:** 

**PL:** Mieszane
**EN:** Hybrid

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Bruce Lee rozwijał JKD w latach 60. XX wieku, wychodząc poza swoje wcześniejsze doświadczenia z wing chun. Po jego śmierci uczniowie różnie interpretowali, czy JKD powinno być zestawem technik, czy raczej metodą dalszego poszukiwania.
**EN:** Lee developed and described JKD in the 1960s, moving beyond his earlier Wing Chun work. After his death, students read differently whether JKD should be a closed set of techniques or a way of searching further.

**PL:** Trening JKD obejmuje ćwiczenia ze sprzętem, sparing oraz łączenie uderzeń, klinczu i prostych obaleń. Metody treningowe mogą się różnić w zależności od nauczyciela.
**EN:** You train with kit, spar, and mix strikes, clinch and simple takedowns, depending on the teacher.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: wysoko
**EN:** Striking: high

**PL:** Pięści: wysoko
**EN:** Punches: high

**PL:** Kopnięcia: wysoko
**EN:** Kicks: high

**PL:** Kolana: średnio
**EN:** Knees: medium

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: średnio
**EN:** Grappling: medium

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: średnio
**EN:** Takedowns: medium

**PL:** Parter: średnio
**EN:** Ground fighting: medium

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: nisko
**EN:** Competition: low

**PL:** Tradycja: średnio
**EN:** Tradition: medium

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: średnio
**EN:** Athletic demand: medium

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Bez zawodów
**EN:** No competition

**PL:** Broń opcjonalna
**EN:** Optional weapon

**PL:** Jeet Kune Do — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Bruce Lee — Encyclopaedia Britannica
**EN:** 

### jujutsu — Jujutsu

**PL:** Jujutsu
**EN:** Jujutsu

**PL:** Chwyty
**EN:** Grappling

**PL:** To nazwa zbiorcza, nie jeden regulamin, więc ten opis nie pasuje do każdej szkoły ani sali.
**EN:** It's an umbrella name, not one rule set, so this description doesn't fit every school or hall.

**PL:** Jujutsu to nazwa na japońskie szkoły chwytów sprzed judo i na późniejsze klubowe ju-jitsu. Koryu, sportowe duo i samoobrona nie grają tą samą walką. Judo rozwinęło się ze starszych szkół jujutsu, natomiast brazylijskie jiu-jitsu rozwinęło się później poprzez brazylijską praktykę judo i pokrewnych form grapplingu. Obie praktyki mają własne karty.
**EN:** Jujutsu is the name for Japanese grappling schools from before judo and for later club ju-jitsu. Koryu, sporting duo and self-defence are not the same fight. Judo developed from older jujutsu schools, while Brazilian jiu-jitsu developed later through Brazilian practice of judo and related grappling. Both have their own cards.

**PL:** Japonia, wiele szkół
**EN:** Japan, many schools

**PL:** Szkoły od okresu wczesnonowożytnego, nazwa zbiorcza
**EN:** Schools from the early modern period, an umbrella name

**PL:** Azja Wschodnia
**EN:** 

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Historyczne szkoły, koryu, uczyły chwytów, rzutów, dźwigni i często broni przy szkole samurajskiej. Kano wybrał z tego materiał na judo. XX-wieczne ju-jitsu klubowe w Europie to już inna praktyka: pary, systemy samoobrony i zawody duo, nie odtworzenie jednej szkoły z Edo.
**EN:** Historical schools, koryu, taught grips, throws, locks and often weapons inside a samurai school. Kano took material from that and built judo. Twentieth-century club ju-jitsu in Europe is a different practice: pairs, self-defence systems and duo contests, not a reconstruction of one Edo school.

**PL:** W koryu pracuje się formami pary i tym, co szkoła uznaje za technikę, łącznie z bronią. W klubowym ju-jitsu częściej są atemi, rzuty, trzymania i ułożone pary na ocenę. To nie jest randori judo ani walka BJJ na punkty.
**EN:** In koryu you work paired forms and whatever the school counts as technique, weapons included. In club ju-jitsu you more often see atemi, throws, holds and set pairs for a score. That is not judo randori and it is not a points fight in BJJ.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: średnio
**EN:** Striking: medium

**PL:** Pięści: średnio
**EN:** Punches: medium

**PL:** Kopnięcia: średnio
**EN:** Kicks: medium

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: wysoko
**EN:** Throws: high

**PL:** Obalenia: średnio
**EN:** Takedowns: medium

**PL:** Parter: średnio
**EN:** Ground fighting: medium

**PL:** Poddania: wysoko
**EN:** Submissions: high

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: średnio
**EN:** Competition: medium

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: średnio
**EN:** Athletic demand: medium

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Praktyka tradycyjna
**EN:** Traditional practice

**PL:** Broń opcjonalna
**EN:** Optional weapon

**PL:** Judo
**EN:** Judo

**PL:** Kano ułożył judo z materiału starszych szkół jujutsu. Dzisiejsze judo sportowe nie jest tymi szkołami.
**EN:** Kano arranged judo from the material of older jujutsu schools. Today's sporting judo is not those schools.

**PL:** Brazylijskie jiu-jitsu
**EN:** Brazilian jiu-jitsu

**PL:** Część opracowań wiąże BJJ z judo i jujutsu Maedy. To nie jest dzisiejsze klubowe ju-jitsu.
**EN:** Some accounts tie BJJ to Maeda's judo and jujutsu. That is not today's club ju-jitsu.

**PL:** Jujutsu — Encyclopaedia Britannica
**EN:** 

**PL:** Jujutsu — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

### pankration — Pankration

**PL:** Pankration
**EN:** Pankration

**PL:** Mieszane
**EN:** Mixed

**PL:** Pankration był konkurencją igrzysk w Grecji: chwyt i uderzenie w jednej walce. Współczesne grupy odtwarzają go z waz, tekstów i przypisów. Nie ma jednej federacji, która byłaby pankrationem tak, jak UWW jest zapaśnictwem.
**EN:** Pankration was a contest at the Greek games: a grip and a strike in one fight. Contemporary groups reconstruct it from vases, texts and commentaries. There is no single federation that is pankration the way UWW is wrestling.

**PL:** Starożytna Grecja
**EN:** Ancient Greece

**PL:** Starożytność; współczesne zawody to rekonstrukcja sportowa
**EN:** Antiquity; modern contests are a sporting reconstruction

**PL:** Europa
**EN:** 

**PL:** Rekonstrukcja historyczna
**EN:** Historical reconstruction

**PL:** Sport walki
**EN:** Combat sport

**PL:** W starożytności pankration stał obok zapasów i pięściarstwa jako szersze połączenie uderzeń i chwytów niż same zapasy. Dzisiejsze rekonstrukcje i sporty, które pożyczają nazwę, nie są tym samym antycznym turniejem. Przepisów z Olimpii nie można po prostu zastosować do współczesnych zawodów.
**EN:** In antiquity pankration stood beside wrestling and boxing, with a broader combination of striking and grappling than wrestling alone. Today's reconstructions, and sports that borrow the name, are not that ancient contest. The rules from Olympia cannot simply be applied to a modern competition.

**PL:** Antyczny obraz to walka w stójce i w parterze, z ciosami i chwytami, bez dzisiejszych rękawic. Współczesna sala może to ćwiczyć jako rekonstrukcję albo jako własny regulamin sportowy. Wtedy trzeba czytać, czyja to zasada, bo jednej nie ma.
**EN:** The ancient picture is a fight standing and on the ground, with strikes and grips, and without modern gloves. A contemporary gym may train that as a reconstruction or as its own sporting rules. You then have to read whose rule it is, because there is not one.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: wysoko
**EN:** Striking: high

**PL:** Pięści: wysoko
**EN:** Punches: high

**PL:** Kopnięcia: średnio
**EN:** Kicks: medium

**PL:** Kolana: średnio
**EN:** Knees: medium

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: średnio
**EN:** Throws: medium

**PL:** Obalenia: średnio
**EN:** Takedowns: medium

**PL:** Parter: średnio
**EN:** Ground fighting: medium

**PL:** Poddania: średnio
**EN:** Submissions: medium

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: nisko
**EN:** Solo training: low

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: średnio
**EN:** Competition: medium

**PL:** Tradycja: średnio
**EN:** Tradition: medium

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: wysoko
**EN:** Endurance: high

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: nisko
**EN:** Equipment: low

**PL:** Rekonstrukcja
**EN:** Reconstruction

**PL:** Bez broni
**EN:** No weapon

**PL:** Pankration — Encyclopaedia Britannica
**EN:** 

**PL:** Pankration — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

### shuai-jiao — Shuai Jiao

**PL:** Shuai Jiao
**EN:** Shuai jiao

**PL:** Chwyty
**EN:** Grappling

**PL:** Shuai jiao to chińskie zapasy w kurtce. Styl pekiński i inne odmiany różnią się wejściem i chwytem za rękaw, ale zostają zapasami, nie sandą. Uderzenia nie rozstrzygają tej walki.
**EN:** Shuai jiao is Chinese jacket wrestling. Beijing style and other variants differ in the entry and the sleeve grip, but they stay wrestling, not sanda. Strikes do not decide this fight.

**PL:** Chiny
**EN:** China

**PL:** Tradycja zapasów, sportowa forma nowożytna
**EN:** A wrestling tradition, modern sporting form

**PL:** Azja Wschodnia
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Zapasy w kurtce mają w Chinach długą praktykę, a współczesne zawody uporządkowały kategorie i chwyt. Sanda wzięła część rzutów na swoją platformę i dołożyła ciosy. To sąsiedztwo, nie druga nazwa tej samej walki.
**EN:** Jacket wrestling has a long practice in China, and modern contests tidied up the divisions and the grip. Sanda took some of the throws onto its platform and added strikes. That is a neighbourhood, not a second name for the same fight.

**PL:** Łapiesz kurtkę i rękaw, wchodzisz biodrem albo nogą i rzucasz. W stylu pekińskim nacisk pada na określone wejścia; inne ośrodki trzymają chwyt inaczej. Nie ma kopnięć punktowanych jak w sandzie ani klinczu kolanem.
**EN:** You grip the jacket and the sleeve, enter with the hip or the leg and throw. In Beijing style the stress falls on particular entries; other centres hold the grip differently. There are no kicks scored as in sanda, and no knee clinch.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: nisko
**EN:** Striking: low

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: wysoko
**EN:** Clinch: high

**PL:** Rzuty: wysoko
**EN:** Throws: high

**PL:** Obalenia: wysoko
**EN:** Takedowns: high

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Bez broni
**EN:** No weapon

**PL:** Shuai jiao — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Kung fu — Encyclopaedia Britannica
**EN:** 

### taekkyeon — Taekkyeon

**PL:** Taekkyeon
**EN:** Taekkyeon

**PL:** Uderzenia
**EN:** Striking

**PL:** Taekkyeon to koreańska sztuka o płynnym, rytmicznym ruchu. Stopa jest tu tak ważna jak ręka, a akcja może być uderzeniem albo podcięciem. To nie jest taekwondo.
**EN:** Taekkyeon is a Korean art of fluid, rhythmic movement. The foot matters as much as the hand, and the action can be a strike or a trip. It is not taekwondo.

**PL:** Korea
**EN:** Korea

**PL:** Tradycja koreańska, wpis UNESCO w 2011
**EN:** A Korean tradition, UNESCO inscription in 2011

**PL:** Azja Wschodnia
**EN:** 

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** UNESCO wpisało taekkyeon w 2011 roku jako tradycyjną sztukę walki, nie jako regulamin World Taekwondo ani ITF. Wspólny kraj nie łączy tych praktyk w jeden sport.
**EN:** UNESCO inscribed taekkyeon in 2011 as a traditional martial art, not as the rulebook of World Taekwondo or the ITF. A shared country does not make these practices one sport.

**PL:** Ruch jest okrągły i rytmiczny, a potem może być ostry. Ćwiczy się uderzenia i podcięcia, nie kamizelkę elektroniczną i nie formy tul. Partner jest potrzebny, gdy z ruchu robi się walka.
**EN:** The movement is circular and rhythmic, and then it can be sharp. You practise strikes and trips, not an electronic chest guard and not tul forms. A partner is needed when the movement becomes a fight.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: średnio
**EN:** Striking: medium

**PL:** Pięści: średnio
**EN:** Punches: medium

**PL:** Kopnięcia: wysoko
**EN:** Kicks: high

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: średnio
**EN:** Grappling: medium

**PL:** Klincz: nisko
**EN:** Clinch: low

**PL:** Rzuty: średnio
**EN:** Throws: medium

**PL:** Obalenia: średnio
**EN:** Takedowns: medium

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: średnio
**EN:** Competition: medium

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: średnio
**EN:** Athletic demand: medium

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: nisko
**EN:** Equipment: low

**PL:** Praktyka tradycyjna
**EN:** Traditional practice

**PL:** Bez broni
**EN:** No weapon

**PL:** Taekkyeon, a traditional Korean martial art — UNESCO
**EN:** 

**PL:** Taekkyeon — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

### taijiquan — Taijiquan

**PL:** Taijiquan
**EN:** Taijiquan

**PL:** Mieszane
**EN:** Mixed

**PL:** To nazwa zbiorcza, nie jeden regulamin, więc ten opis nie pasuje do każdej szkoły ani sali.
**EN:** It's an umbrella name, not one rule set, so this description doesn't fit every school or hall.

**PL:** Taijiquan to chińska praktyka form, pchnięć rąk i własnej wersji sportowej. Nazwa zbiera szkoły, między innymi Chen, Yang, Wu, Sun i Wu (Hao). To nie jest skrót na całe wushu.
**EN:** Taijiquan is a Chinese practice of forms, push-hands and its own sport version. The name gathers schools, among them Chen, Yang, Wu, Sun and Wu (Hao). It is not an abbreviation for all of wushu.

**PL:** Chiny
**EN:** China

**PL:** Szkoły nowożytne, sportowa forma w XX wieku
**EN:** Modern schools, a sporting form in the 20th century

**PL:** Azja Wschodnia
**EN:** 

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Szkoły różnią się tempem, fajką ruchu i tym, ile zostawiają zastosowań. IWUF ułożyło z tego sportowe taolu, z osobnym czasem i listą wymaganych ruchów. Formy sportowe nie zastępują szkoły, z której wyszły.
**EN:** The schools differ in tempo, in the shape of the movement and in how much application they keep. The IWUF arranged a sport taolu from this, with its own time limit and a list of required movements. Sport forms do not replace the school they came from.

**PL:** Solo to układ, często wolny, czasem z ostrzejszym wypuszczeniem siły. W parze dochodzą pchnięcia rąk: wytrącenie równowagi bez ciosu jak w sandzie. Broń, na przykład miecz taiji, jest osobnym układem, nie walką na punkty.
**EN:** Solo work is a routine, often slow, sometimes with a sharper release of force. In pairs, push-hands are added: breaking balance without a strike as in sanda. A weapon, for example the taiji sword, is a separate routine, not a points fight.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: nisko
**EN:** Striking: low

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: średnio
**EN:** Kicks: medium

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: średnio
**EN:** Grappling: medium

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: średnio
**EN:** Throws: medium

**PL:** Obalenia: średnio
**EN:** Takedowns: medium

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: wysoko
**EN:** Solo training: high

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: nisko
**EN:** Contact: low

**PL:** Zawody: średnio
**EN:** Competition: medium

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: średnio
**EN:** Athletic demand: medium

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: nisko
**EN:** Equipment: low

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Broń opcjonalna
**EN:** Optional weapon

**PL:** Wushu taolu, including taijiquan — IWUF
**EN:** 

**PL:** Tai chi — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

### catch — Catch wrestling

**PL:** Catch wrestling
**EN:** Catch wrestling

**PL:** Chwyty
**EN:** Grappling

**PL:** Catch to zapasy, w których obok rzutu i kontroli jest poddanie: dźwignia albo duszenie. To nie jest olimpijski styl wolny ani klasyczny, bo tam walka nie idzie po dźwignię jako cel.
**EN:** Catch is wrestling in which a submission, a lock or a choke, sits beside the throw and the control. It is not Olympic freestyle or Greco-Roman, because those bouts do not go looking for a lock as the aim.

**PL:** Anglia i później Stany Zjednoczone, zapasy z poddaniami
**EN:** England and later the United States, wrestling with submissions

**PL:** XIX i XX wiek
**EN:** 19th and 20th centuries

**PL:** Europa / Ameryka Północna
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Catch-as-catch-can rozwinęło się w ramach brytyjskich tradycji zapaśniczych, a później stało się wpływowe w Stanach Zjednoczonych. Formy historyczne i współczesne różnią się regulaminami oraz tym, jak centralną rolę odgrywają poddania. Styl wolny i klasyczny pozostały odrębnymi stylami olimpijskimi z własnymi zasadami punktowania i zakończenia walki.
**EN:** Catch-as-catch-can developed within British wrestling traditions and later became influential in the United States. Historical and modern forms differ in rules and in how central submissions are. Freestyle and Greco-Roman remained separate Olympic styles with their own rules on points and falls.

**PL:** Schodzisz do chwytu, obalasz i szukasz pozycji, z której da się założyć dźwignię. Nie ma ciosów. Kurtki judo też zwykle nie ma: chwyt idzie na ciało i na staw.
**EN:** You level for the grip, take the opponent down and look for a position from which a lock can be put on. There are no strikes. A judo jacket is usually absent too: the grip goes to the body and the joint.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: nisko
**EN:** Striking: low

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: wysoko
**EN:** Throws: high

**PL:** Obalenia: wysoko
**EN:** Takedowns: high

**PL:** Parter: wysoko
**EN:** Ground fighting: high

**PL:** Poddania: wysoko
**EN:** Submissions: high

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: nisko
**EN:** Solo training: low

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: średnio
**EN:** Competition: medium

**PL:** Tradycja: średnio
**EN:** Tradition: medium

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: wysoko
**EN:** Endurance: high

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: nisko
**EN:** Equipment: low

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Bez broni
**EN:** No weapon

**PL:** Catch wrestling — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Wrestling — Encyclopaedia Britannica
**EN:** 

### luta-livre — Luta livre esportiva

**PL:** Luta livre esportiva
**EN:** Luta livre esportiva

**PL:** Chwyty
**EN:** Grappling

**PL:** Luta livre esportiva to brazylijski grappling bez kimona: obalenia, kontrola i poddania, bez uderzeń. Historycznie stała obok BJJ, a nie jako jego reguła no-gi.
**EN:** Luta livre esportiva is Brazilian grappling without the gi: takedowns, control and submissions, with no strikes. Historically it stood beside BJJ, not as BJJ's no-gi rule.

**PL:** Brazylia, grappling bez kimona
**EN:** Brazil, grappling without the gi

**PL:** XX wiek
**EN:** 20th century

**PL:** Ameryka Południowa
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** W Brazylii luta livre urosła jako zapasy z poddaniami, obok linii Gracie. Formuła esportiva zostawia ciosy na boku. Vale tudo, w którym uderzenia wracają, jest inną praktyką i bliższą wczesnemu MMA niż tej karcie.
**EN:** In Brazil luta livre grew as wrestling with submissions, beside the Gracie line. The esportiva format leaves strikes out. Vale tudo, where the strikes come back, is a different practice and closer to early MMA than to this card.

**PL:** Walczysz bez kimona. Chwyt idzie na nadgarstek, szyję i nogę, a nie na kołnierz. Sparing szuka poddania. To nie jest randori judo i nie jest punktowe BJJ w gi, nawet gdy część technik wygląda podobnie.
**EN:** You fight without the gi. The grip goes to the wrist, the neck and the leg, not to the collar. Sparring looks for a submission. It is not judo randori and it is not points BJJ in the gi, even when some techniques look alike.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: nisko
**EN:** Striking: low

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: średnio
**EN:** Throws: medium

**PL:** Obalenia: wysoko
**EN:** Takedowns: high

**PL:** Parter: wysoko
**EN:** Ground fighting: high

**PL:** Poddania: wysoko
**EN:** Submissions: high

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: nisko
**EN:** Solo training: low

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: średnio
**EN:** Tradition: medium

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: nisko
**EN:** Equipment: low

**PL:** Zawody
**EN:** Competition

**PL:** Bez broni
**EN:** No weapon

**PL:** Luta livre — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Luta livre esportiva — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

### iaido — Iaido

**PL:** Iaido
**EN:** Iaido

**PL:** Broń
**EN:** Weapons

**PL:** Iaido to formy z mieczem: dobyć, ciąć i schować, zwykle solo. All Japan Kendo Federation ma własny zestaw kata, ale iaido nie jest punktowanym kendo na shinai.
**EN:** Iaido is sword forms: draw, cut and sheathe, usually solo. The All Japan Kendo Federation has its own set of kata, but iaido is not scored kendo with a shinai.

**PL:** Japonia, formy dobycia miecza
**EN:** Japan, forms of drawing the sword

**PL:** Szkoły miecza, formy AJKF od 1969
**EN:** Sword schools, AJKF forms from 1969

**PL:** Azja Wschodnia
**EN:** 

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Z bronią
**EN:** Weapon-based

**PL:** Szkoły miecza są starsze niż wspólny katalog. W 1969 roku AJKF ułożyła standaryzowane kata, później rozszerzone, żeby dało się porównać wykonanie. Kenjutsu zostaje przy szkole i jej parach, bez tego katalogu i bez turnieju kendo.
**EN:** The sword schools are older than the shared catalogue. In 1969 the AJKF arranged standardised kata, later extended, so a performance could be compared. Kenjutsu stays with the school and its pairs, without that catalogue and without a kendo tournament.

**PL:** Ćwiczy się katalog form, często mieczem treningowym, czasem ostrzem pod nadzorem szkoły. Nie ma zbroi bogu ani punktu za men. Ocena, jeśli jest, dotyczy cięcia, postawy i dobycia, nie wymiany ciosów.
**EN:** You practise a catalogue of forms, often with a training sword, sometimes with a live blade under the school's supervision. There is no bogu armour and no point for a men strike. A score, if there is one, is about the cut, the posture and the draw, not an exchange of blows.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: nisko
**EN:** Striking: low

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: nisko
**EN:** Grappling: low

**PL:** Klincz: nisko
**EN:** Clinch: low

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: wysoko
**EN:** Weapons: high

**PL:** Trening
**EN:** Training

**PL:** Trening solo: wysoko
**EN:** Solo training: high

**PL:** Praca z partnerem: nisko
**EN:** Partner work: low

**PL:** Kontakt: nisko
**EN:** Contact: low

**PL:** Zawody: średnio
**EN:** Competition: medium

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: średnio
**EN:** Athletic demand: medium

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: wysoko
**EN:** Equipment: high

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Broń treningowa
**EN:** Training weapon

**PL:** The concept of iaido — AJKF
**EN:** 

**PL:** Iaido — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

### kyudo — Kyudo

**PL:** Kyudo
**EN:** Kyudo

**PL:** Broń
**EN:** Weapons

**PL:** Kyudo to japońskie łucznictwo jako budō: łuk, strzała, ceremonia strzału i trening postawy. To nie jest odmiana kendo i nie jest łucznictwem olimpijskim na czas.
**EN:** Kyudo is Japanese archery as budō: the bow, the arrow, the ceremony of the shot and training of posture. It is not a variant of kendo and it is not timed Olympic archery.

**PL:** Japonia, łucznictwo jako budō
**EN:** Japan, archery as budō

**PL:** Tradycja łucznictwa, współczesne federacje
**EN:** An archery tradition, contemporary federations

**PL:** Azja Wschodnia
**EN:** 

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Z bronią
**EN:** Weapon-based

**PL:** Łuk był w Japonii bronią, a potem drogą treningu. International Kyudo Federation, założona w 2006 roku, prowadzi zawody i egzaminy poza Japonią razem z All Nippon Kyudo Federation. Shinai i zbroja kendo nie wchodzą do tego sprzętu.
**EN:** The bow was a weapon in Japan, and later a way of training. The International Kyudo Federation, founded in 2006, runs contests and exams outside Japan together with the All Nippon Kyudo Federation. The kendo shinai and armour are not part of this kit.

**PL:** Stoisz, nakładasz strzałę i wypuszczasz ją w ustalonej formie. Partner nie zasłania się mieczem. Zawody są strzelaniem do mato, nie walką wręcz.
**EN:** You stand, nock the arrow and release it in a set form. A partner does not parry with a sword. Contests are shooting at a mato, not an unarmed fight.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: nisko
**EN:** Striking: low

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: nisko
**EN:** Grappling: low

**PL:** Klincz: nisko
**EN:** Clinch: low

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: wysoko
**EN:** Weapons: high

**PL:** Trening
**EN:** Training

**PL:** Trening solo: wysoko
**EN:** Solo training: high

**PL:** Praca z partnerem: nisko
**EN:** Partner work: low

**PL:** Kontakt: nisko
**EN:** Contact: low

**PL:** Zawody: średnio
**EN:** Competition: medium

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: średnio
**EN:** Athletic demand: medium

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: wysoko
**EN:** Equipment: high

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Broń główna
**EN:** Weapon first

**PL:** About the International Kyudo Federation — IKYF
**EN:** 

**PL:** Kyūdō — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

### bokh — Bökh

**PL:** Bökh
**EN:** Bökh

**PL:** Chwyty
**EN:** Grappling

**PL:** Bökh to mongolskie zapasy Naadam, nie nazwa całego święta. Charakterystyczne są strój zodog i shuudag, chwyt za górę ciała oraz zwycięstwo, gdy rywal dotknie ziemi w sposób określony przez lokalne zasady. Ciosów nie ma.
**EN:** Bökh is the Mongolian wrestling of Naadam, not the name of the whole festival. It is defined by the zodog and shuudag costume, an upper-body grip, and a win when the opponent touches the ground in a way defined by the local rules. There are no strikes.

**PL:** Mongolia
**EN:** Mongolia

**PL:** Święto naadam, tradycja zapasów
**EN:** The Naadam festival, a wrestling tradition

**PL:** Azja Środkowa
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Naadam składa się z zapasów, łucznictwa i wyścigów konnych. Bökh jest jedną z tych trzech rzeczy. Rytuał wejścia i strój są częścią zawodów, a nie przerywnikiem przed właściwą walką.
**EN:** Naadam is wrestling, archery and horse racing. Bökh is one of those three. The entrance ritual and the costume are part of the contest, not an interval before the real fight.

**PL:** Chwyt idzie za kurtkę i za tors. Starcie kończy się, gdy rywal dotknie ziemi w sposób określony przez lokalne zasady; szczegóły różnią się między odmianami. Nie ma pasa jak w ssireum, nie ma maty olimpijskiej i nie walczy się do upływu czasu w ten sam sposób co w stylu wolnym.
**EN:** The grip goes to the jacket and the torso. The bout ends when the opponent touches the ground in a way defined by the local rules; the details vary between variants. There is no belt as in ssireum, no Olympic mat, and it is not fought to the clock the way freestyle is.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: nisko
**EN:** Striking: low

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: wysoko
**EN:** Throws: high

**PL:** Obalenia: wysoko
**EN:** Takedowns: high

**PL:** Parter: średnio
**EN:** Ground fighting: medium

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: nisko
**EN:** Solo training: low

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: średnio
**EN:** Competition: medium

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Praktyka tradycyjna
**EN:** Traditional practice

**PL:** Bez broni
**EN:** No weapon

**PL:** Naadam w Mongolii to zapasy, łucznictwo i wyścigi konne. Bökh jest jedną z tych trzech konkurencji, a nie całym świętem.
**EN:** Naadam in Mongolia is wrestling, archery and horse racing. Bökh is one of those three contests, not the whole festival.

**PL:** Mongolian wrestling — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Mongolia — Encyclopaedia Britannica
**EN:** 

### ssireum — Ssireum

**PL:** Ssireum
**EN:** Ssireum

**PL:** Chwyty
**EN:** Grappling

**PL:** Ssireum to koreańskie zapasy na pasie satba, na piasku. Obejmujesz rywala za pas i rzucasz tak, by część ciała powyżej kolana dotknęła ziemi. UNESCO wpisało ssireum w 2018 roku jako tradycję wspólną dla obu Korei.
**EN:** Ssireum is Korean belt wrestling on sand, with the satba. You hold the opponent by the belt and throw so that a part of the body above the knee touches the ground. UNESCO inscribed ssireum in 2018 as a tradition shared by both Koreas.

**PL:** Korea
**EN:** Korea

**PL:** Tradycja zapasów, współczesne zawody
**EN:** A wrestling tradition, modern contests

**PL:** Azja Wschodnia
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Satba owija biodro i udo, więc chwyt ma stałe miejsce, inaczej niż w zapasach olimpijskich. W tradycyjnej formule dorosłych zwycięzca finału bywał nagradzany wołem. Współczesne zawody mają kategorie, ale piasek i pas zostają.
**EN:** The satba wraps the waist and the thigh, so the grip has a fixed place, unlike Olympic wrestling. In the traditional adult format the final winner used to receive an ox. Modern contests have divisions, but the sand and the belt remain.

**PL:** Nie łapiesz nogi jak w stylu wolnym. Siła idzie przez pas, a dotknięcie piasku tułowiem kończy akcję. To nie jest taekwondo i nie jest taekkyeon: nie ma kopnięć.
**EN:** You do not attack the leg the way you do in freestyle. The force goes through the belt, and the torso touching the sand ends the action. This is not taekwondo and it is not taekkyeon: there are no kicks.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: nisko
**EN:** Striking: low

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: wysoko
**EN:** Clinch: high

**PL:** Rzuty: wysoko
**EN:** Throws: high

**PL:** Obalenia: średnio
**EN:** Takedowns: medium

**PL:** Parter: średnio
**EN:** Ground fighting: medium

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: nisko
**EN:** Solo training: low

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Bez broni
**EN:** No weapon

**PL:** Ssireum — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Traditional Korean wrestling (Ssirum/Ssireum) — UNESCO
**EN:** 

### chidaoba — Chidaoba

**PL:** Chidaoba
**EN:** Chidaoba

**PL:** Chwyty
**EN:** Grappling

**PL:** Chidaoba to gruzińskie zapasy w stroju chokha. Wygrywa rzut przy chwytach, których katalog jest duży. Przy arenie grają zurna i doli. UNESCO wpisało chidaobę w 2018 roku.
**EN:** Chidaoba is Georgian wrestling in the chokha. A throw with a grip wins, and the catalogue of holds is large. Zurna and doli play by the arena. UNESCO inscribed chidaoba in 2018.

**PL:** Gruzja
**EN:** Georgia

**PL:** Tradycja zapasów
**EN:** A wrestling tradition

**PL:** Kaukaz
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Strój, muzyka i nazwy chwytów są częścią opisu, nie dodatkiem folklorystycznym. To nie jest styl klasyczny na macie UWW: inna przestrzeń, inny chwyt i inne zakończenie akcji.
**EN:** The costume, the music and the names of the holds are part of the description, not a folklore extra. This is not Greco-Roman on a UWW mat: a different space, a different grip and a different way to end the action.

**PL:** Walczy się w chwycie za strój i za ciało, bez ciosów. Upadek rywala rozstrzyga. Muzyka i tradycyjna oprawa pozostają częścią otoczenia walki, obok zasad samego konkursu.
**EN:** You fight by gripping the costume and the body, with no strikes. The opponent's fall decides it. Music and traditional presentation remain part of the setting, alongside the rules of the contest.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: nisko
**EN:** Striking: low

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: wysoko
**EN:** Throws: high

**PL:** Obalenia: średnio
**EN:** Takedowns: medium

**PL:** Parter: średnio
**EN:** Ground fighting: medium

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: nisko
**EN:** Solo training: low

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: średnio
**EN:** Competition: medium

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Praktyka tradycyjna
**EN:** Traditional practice

**PL:** Bez broni
**EN:** No weapon

**PL:** Chidaoba, wrestling in Georgia — UNESCO
**EN:** 

**PL:** Chidaoba — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

### laamb — Laamb

**PL:** Laamb
**EN:** Laamb

**PL:** Mieszane
**EN:** Mixed

**PL:** Laamb to senegalskie zapasy. W formule avec frappe dochodzą uderzenia, a w formule bez uderzeń zostają chwyty i rzuty. Jedna nazwa nie znaczy jednego regulaminu.
**EN:** Laamb is Senegalese wrestling. The avec frappe format adds strikes, and the format without strikes stays with grips and throws. One name does not mean one rule set.

**PL:** Senegal
**EN:** Senegal

**PL:** Tradycja zapasów, współczesne gale
**EN:** A wrestling tradition, modern cards

**PL:** Afryka Zachodnia
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Walka zapaśnicza jest w Senegalu dużym widowiskiem, z własnym polem i z ceremonią wejścia. Gale z frappe to warstwa nowsza. Nie da się tego wpisu sprowadzić do zdania „chwyty, rzuty, bez uderzeń”.
**EN:** Wrestling is a major spectacle in Senegal, with its own ground and an entrance ceremony. Cards with frappe are a newer layer. This entry cannot be reduced to the sentence “grips, throws, no strikes”.

**PL:** W formule bez uderzeń szukasz rzutu na ziemię. W formule z uderzeniami (frappe) wolno bić, zanim dojdzie do chwytu. Pole nie jest matą olimpijską, a koniec walki zależy od formuły, nie od wspólnego przepisu z bökh.
**EN:** In the format without strikes you look for a throw to the ground. In the avec frappe format you may strike before the grip. The ground is not an Olympic mat, and the end of the fight depends on the format, not on a rule shared with bökh.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: średnio
**EN:** Striking: medium

**PL:** Pięści: średnio
**EN:** Punches: medium

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: średnio
**EN:** Throws: medium

**PL:** Obalenia: wysoko
**EN:** Takedowns: high

**PL:** Parter: średnio
**EN:** Ground fighting: medium

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: nisko
**EN:** Solo training: low

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: nisko
**EN:** Equipment: low

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Bez broni
**EN:** No weapon

**PL:** Senegalese wrestling — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Senegal — Encyclopaedia Britannica
**EN:** 

### glima — Glíma

**PL:** Glíma
**EN:** Glíma

**PL:** Chwyty
**EN:** Grappling

**PL:** Glíma to islandzkie zapasy, najczęściej w pasie, z ruchem po kole. Rzut kończy akcję. Uderzeń nie ma. Średniowiecznej ciągłości nie da się tu dowieść z samego treningu.
**EN:** Glíma is Icelandic wrestling, most often with a belt, moving in a circle. A throw ends the action. There are no strikes. Medieval continuity cannot be proved from the training alone.

**PL:** Islandia
**EN:** Iceland

**PL:** Tradycja zapasów, opisana też w XIX i XX wieku
**EN:** A wrestling tradition, also described in the 19th–20th centuries

**PL:** Europa Północna
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Pas i krok po okręgu odróżniają glímę od stylu wolnego. Opowieść o linii prostej od sag jest słabsza niż opis samego chwytu, więc zostawiam ją jako opowieść, nie jako metrykę.
**EN:** The belt and the circular step distinguish glíma from freestyle. A story of a straight line from the sagas is weaker than the description of the grip itself, so I leave it as a story, not as a certificate.

**PL:** Stoisz w pasie, trzymasz uchwyt i wytrącasz rywala z równowagi w ruchu, nie w klinczu olimpijskim. Dotknięcie ziemi po rzucie rozstrzyga. Nie ma piasku ssireum ani kurtki bökh.
**EN:** You stand in the belt, hold the grip and break balance on the move, not in an Olympic clinch. The ground after a throw decides it. There is no ssireum sand and no bökh jacket.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: nisko
**EN:** Striking: low

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: wysoko
**EN:** Throws: high

**PL:** Obalenia: średnio
**EN:** Takedowns: medium

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: średnio
**EN:** Competition: medium

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Praktyka tradycyjna
**EN:** Traditional practice

**PL:** Bez broni
**EN:** No weapon

**PL:** Glíma — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Iceland — Encyclopaedia Britannica
**EN:** 

### alysh — Alysh

**PL:** Alysh
**EN:** Alysh

**PL:** Chwyty
**EN:** Grappling

**PL:** Alysh to środkowoazjatyckie zapasy na pasie, szczególnie w Kirgistanie. Chwyt idzie na pas, a rzut kończy akcję. To nie jest kurash, choć region jest ten sam.
**EN:** Alysh is Central Asian belt wrestling, especially in Kyrgyzstan. The grip goes to the belt, and a throw ends the action. It is not kurash, even though the region is the same.

**PL:** Azja Środkowa, zwłaszcza Kirgistan
**EN:** Central Asia, especially Kyrgyzstan

**PL:** Tradycja zapasów na pasie
**EN:** A belt-wrestling tradition

**PL:** Azja Środkowa
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Międzynarodowe starty są nowszą ramą na starszych zapasach ludowych. Kurash ma własny chwyt za kurtkę i własną federację. Wspólna mapa nie zrówna pasa z kurtką.
**EN:** International starts are a newer frame on older folk wrestling. Kurash has its own jacket grip and its own federation. A shared map does not make a belt and a jacket the same.

**PL:** Trzymasz pas obiema rękami i wchodzisz na rzut biodrem. Ciosów nie ma. Nie można opisać tego jako stylu wolnego: pas wyznacza chwyt od początku, a walka ma własne zasady.
**EN:** You hold the belt with both hands and enter a hip throw. There are no strikes. It cannot be described as freestyle: the belt fixes the grip from the start and the bout follows its own rules.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: nisko
**EN:** Striking: low

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: wysoko
**EN:** Throws: high

**PL:** Obalenia: średnio
**EN:** Takedowns: medium

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: nisko
**EN:** Solo training: low

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: średnio
**EN:** Competition: medium

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Bez broni
**EN:** No weapon

**PL:** Alysh — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** United World Wrestling — UWW
**EN:** 

### kurash — Kurash

**PL:** Kurash
**EN:** Kurash

**PL:** Chwyty
**EN:** Grappling

**PL:** Kurash to uzbeckie zapasy w kurtce. Chwyt za połę rozstrzyga rzut, bez walki w parterze po upadku. To nie jest alysh na pasie i nie jest judo, mimo podobnej kurtki.
**EN:** Kurash is Uzbek jacket wrestling. A grip on the jacket decides the throw, with no ground fight after the fall. It is not belt alysh and it is not judo, even with a similar jacket.

**PL:** Uzbekistan i Azja Środkowa
**EN:** Uzbekistan and Central Asia

**PL:** Tradycja zapasów, federacja międzynarodowa w XX wieku
**EN:** A wrestling tradition, an international federation in the 20th century

**PL:** Azja Środkowa
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Międzynarodowa federacja kurash uporządkowała zawody w XX i XXI wieku. Starsza praktyka jest środkowoazjatycka. Alysh zostaje przy pasie, sambo przy własnej kurtce i przy dźwigniach, których tu nie ma.
**EN:** The international kurash federation tidied the contests in the twentieth and twenty-first centuries. The older practice is Central Asian. Alysh stays with the belt, sambo with its own jacket and with locks that are not part of this.

**PL:** Rzut zgodny z regulaminem może dać punkty albo zakończyć walkę, a akcja nie jest kontynuowana w parterze. Uderzeń nie ma. Kurtka jest częścią zasad walki, a nie tylko strojem.
**EN:** A throw under the rules can score or end the bout, and the action does not continue on the ground. There are no strikes. The jacket is part of the rules, not only the costume.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: nisko
**EN:** Striking: low

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: wysoko
**EN:** Grappling: high

**PL:** Klincz: średnio
**EN:** Clinch: medium

**PL:** Rzuty: wysoko
**EN:** Throws: high

**PL:** Obalenia: średnio
**EN:** Takedowns: medium

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: nisko
**EN:** Solo training: low

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: wysoko
**EN:** Competition: high

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Zawody i tradycja
**EN:** Competition and tradition

**PL:** Bez broni
**EN:** No weapon

**PL:** International Kurash Association — IKA
**EN:** 

**PL:** Kurash — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

### gatka — Gatka

**PL:** Gatka
**EN:** Gatka

**PL:** Broń
**EN:** Weapons

**PL:** Gatka to sikhijska sztuka broni, ćwiczona kijem, mieczem i innymi narzędziami, często przy pokazach i przy nagar kirtan.
**EN:** Gatka is a Sikh weapon art, practised with a stick, a sword and other tools, often at demonstrations and at nagar kirtan.

**PL:** Pendżab
**EN:** Punjab

**PL:** Tradycja sikhijska, odnowa w XX wieku
**EN:** A Sikh tradition, a revival in the 20th century

**PL:** Azja Południowa
**EN:** 

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Z bronią
**EN:** Weapon-based

**PL:** Broń i wspólnota sikhijska są kontekstem, nie ozdobnikiem. Współczesne szkoły uczą gatki zarówno jako praktyki walki, jak i tradycji kulturowej i religijnej. Nie jest to HEMA ani kendo: inne źródła, inna broń i inny kontekst.
**EN:** Weapons and the Sikh community are the context, not decoration. Contemporary schools teach gatka both as a martial practice and as a cultural and religious tradition. It is not HEMA and it is not kendo: different sources, different weapons and a different context.

**PL:** Ćwiczy się formy i pary na kiju oraz na broni, często w ruchu kołowym. Kontakt turniejowy nie jest tu osią, tak jak w szermierce. Pokaz i szkolenie religijnej wspólnoty zostają częścią praktyki.
**EN:** You drill forms and pairs with a stick and with weapons, often in a circular movement. Tournament contact is not the axis, the way it is in fencing. The demonstration and the training of a religious community stay part of the practice.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: średnio
**EN:** Striking: medium

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: nisko
**EN:** Kicks: low

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: nisko
**EN:** Grappling: low

**PL:** Klincz: nisko
**EN:** Clinch: low

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: wysoko
**EN:** Weapons: high

**PL:** Trening
**EN:** Training

**PL:** Trening solo: wysoko
**EN:** Solo training: high

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: nisko
**EN:** Competition: low

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: średnio
**EN:** Athletic demand: medium

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: wysoko
**EN:** Equipment: high

**PL:** Praktyka tradycyjna
**EN:** Traditional practice

**PL:** Broń treningowa
**EN:** Training weapon

**PL:** Gatka — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Sikhism — Encyclopaedia Britannica
**EN:** 

### kalaripayattu — Kalaripayattu

**PL:** Kalaripayattu
**EN:** Kalaripayattu

**PL:** Mieszane
**EN:** Mixed

**PL:** Nie da się uczciwie podać jednej wersji, źródła są niejasne.
**EN:** There's no honest single version — the sources are unclear.

**PL:** Kalaripayattu to sztuka z Kerali, ćwiczona w kalari, czyli często zagłębionej sali treningowej. Są nurty północny i południowy, formy, broń i praca z ciałem. To nie jest indyjska nazwa na kickboxing.
**EN:** Kalaripayattu is an art from Kerala, practised in a kalari, a training space that is often sunken. There are northern and southern currents, forms, weapons and body work. It is not an Indian name for kickboxing.

**PL:** Kerala, Indie
**EN:** Kerala, India

**PL:** Tradycja keralijska
**EN:** A Kerala tradition

**PL:** Azja Południowa
**EN:** 

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Z bronią
**EN:** Weapon-based

**PL:** Północne i południowe style różnią się formami, bronią oraz naciskiem na masaż i leczenie w tradycji kalari. Źródła dotyczące nieprzerwanej średniowiecznej ciągłości są słabsze niż źródła opisujące samą praktykę w Kerali, dlatego karta nie sprowadza ich do jednej daty założenia.
**EN:** Northern and southern styles differ in forms, weapons and in the emphasis placed on massage and treatment in the kalari tradition. Sources for a medieval unbroken line are thinner than the description of the practice in Kerala, so the card does not turn them into one founding date.

**PL:** Rozgrzewka i formy idą przed bronią: kij, sztylet, miecz i tarcza zależnie od nurtu. Pusta ręka jest w zestawie, ale sala kalari i sekwencje nie wyglądają jak runda na ringu. Partner jest potrzebny przy broni i przy zastosowaniach.
**EN:** Warm-up and forms come before weapons: stick, dagger, sword and shield, depending on the current. The empty hand is in the set, but the kalari and the sequences do not look like a round in a ring. A partner is needed for weapons and for applications.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: średnio
**EN:** Striking: medium

**PL:** Pięści: nisko
**EN:** Punches: low

**PL:** Kopnięcia: wysoko
**EN:** Kicks: high

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: średnio
**EN:** Grappling: medium

**PL:** Klincz: nisko
**EN:** Clinch: low

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: wysoko
**EN:** Weapons: high

**PL:** Trening
**EN:** Training

**PL:** Trening solo: wysoko
**EN:** Solo training: high

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: średnio
**EN:** Contact: medium

**PL:** Zawody: nisko
**EN:** Competition: low

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: wysoko
**EN:** Technical complexity: high

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: średnio
**EN:** Explosiveness: medium

**PL:** Sprzęt: średnio
**EN:** Equipment: medium

**PL:** Praktyka tradycyjna
**EN:** Traditional practice

**PL:** Broń treningowa
**EN:** Training weapon

**PL:** Kalaripayattu — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Kerala — Encyclopaedia Britannica
**EN:** 

### dambe — Dambe

**PL:** Dambe
**EN:** Dambe

**PL:** Uderzenia
**EN:** Striking

**PL:** Dambe to tradycyjna sztuka walki wywodząca się z kultury ludu Hausa w Afryce Zachodniej. Charakteryzuje się owijaniem jednej ręki w charakterystyczny sposób oraz wykorzystaniem kopnięć. Różni się od boksu w rękawicach.
**EN:** Dambe is a fighting style that comes from Hausa tradition. Traditionally one hand is wrapped in a distinctive way, and kicks also appear in the fight. It is something different from gloved boxing.

**PL:** Lud Hausa, Afryka Zachodnia
**EN:** The Hausa people, West Africa

**PL:** Tradycja walki pięścią i kopnięciem
**EN:** A fist-and-kick fighting tradition

**PL:** Afryka Zachodnia
**EN:** 

**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Dambe jest ściśle związane z kulturą Hausa i historycznie z określonymi grupami zawodowymi oraz pokazami. Współczesne pojedynki mogą różnić się od tradycyjnych starć pod względem zabezpieczeń i zasad sędziowania.
**EN:** Dambe is tied to Hausa tradition, historically also to particular occupational groups and to shows. Modern events can change protection, judging and other details, so not every modern bout looks identical to a traditional fight.

**PL:** Walczy się z owiniętą pięścią, w gardzie, z kopnięciami. Kontakt jest częścią tradycyjnego starcia.
**EN:** You fight with a wrapped fist, in a guard, with kicks. Contact is part of the traditional bout.

**PL:** Oceny (nisko / średnio / wysoko) mówią, jak mocno dany element występuje w typowym treningu — to nie ranking siły ani umiejętności.
**EN:** 

**PL:** nisko — prawie nie występuje albo niewielkie nastawienie.
**EN:** 

**PL:** średnio — umiarkowanie: bywa, ale nie dominuje.
**EN:** 

**PL:** wysoko — wyraźnie ważne i regularne w treningu.
**EN:** 

**PL:** Uderzenia
**EN:** Striking

**PL:** Uderzenia: wysoko
**EN:** Striking: high

**PL:** Pięści: wysoko
**EN:** Punches: high

**PL:** Kopnięcia: średnio
**EN:** Kicks: medium

**PL:** Kolana: nisko
**EN:** Knees: low

**PL:** Łokcie: nisko
**EN:** Elbows: low

**PL:** Chwyt
**EN:** Grappling

**PL:** Chwyt: nisko
**EN:** Grappling: low

**PL:** Klincz: nisko
**EN:** Clinch: low

**PL:** Rzuty: nisko
**EN:** Throws: low

**PL:** Obalenia: nisko
**EN:** Takedowns: low

**PL:** Parter: nisko
**EN:** Ground fighting: low

**PL:** Poddania: nisko
**EN:** Submissions: low

**PL:** Broń
**EN:** Weapons

**PL:** Broń: nisko
**EN:** Weapons: low

**PL:** Trening
**EN:** Training

**PL:** Trening solo: średnio
**EN:** Solo training: medium

**PL:** Praca z partnerem: wysoko
**EN:** Partner work: high

**PL:** Kontakt: wysoko
**EN:** Contact: high

**PL:** Zawody: średnio
**EN:** Competition: medium

**PL:** Tradycja: wysoko
**EN:** Tradition: high

**PL:** Złożoność techniczna: średnio
**EN:** Technical complexity: medium

**PL:** Obciążenie fizyczne: wysoko
**EN:** Athletic demand: high

**PL:** Wytrzymałość: średnio
**EN:** Endurance: medium

**PL:** Eksplozywność: wysoko
**EN:** Explosiveness: high

**PL:** Sprzęt: nisko
**EN:** Equipment: low

**PL:** Praktyka tradycyjna
**EN:** Traditional practice

**PL:** Bez broni
**EN:** No weapon

**PL:** Dambe — Wikipedia contributors — CC BY-SA 4.0
**EN:** 

**PL:** Hausa — Encyclopaedia Britannica
**EN:** 

## 5. Quizopasowanie — pytania

**PL:** Jak bardzo chcesz uderzać?
**EN:** How much do you want to strike?

**PL:** Jak bardzo chcesz chwytać i trzymać?
**EN:** How much do you want to grapple and hold?

**PL:** Jak bardzo chcesz walczyć w parterze?
**EN:** How much do you want to fight on the ground?

**PL:** Jak bardzo chcesz mieć broń na treningu?
**EN:** How much do you want a weapon in training?

**PL:** Jak bardzo chcesz kopać?
**EN:** How much do you want to kick?

**PL:** Jak mocny ma być kontakt?
**EN:** How hard should the contact be?

**PL:** Jak bardzo chcesz startować w zawodach?
**EN:** How much do you want to compete?

**PL:** Jak ważne są dla Ciebie tradycje i zwyczaje w sali?
**EN:** How much do traditions and hall customs matter to you?

**PL:** Wolisz ćwiczyć sam czy z partnerem?
**EN:** Would you rather train alone, or with a partner?

**PL:** Sam, technika albo worek.
**EN:** Alone, with technique or a bag.

**PL:** Z partnerem, który się rusza.
**EN:** With a partner who moves.

**PL:** Wolisz zostać daleko czy wejść blisko?
**EN:** Would you rather stay far, or step in close?

**PL:** Z daleka, niech noga robi robotę.
**EN:** At a distance, let the leg do the work.

**PL:** Z bliska, klincz albo chwyt.
**EN:** Up close, a clinch or a grip.

**PL:** Na treningu dochodzi do zwarcia. Co ma być dalej?
**EN:** In training it comes to close range. What should happen next?

**PL:** Rzut.
**EN:** A throw.

**PL:** Schodzicie do parteru i szukacie poddania.
**EN:** You go to the ground and look for a submission.

**PL:** Uderzenie i odskok.
**EN:** A strike and a step out.

**PL:** Zaznacz, co ma być w Twoim tygodniu treningowym. Możesz wybrać kilka rzeczy naraz, a jeśli nic z tego Cię nie rusza, zostaw puste.
**EN:** Tick what should be in your training week. You can pick several, or leave it blank if none of it matters to you.

**PL:** Kolana i łokcie.
**EN:** Knees and elbows.

**PL:** Zbroja albo maska.
**EN:** Armour or a mask.

**PL:** Rękawice.
**EN:** Gloves.

**PL:** Wytrzymałość, długie rundy.
**EN:** Endurance, long rounds.

**PL:** Szybkie, mocne wejście.
**EN:** An explosive entry.

**PL:** Nic z tego.
**EN:** None of these.

## 6. Badania (porównanie)



## 7. Teksty dopasowania i porównania

**PL:** nisko
**EN:** low

**PL:** średnio
**EN:** medium

**PL:** wysoko
**EN:** high

**PL:** Obciążenie ciała jest tu mniej więcej takie, jakiego szukasz.
**EN:** The physical demand is about what you're after.

**PL:** Ciało jest tu obciążane mocniej, niż chcesz.
**EN:** The body is loaded harder here than you want.

**PL:** Ciało jest tu obciążane lżej, niż chcesz.
**EN:** The body is loaded lighter here than you want.

**PL:** Walka w zwarciu jest tu mniej więcej tak ważna, jak chcesz.
**EN:** Close-range work matters here about as much as you want.

**PL:** Zwarcia jest tu więcej, niż szukasz.
**EN:** There's more close-range work here than you're after.

**PL:** Zwarcia jest tu mniej, niż szukasz.
**EN:** There's less close-range work here than you're after.

**PL:** Zawodów jest tu mniej więcej tyle, ile chcesz.
**EN:** There's about as much competition here as you want.

**PL:** Zawody są tu ważniejsze, niż szukasz.
**EN:** Competition matters more here than you're after.

**PL:** Zawody są tu mniej ważne, niż szukasz.
**EN:** Competition matters less here than you're after.

**PL:** Poziom kontaktu pasuje do tego, czego szukasz.
**EN:** The amount of contact fits what you're after.

**PL:** Kontakt jest mocniejszy, niż chcesz.
**EN:** The contact is harder than you want.

**PL:** Kontakt jest lżejszy, niż chcesz.
**EN:** The contact is lighter than you want.

**PL:** Łokcie są tu mniej więcej tak ważne, jak chcesz.
**EN:** Elbows matter here about as much as you want.

**PL:** Łokcie liczą się tu bardziej, niż szukasz.
**EN:** Elbows matter more here than you're after.

**PL:** Łokcie liczą się tu mniej, niż szukasz.
**EN:** Elbows matter less here than you're after.

**PL:** Wytrzymałość jest tu mniej więcej tak ważna, jak chcesz.
**EN:** Endurance matters here about as much as you want.

**PL:** Wytrzymałości trzeba tu więcej, niż szukasz.
**EN:** It takes more endurance here than you're after.

**PL:** Wytrzymałości trzeba tu mniej, niż szukasz.
**EN:** It takes less endurance here than you're after.

**PL:** Sprzętu jest tu mniej więcej tyle, ile chcesz.
**EN:** There's about as much kit here as you want.

**PL:** Sprzętu jest tu więcej, niż potrzebujesz.
**EN:** There's more kit here than you need.

**PL:** Sprzętu jest tu mniej, niż potrzebujesz.
**EN:** There's less kit here than you need.

**PL:** Tempo i zryw pasują do tego, czego szukasz.
**EN:** The pace and the burst fit what you're after.

**PL:** Jest tu więcej zrywu, niż chcesz.
**EN:** There's more burst here than you want.

**PL:** Jest tu mniej zrywu, niż chcesz.
**EN:** There's less burst here than you want.

**PL:** Chcesz dużo chwytów i tutaj jest ich dużo.
**EN:** You want a lot of grappling, and there's a lot of it here.

**PL:** Chwytów jest tu więcej, niż szukasz.
**EN:** There's more grappling here than you're after.

**PL:** Chwytów jest tu mniej, niż szukasz.
**EN:** There's less grappling here than you're after.

**PL:** Parteru jest tu mniej więcej tyle, ile chcesz.
**EN:** There's about as much ground work here as you want.

**PL:** Parteru jest tu więcej, niż szukasz.
**EN:** There's more ground work here than you're after.

**PL:** Parteru jest tu mniej, niż szukasz.
**EN:** There's less ground work here than you're after.

**PL:** Kopnięcia są tu mniej więcej tak częste, jak chcesz.
**EN:** Kicks are about as common here as you want.

**PL:** Kopnięć jest tu więcej, niż szukasz.
**EN:** There are more kicks here than you're after.

**PL:** Kopnięć jest tu mniej, niż szukasz.
**EN:** There are fewer kicks here than you're after.

**PL:** Kolana są tu mniej więcej tak ważne, jak chcesz.
**EN:** Knees matter here about as much as you want.

**PL:** Kolana liczą się tu bardziej, niż szukasz.
**EN:** Knees matter more here than you're after.

**PL:** Kolana liczą się tu mniej, niż szukasz.
**EN:** Knees matter less here than you're after.

**PL:** Praca z partnerem jest tu mniej więcej tak ważna, jak chcesz.
**EN:** Partner work matters here about as much as you want.

**PL:** Pracy z partnerem jest tu więcej, niż szukasz.
**EN:** There's more partner work here than you're after.

**PL:** Pracy z partnerem jest tu mniej, niż szukasz.
**EN:** There's less partner work here than you're after.

**PL:** Praca pięścią jest tu mniej więcej tak ważna, jak chcesz.
**EN:** Fist work matters here about as much as you want.

**PL:** Pięści liczą się tu bardziej, niż szukasz.
**EN:** Fists matter more here than you're after.

**PL:** Pięści liczą się tu mniej, niż szukasz.
**EN:** Fists matter less here than you're after.

**PL:** Jest tu miejsce na pracę solo, której szukasz.
**EN:** There's room here for the solo work you're after.

**PL:** Pracy solo jest tu więcej, niż potrzebujesz.
**EN:** There's more solo work here than you need.

**PL:** Pracy solo jest tu mniej, niż szukasz.
**EN:** There's less solo work here than you're after.

**PL:** Chcesz dużo uderzeń i tutaj jest ich dużo.
**EN:** You want a lot of striking, and there's a lot of it here.

**PL:** Uderzeń jest tu więcej, niż szukasz.
**EN:** There's more striking here than you're after.

**PL:** Uderzeń jest tu mniej, niż szukasz.
**EN:** There's less striking here than you're after.

**PL:** Szukanie poddania pasuje do tego treningu mniej więcej tak, jak chcesz.
**EN:** Going for a submission fits this training about as much as you want.

**PL:** Poddania liczą się tu bardziej, niż szukasz.
**EN:** Submissions matter more here than you're after.

**PL:** Poddania liczą się tu mniej, niż szukasz.
**EN:** Submissions matter less here than you're after.

**PL:** Obaleń jest tu mniej więcej tyle, ile chcesz.
**EN:** There are about as many takedowns here as you want.

**PL:** Obaleń jest tu więcej, niż szukasz.
**EN:** There are more takedowns here than you're after.

**PL:** Obaleń jest tu mniej, niż szukasz.
**EN:** There are fewer takedowns here than you're after.

**PL:** Złożoność techniczna pasuje do tego, czego szukasz.
**EN:** The technical load fits what you're after.

**PL:** Techniki jest tu więcej, niż szukasz.
**EN:** There's more technique here than you're after.

**PL:** Techniki jest tu mniej, niż szukasz.
**EN:** There's less technique here than you're after.

**PL:** Rzuty są tu mniej więcej tak ważne, jak chcesz.
**EN:** Throws matter here about as much as you want.

**PL:** Rzutów jest tu więcej, niż szukasz.
**EN:** There are more throws here than you're after.

**PL:** Rzutów jest tu mniej, niż szukasz.
**EN:** There are fewer throws here than you're after.

**PL:** Zwyczajów i tradycji w sali jest tu mniej więcej tyle, ile chcesz.
**EN:** There's about as much hall custom and tradition here as you want.

**PL:** Zwyczajów i tradycji w sali jest tu więcej, niż szukasz.
**EN:** There's more hall custom and tradition here than you're after.

**PL:** Zwyczajów i tradycji w sali jest tu mniej, niż szukasz.
**EN:** There's less hall custom and tradition here than you're after.

**PL:** Broń na tym treningu jest mniej więcej tak ważna, jak chcesz.
**EN:** Weapons matter in this training about as much as you want.

**PL:** Broń jest tu ważniejsza, niż szukasz.
**EN:** Weapons matter more here than you're after.

**PL:** Broń jest tu mniej ważna, niż szukasz.
**EN:** Weapons matter less here than you're after.

**PL:** Obciążenia fizycznego jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** The physical demand is low here — and that's what you want.

**PL:** Zwarcia jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little close-range work here — and that's what you want.

**PL:** Zawodów jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little competition here — and that's what you want.

**PL:** Kontaktu jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little contact here — and that's what you want.

**PL:** Łokcie prawie tu nie mają znaczenia — i dobrze, bo właśnie tego szukasz.
**EN:** Elbows barely matter here — and that's what you want.

**PL:** Nie trzeba jej tu wiele — i dobrze, bo właśnie tego szukasz.
**EN:** You don't need much endurance here — and that's what you want.

**PL:** Sprzętu jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little kit here — and that's what you want.

**PL:** Zrywu jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little burst here — and that's what you want.

**PL:** Chwytów jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little grappling here — and that's what you want.

**PL:** Parteru jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little ground work here — and that's what you want.

**PL:** Kopnięć jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There are few kicks here — and that's what you want.

**PL:** Kolana prawie tu nie mają znaczenia — i dobrze, bo właśnie tego szukasz.
**EN:** Knees barely matter here — and that's what you want.

**PL:** Pracy z partnerem jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little partner work here — and that's what you want.

**PL:** Pięści prawie tu nie mają znaczenia — i dobrze, bo właśnie tego szukasz.
**EN:** Fists barely matter here — and that's what you want.

**PL:** Pracy solo jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little solo work here — and that's what you want.

**PL:** Uderzeń jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little striking here — and that's what you want.

**PL:** Poddania prawie tu nie mają znaczenia — i dobrze, bo właśnie tego szukasz.
**EN:** Submissions barely matter here — and that's what you want.

**PL:** Obaleń jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There are few takedowns here — and that's what you want.

**PL:** Technicznie jest tu prościej — i dobrze, bo właśnie tego szukasz.
**EN:** Technically it's simpler here — and that's what you want.

**PL:** Rzutów jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There are few throws here — and that's what you want.

**PL:** Zwyczajów i tradycji w sali jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little hall custom and tradition here — and that's what you want.

**PL:** Broni jest tu prawie nie ma — i dobrze, bo właśnie tego szukasz.
**EN:** There's almost no weapon here — and that's what you want.

**PL:** {higher} bardziej obciąża ciało niż {lower}.
**EN:** {higher} loads the body more than {lower}.

**PL:** {higher} spędza więcej czasu w zwarciu niż {lower}.
**EN:** {higher} spends more time at close range than {lower}.

**PL:** {higher} przykłada większą wagę do zawodów niż {lower}.
**EN:** {higher} puts more weight on competition than {lower}.

**PL:** {higher} trenuje z mocniejszym kontaktem niż {lower}.
**EN:** {higher} trains with harder contact than {lower}.

**PL:** {higher} częściej używa łokci niż {lower}.
**EN:** {higher} uses elbows more often than {lower}.

**PL:** {higher} wymaga większej wytrzymałości niż {lower}.
**EN:** {higher} asks more of your endurance than {lower}.

**PL:** {higher} wymaga więcej sprzętu niż {lower}.
**EN:** {higher} needs more kit than {lower}.

**PL:** {higher} ma więcej zrywu niż {lower}.
**EN:** {higher} is more explosive than {lower}.

**PL:** {higher} ma więcej chwytów niż {lower}.
**EN:** {higher} has more grappling than {lower}.

**PL:** {higher} dłużej zostaje w parterze niż {lower}.
**EN:** {higher} stays on the ground longer than {lower}.

**PL:** {higher} więcej kopie niż {lower}.
**EN:** {higher} kicks more than {lower}.

**PL:** {higher} częściej używa kolan niż {lower}.
**EN:** {higher} uses knees more often than {lower}.

**PL:** {higher} bardziej potrzebuje partnera niż {lower}.
**EN:** {higher} needs a partner more than {lower}.

**PL:** {higher} więcej pracuje pięściami niż {lower}.
**EN:** {higher} uses the fists more than {lower}.

**PL:** {higher} zostawia więcej miejsca na pracę solo niż {lower}.
**EN:** {higher} leaves more room for solo practice than {lower}.

**PL:** {higher} ma więcej uderzeń niż {lower}.
**EN:** {higher} has more striking than {lower}.

**PL:** {higher} częściej szuka poddania niż {lower}.
**EN:** {higher} looks for a submission more often than {lower}.

**PL:** {higher} częściej próbuje obalić rywala niż {lower}.
**EN:** {higher} goes for takedowns more often than {lower}.

**PL:** {higher} ma bardziej rozbudowany arsenał technik niż {lower}.
**EN:** {higher} has a broader technical arsenal than {lower}.

**PL:** {higher} mocniej opiera się na rzutach niż {lower}.
**EN:** {higher} leans on throws more than {lower}.

**PL:** {higher} przykłada większą wagę do tradycji sali niż {lower}.
**EN:** {higher} puts more weight on the hall's traditions than {lower}.

**PL:** {higher} wyraźniej stawia na broń niż {lower}.
**EN:** {higher} puts more weight on weapons than {lower}.

## Załącznik: SEO

**PL:** wiciędze
**EN:** wiciędze

**PL:** Katalog sportów i sztuk walki, sprawdzenie, czego szukasz na treningu, porównywarka i trochę beki.
**EN:** A catalog of combat sports and martial arts, a check of what you want from training, a comparison tool and a bit of a laugh.

**PL:** Obczaj różne sporty i sztuki walki — możesz je też porównywać.
**EN:** Check out all kinds of combat sports and martial arts — you can compare them too.

**PL:** Katalog | wiciędze
**EN:** Catalog | wiciędze

**PL:** {{ style.summary_pl }}
**EN:** {{ style.summary_en }}

**PL:** {{ style.name_pl }} | wiciędze
**EN:** {{ style.name_en }} | wiciędze

**PL:** Quizopasowanie | wiciędze
**EN:** Quizmatch | wiciędze

**PL:** Do poczytania | wiciędze
**EN:** To read | wiciędze

**PL:** Dwa style z zestawu głównego, jeden obok drugiego.
**EN:** Two core styles, one next to the other.

**PL:** Porównaj | wiciędze
**EN:** Compare | wiciędze

**PL:** {{ left.name_pl }} i {{ right.name_pl }}, obok siebie.
**EN:** {{ left.name_en }} and {{ right.name_en }}, side by side.

**PL:** {{ left.name_pl }} / {{ right.name_pl }} | wiciędze
**EN:** {{ left.name_en }} / {{ right.name_en }} | wiciędze

**PL:** Brak pytań | wiciędze
**EN:** No questions | wiciędze

**PL:** Nie ma takiej strony | wiciędze
**EN:** This page is not here | wiciędze

## Sekcja B — katalog-opisy.md (lustro redakcyjne, 46 stylów)



# Katalog wiciędze — opisy do sprawdzenia

Ten plik jest do dwóch przejść, w tej kolejności.

1. Najpierw model ze źródłami. Sprawdza fakty, relacje i to, czy karta jest jedną sztuką, czy workiem. Nie wygładza zdań.
2. Dopiero potem model, który porównuje polski akapit z angielskim nad nim i wygładza polski tak, żeby trzymał sens angielskiego.

Angielski jest tekstem roboczym. Polski idzie pod nim. W pliku nie ma profilu liczbowego, tagów, żartów ani adresów źródeł.

## Boxing

Nazwa PL: Boks

### About

Boxing is a fist sport fought in a ring — in gloves. In typical sporting boxing, legal punches go to set zones of the head and torso. A typical sporting boxing rulebook also has no kicks and no continuing the fight on the ground.

Boks to sport walki na pięści, rozgrywany w ringu — w rękawicach. W typowym boksie sportowym dozwolone ciosy pięścią kieruje się w określone strefy głowy i tułowia. W typowym regulaminie boksu sportowego nie ma też kopnięć ani kontynuowania walki w parterze.

### History

Modern boxing took shape in England out of earlier bare-knuckle fights. The Queensberry rules, published in 1867, standardised gloved, round-based boxing and banned wrestling. Over time that became a sport in its own right, Olympic and professional.

Współczesny boks wykształcił się w Anglii z wcześniejszych walk na gołe pięści. Reguły Queensberry, opublikowane w 1867 roku, ujednoliciły boks w rękawicach i rundach oraz zakazały zapasów. Z czasem wykształcił się z tego osobny sport, dziś zarówno olimpijski, jak i zawodowy.

### How it is fought

Training works on holding the guard, footwork, punching on pads and the bag, and sparring. Defence means slips, blocks and a short clinch that the referee breaks.

Na treningu ćwiczy się trzymanie gardy, pracę nóg, uderzenia na tarczach i worku oraz sparing. W obronie liczą się uniki, bloki i krótki klincz, który rozdziela sędzia.

### Facts

- The Queensberry rules were published in 1867. Earlier London Prize Ring Rules allowed wrestling and holding more broadly.
Reguły Queensberry zostały opublikowane w 1867 roku. Wcześniejsze London Prize Ring Rules szerzej dopuszczały zapasy i chwyty.



### Relations

Brak osobnej relacji.

## Muay Thai

Nazwa PL: Muay thai

### About

Muay Thai is Thai boxing. It is often popularly called the art of eight limbs, because it uses fists, elbows, knees and shins. In the clinch you can hold your opponent and attack with knees, and in a typical sporting bout there is no ground fighting.

Muay thai to tajski boks. Bywa popularyzatorsko nazywane sztuką ośmiu kończyn, ponieważ wykorzystuje pięści, łokcie, kolana i golenie. W klinczu można trzymać rywala i atakować kolanami, a w typowej walce sportowej nie ma parteru.

### History

The roots of Muay Thai are tied to Thai fighting traditions, military training and local contests; the earliest development is still debated. In the twentieth century a modern sporting form grew with the ring, rounds and gloves, and the ram muay ritual stayed part of the practice.

Korzenie muay thai wiążą się z tajskimi tradycjami walki, treningiem wojskowym i lokalnymi zawodami; szczegóły najdawniejszego rozwoju są przedmiotem dyskusji. W XX wieku rozwinęła się współczesna forma sportowa z ringiem, rundami i rękawicami, a rytuał ram muay pozostał częścią praktyki.

### How it is fought

Punches, kicks, knees, elbows and clinch work in which the fighter may hold and attack with knees. The ram muay is the dance before the fight, not a round. There is no ground game on the mat. Lethwei adds the head as a weapon and, in traditional formats, uses hand wraps instead of boxing gloves. Kickboxing has different rules for clinching and knees depending on the format.

Pięści, kopnięcia, kolana, łokcie oraz klincz, w którym wolno trzymać rywala i atakować kolanami. Ram muay jest tańcem przed walką, nie rundą. Na macie nie ma parteru. Lethwei dokłada głowę jako broń i, w tradycyjnych formułach, używa owijek zamiast rękawic bokserskich. Kickboxing ma różne zasady dotyczące klinczu i kolan zależnie od formuły.

### Facts

- The ram muay is the dance before a Muay Thai bout, not a round and not the fight itself.
Ram muay jest tańcem przed walką muay thai, a nie rundą i nie samą walką.



### Relations

- Z kartą Lethwei: Lethwei and Muay Thai use a similar set of limbs, but traditional lethwei adds the head and, in traditional formats, uses hand wraps instead of boxing gloves.
Lethwei i muay thai używają podobnych kończyn, ale tradycyjne lethwei dokłada głowę i, w tradycyjnych formułach, używa owijek zamiast rękawic bokserskich.
- Z kartą Kickboxing: Some kickboxing formats sit closer to Muay Thai, and some have neither this clinch nor the knees.
Część formuł kickboxingu jest bliżej muay thai, a część nie ma tego klinczu ani kolan.



## Kickboxing

Nazwa PL: Kickboxing

### About

Kickboxing is an umbrella term for several striking rulesets and training traditions, not one universal sport rulebook. Full Contact, Low Kick and K1 Style are separate ring disciplines, while Dutch kickboxing is chiefly a training and fighting style rather than one universal international ruleset. Clinch rules, knees and legal targets divide the formats.

Kickboxing to określenie obejmujące kilka formuł walki na pięści i kopnięcia oraz tradycje treningowe, a nie jeden uniwersalny regulamin. Full Contact, Low Kick i K1 Style są odrębnymi formułami ringowymi, a kickboxing holenderski jest przede wszystkim stylem walki i treningu, a nie jednym uniwersalnym regulaminem międzynarodowym. Formuły różnią się zasadami klinczu, kolan i dozwolonych celów.

### History

In the United States, full-contact kickboxing developed alongside point karate. In Japan, kickboxing developed as a distinct striking ruleset. K-1 later popularised a particular combination of punches, kicks and knees. Dutch kickboxing became a recognisable training and fighting style rather than a single international rulebook.

W Stanach Zjednoczonych full-contact kickboxing rozwijał się obok karate punktowego. W Japonii kickboxing rozwinął się jako odrębna formuła walki na uderzenia. K-1 spopularyzowało określone połączenie pięści, kopnięć i kolan. Kickboxing holenderski stał się rozpoznawalnym stylem treningu i walki, a nie jednym międzynarodowym regulaminem.

### How it is fought

Full Contact generally allows kicks above the waist and restricts the clinch. Low Kick adds legal kicks to the thighs. K1 Style permits knees and limits clinching under its rules. The details vary by organisation; these formats should not be treated as interchangeable.

Full Contact zasadniczo dopuszcza kopnięcia powyżej pasa i ogranicza klincz. Low Kick dopuszcza kopnięcia w uda. K1 Style dopuszcza kolana i ogranicza klincz zgodnie z własnym regulaminem. Szczegóły zależą od organizacji; tych formuł nie należy traktować jako wymiennych.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Mixed martial arts

Nazwa PL: MMA

### About

MMA is a sport in which one fight allows striking and ground fighting, inside a promotion's rules. There is no single school. A typical camp puts together boxing or Muay Thai, wrestling and Brazilian jiu-jitsu.

MMA to sport, w którym w jednej walce wolno uderzać i walczyć w parterze, w granicach regulaminu organizacji. Nie ma jednej szkoły. Typowy trening składa boks albo muay thai, zapasy i brazylijskie jiu-jitsu.

### History

Vale tudo in Brazil and early Japanese cards, including PRIDE, mixed styles before the name MMA stuck. The early UFC events had no standard weight classes and used a tournament format, with fewer fouls than modern MMA. Modern MMA has gloves, rounds, weight divisions and a foul list.

Vale tudo w Brazylii i wczesne gale w Japonii, w tym PRIDE, mieszały style, zanim nazwa MMA się utarła. Pierwsze edycje UFC nie miały standardowego podziału na kategorie wagowe i miały formułę turniejową, a lista fauli była krótsza niż we współczesnym MMA. Współczesne MMA ma rękawice, rundy, kategorie wagowe i listę fauli.

### How it is fought

In the gym, striking, takedown entries, control and submissions are drilled apart, then sparring puts them together. Kickboxing without takedowns, or BJJ without punches, is not yet an MMA fight, even when it supplies the tools.

Na sali osobno idą stójka, wejścia w obalenie, kontrola i poddania, a potem sparing, który to składa. Kickboxing bez obaleń albo BJJ bez ciosów nie są jeszcze walką MMA, nawet jeśli dają jej narzędzia.

### Facts

Brak osobnego faktu.

### Relations

- Z kartą Brazylijskie jiu-jitsu: In a typical MMA camp the ground game is taken from BJJ, beside wrestling and the stand-up.
W typowym treningu MMA parter bierze się z BJJ, obok zapasów i stójki.
- Z kartą Zapasy: Wrestling is one of the main sources of MMA takedowns, although fighters also use judo, sambo and other grappling systems.
Zapasy są jednym z głównych źródeł obaleń w MMA, choć zawodnicy używają też judo, sambo i innych systemów grapplingowych.
- Z kartą Muay thai: The stand-up in MMA often takes boxing or Muay Thai. A knee clinch is not yet the whole MMA fight.
Stójka w MMA często bierze boks albo muay thai. Klincz kolanem nie jest jeszcze całą walką MMA.



## Wrestling

Nazwa PL: Zapasy

### About

Olympic wrestling uses freestyle and Greco-Roman for men, while women's wrestling follows freestyle rules. Folkstyle, catch wrestling and various folk wrestling traditions belong to the broader wrestling family, but they are not the two Olympic styles.

W zapasach olimpijskich mężczyźni rywalizują w stylu wolnym i klasycznym, a zapasy kobiet stosują reguły stylu wolnego. Folkstyle, catch wrestling i różne zapasy ludowe należą do szerszej rodziny zapasów, ale nie są tymi dwoma stylami olimpijskimi.

### History

United World Wrestling runs freestyle and Greco-Roman as Olympic sports. Folkstyle is the scholastic and collegiate format in the United States, with different points for a takedown and a hold. Catch wrestling is a separate line, where a submission sits beside the throw.

United World Wrestling prowadzi styl wolny i klasyczny jako sport olimpijski. Folkstyle to szkolna i akademicka formuła w Stanach, z innymi punktami za sprowadzenie i przytrzymanie. Catch wrestling to osobna linia, w której obok rzutu jest poddanie.

### How it is fought

In freestyle the grip may go to the leg. In Greco-Roman an attack below the waist is a foul. In both styles a fall (pin) can end the bout, and technical superiority can also end it under the rules; otherwise the points decide. There are no strikes.

W stylu wolnym chwyt może zejść na nogę. W klasycznym atak poniżej pasa jest błędem. W obu stylach przytrzymanie obu barków na macie (fall/pin) może zakończyć walkę, a regulamin przewiduje także zwycięstwo przez przewagę techniczną; w pozostałych przypadkach decydują punkty. Ciosów nie ma.

### Facts

- Olympic wrestling is freestyle and Greco-Roman. Freestyle may attack the legs, Greco-Roman only the upper body.
Zapasy olimpijskie to styl wolny i klasyczny. W wolnym wolno atakować nogi, w klasycznym tylko górę ciała.



### Relations

- Z kartą Catch wrestling: Catch adds submissions. Freestyle and Greco-Roman use points, falls and technical superiority under their rules.
Catch dokłada poddania. Styl wolny i klasyczny mają punkty, przytrzymanie obu barków na macie oraz zwycięstwo przez przewagę techniczną zgodnie ze swoimi regulaminami.



## Judo

Nazwa PL: Judo

### About

Judo is a Japanese art fought in a judogi. In sporting judo a win can come from a throw, a hold-down or a legal submission, depending on the rules. There are no strikes in a typical sporting bout.

Judo to japońska sztuka walki w judogi. W sportowym judo zwycięstwo może przynieść między innymi rzut, unieruchomienie albo dozwolone poddanie, zależnie od regulaminu. Uderzeń nie ma w typowej walce sportowej.

### History

Jigoro Kano arranged judo at the end of the nineteenth century out of older jujutsu schools, among other things with education in mind. Later competitive sport narrowed some of what is legal in contest.

Jigoro Kano ułożył judo pod koniec XIX wieku na bazie starszych szkół jujutsu, między innymi z myślą o edukacji i wychowaniu. Późniejszy sport wyczynowy zawęził część tego, co wolno na zawodach.

### How it is fought

You grip the opponent's judogi, break their balance and throw. On the ground you can hold them or look for a submission the rules allow.

Chwytasz judogi przeciwnika, wytrącasz go z równowagi i rzucasz. Na ziemi możesz go unieruchomić albo szukać poddania dopuszczonego przez regulamin.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Brazilian jiu-jitsu

Nazwa PL: Brazylijskie jiu-jitsu

### About

Brazilian jiu-jitsu (BJJ) looks for a submission by a joint lock or a choke. Most of the work is on the ground, and sporting gi and no-gi usually have no strikes.

Brazylijskie jiu-jitsu (BJJ) szuka poddania rywala przez dźwignię albo duszenie. Większość pracy odbywa się w parterze, a w sportowym gi i no-gi uderzeń zwykle nie ma.

### History

Some accounts tie the start to the judo and jujutsu Mitsuyo Maeda brought to Brazil, and to later Gracie work on the ground. That isn't one undisputed origin, and today's BJJ contests are not judo. Details of family stories are sometimes later tradition.

Część opracowań wiąże początki z judo i jujutsu, które do Brazylii przywiózł Mitsuyo Maeda, oraz z późniejszą pracą rodziny Gracie nad parterem. Nie jest to jeden bezsporny rodowód, a dzisiejsze zawody BJJ to nie judo. Szczegóły rodzinnych opowieści bywają późniejszą tradycją.

### How it is fought

You pass the guard, take the back or mount, and look for a lock or a choke. Sparring is built around continuous work with a partner.

Przechodzisz gardę, bierzesz plecy albo wchodzisz w dosiad i szukasz dźwigni lub duszenia. Sparingi opierają się na ciągłej pracy z partnerem.

### Facts

Brak osobnego faktu.

### Relations

- Z kartą Judo: Some accounts tie the start of BJJ to the judo and jujutsu Maeda practiced. That isn't one undisputed origin, and today's BJJ contests are not judo.
Część opracowań wiąże początki BJJ z judo i jujutsu, które ćwiczył Maeda. To nie jest jeden bezsporny rodowód, a dzisiejsze zawody BJJ to nie judo.
- Z kartą Luta livre esportiva: Luta livre esportiva is Brazilian grappling without the gi, historically beside BJJ, not its no-gi rule.
Luta livre esportiva to brazylijski grappling bez kimona, historycznie obok BJJ, a nie jego reguła no-gi.



## Karate

Nazwa PL: Karate

### About

Karate is a family of striking arts rooted in Okinawa and later developed in Japan, not one rule set. WKF scores controlled kumite, including punches to the head, while knockdown formats such as Kyokushin leave the head for kicks. Kyokushin is a karate style, not an art beside karate.

Karate to rodzina sztuk uderzeń wywodzących się z Okinawy i rozwiniętych następnie w Japonii, a nie jeden regulamin. WKF punktuje kontrolowane kumite, w tym ciosy w głowę, a formuły knockdown, jak kyokushin, nie dopuszczają ciosów ręką na głowę, pozostawiając kopnięcia na głowę. Kyokushin jest stylem karate, nie sztuką obok karate.

### History

In Okinawa karate grew out of local striking arts, then entered Japan in the twentieth century and split into schools. Shotokan, Goju-ryu, Shito-ryu and Wado-ryu are four large currents that the WKF treats as separate styles, not one bag of techniques.

Na Okinawie karate wyrosło z lokalnych sztuk uderzeń, a w XX wieku weszło do Japonii i rozeszło się na szkoły. Shotokan, goju-ryu, shito-ryu i wado-ryu to cztery duże nurty, które WKF traktuje jako osobne style, nie jako jeden worek technik.

### How it is fought

Shared training is kihon, kata and kumite, but sparring depends on the school. In WKF kumite the score is a controlled hit, including a punch to the head. In knockdown the contact is fuller and hand strikes to the head drop out. Kata stays a solo or group form, not a fight.

Wspólny trening to kihon, kata i kumite, ale sparing zależy od szkoły. W kumite WKF liczą się kontrolowane trafienia, także pięścią w głowę. W knockdownzie kontakt jest pełniejszy, a ciosy ręką w głowę odpadają. Kata zostaje formą solo albo w grupie, nie walką.

### Facts

- The WKF scores controlled kumite, including punches to the head. A knockdown format, as in Kyokushin, leaves the head for kicks. That is not one karate rulebook.
WKF punktuje kontrolowane kumite, w tym ciosy w głowę. Formuła knockdown, jak w kyokushin, zostawia głowę dla kopnięć. To nie jest jeden regulamin karate.



### Relations

Brak osobnej relacji.

## Taekwondo

Nazwa PL: Taekwondo

### About

Taekwondo is a Korean martial art with a strong emphasis on kicks, but WT and ITF are not the same sport. World Taekwondo kyorugi is fought with approved protective equipment and electronic scoring. ITF uses its own patterns and sparring rules. Taekkyeon is a separate, older tradition.

Taekwondo to koreańska sztuka walki z mocnym naciskiem na kopnięcia, ale WT i ITF nie są tym samym sportem. W kyorugi World Taekwondo zawodnicy walczą w zatwierdzonych ochraniaczach i z elektronicznym systemem punktowania. ITF ma własne układy i regulamin sparingu. Taekkyeon to osobna, starsza tradycja.

### History

After the Korean War several schools came together under the name taekwondo. The ITF was founded in 1966, while the federation now known as World Taekwondo was founded in 1973. They developed distinct competition rules and training frameworks. Hapkido is sometimes taught next door, but it is a different art, with grips and locks.

Po wojnie koreańskiej kilka szkół zeszło się pod nazwą taekwondo. ITF powstała w 1966 roku, a federacja znana dziś jako World Taekwondo w 1973 roku. Z czasem rozwinęły odrębne regulaminy zawodów i odmienne ramy treningu. Hapkido bywa nauczane obok, ale to inna sztuka, z chwytami i dźwigniami.

### How it is fought

In WT the fight goes through a chest guard and foot protectors, and a kick to the head scores higher than a punch. ITF keeps patterns, the sine-wave movement and sparring in which the hands have a larger role. Forms are tul or poomsae, depending on the federation, and they are not the fight.

W WT zawodnicy walczą w kamizelce i nagolennikach, a punkt za kopnięcie w głowę jest wyższy niż za cios pięścią. W ITF zostają wzorce, układ sine wave i sparing, w którym ręce mają większą rolę. Formy to tul albo poomsae, zależnie od federacji, i nie są walką.

### Facts

- World Taekwondo and the ITF do not use the same rules. WT kyorugi is fought with body armour and electronic scoring, while ITF uses its own patterns and sparring rules.
World Taekwondo i ITF nie stosują tego samego regulaminu. W kyorugi WT zawodnicy walczą w ochraniaczach i z elektronicznym systemem punktowania, a ITF ma własne układy i regulamin sparingu.



### Relations

- Z kartą Hapkido: Hapkido is sometimes taught beside taekwondo, but the axis is the grip and the lock, not the kick to a chest guard.
Hapkido bywa nauczane obok taekwondo, ale osią są chwyt i dźwignia, nie kopnięcie na kamizelkę.
- Z kartą Taekkyeon: Taekkyeon is a separate tradition inscribed by UNESCO, not the World Taekwondo rulebook.
Taekkyeon to osobna tradycja wpisana przez UNESCO, nie regulamin World Taekwondo.



## Sumo

Nazwa PL: Sumo

### About

Sumo is decided in a ring: you push the opponent out, or make them touch the ground with anything but the sole of the foot. Open-hand strikes are among the legal techniques, but there is no ground fighting.

Sumo rozstrzyga się w kole: trzeba wypchnąć rywala albo sprawić, by dotknął ziemi czymś innym niż podeszwa stopy. Uderzenia otwartą dłonią należą do dozwolonych technik, ale walki w parterze nie ma.

### History

Sumo has a long history in Japan as ritual and spectacle, and the professional organisation and the ranking came later. The pre-bout ritual is part of the practice, not a decoration added along the way.

Sumo ma w Japonii długą historię jako rytuał i widowisko, a zawodowa organizacja i ranking powstały później. Rytuał przed walką jest częścią praktyki, a nie ozdobą dorzuconą po drodze.

### How it is fought

A low stance, the charge, a grip on the mawashi, and an attempt to push out or throw. Training is heavy and leans hard on work with a partner.

Niska pozycja, zderzenie, chwyt za mawashi i próba wypchnięcia albo rzutu. Trening jest ciężki i mocno opiera się na pracy z partnerem.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Sambo

Nazwa PL: Sambo

### About

Sambo is a Soviet-origin combat-sport family with separate sport and combat formats. Sport sambo centres on throws, holds and legal locks, with no strikes. Combat sambo adds striking to throws, holds, locks and ground fighting. It is not judo and it is not Olympic wrestling.

Sambo to rodzina sportów walki wywodzących się z tradycji radzieckiej, z odrębnymi formułami sportową i bojową. Sportowe sambo skupia się na rzutach, trzymaniach i dozwolonych dźwigniach, bez uderzeń. Combat sambo dokłada uderzenia do rzutów, trzymań, dźwigni i walki w parterze. To nie jest judo i nie jest tożsame z zapasami olimpijskimi.

### History

In the USSR, material from folk wrestling, judo and other grappling systems was combined into a single system. FIAS now runs sport and combat sambo as separate formats. The sambo jacket is a gripping tool, as in judo, but the legal techniques differ: sport sambo allows leg locks and forbids chokes under its rules.

W ZSRR materiał z zapasów ludowych, judo i innych systemów chwytów połączono w jeden system. FIAS prowadzi dziś sportowe i bojowe sambo jako odrębne formuły. Kurtka sambowa jest narzędziem chwytu, podobnie jak w judo, ale techniki dozwolone przez regulamin są inne: sportowe sambo dopuszcza dźwignie na nogi i nie dopuszcza duszeń.

### How it is fought

In sport sambo you fight in a jacket: throws, holds and locks. Combat sambo adds strikes standing and on the ground, still in the jacket, under its own rules. These formats are related but are not the same fight.

W sportowym sambo walczy się w kurtce: rzuty, trzymania i dźwignie. Combat sambo dokłada uderzenia w stójce i w parterze, nadal w kurtce, według własnego regulaminu. Te formuły są ze sobą powiązane, ale nie są tą samą walką.

### Facts

Brak osobnego faktu.

### Relations

- Z kartą Judo: Sport sambo shares the jacket grip and throws with judo, but its rules allow leg locks and differ in other techniques and scoring.
Sportowe sambo dzieli z judo chwyt za kurtkę i rzuty, ale ma inne przepisy, m.in. dotyczące dźwigni na nogi i punktowania.
- Z kartą Zapasy: Sambo includes throws and grappling, but uses its own jacket and rules.
Sambo obejmuje rzuty i grappling, ale ma własną kurtkę i własny regulamin.
- Z kartą MMA: Combat sambo includes striking and ground fighting, but remains a distinct ruleset with a jacket and its own technique list.
Combat sambo obejmuje uderzenia i walkę w parterze, ale pozostaje odrębnym regulaminem z kurtką i własnym katalogiem technik.



## Wushu / kung fu

Nazwa PL: Wushu / kung fu

### About

Wushu is a broad label for Chinese martial arts, while sport wushu under IWUF is a modern competition framework with taolu and sanda. Traditional styles and schools sit alongside that sport framework. Sanda, Wing Chun and Taijiquan are related but are not synonyms for all wushu.

Wushu to szerokie określenie chińskich sztuk walki, podczas gdy sportowe wushu w ramach IWUF jest współczesną strukturą zawodniczą obejmującą taolu i sanda. Tradycyjne style i szkoły istnieją obok tej sportowej struktury. Sanda, wing chun i taijiquan są z nią powiązane, ale nie są synonimami całego wushu.

### History

One label covers southern and northern schools, among them Hung Gar, Choy Li Fut, Bajiquan and Xingyiquan. In the twentieth century the state organised part of that material as sport wushu: taolu forms and sanda fighting. A traditional school does not become sanda because of that.

Pod jedną etykietą mieszczą się szkoły południowe i północne, między innymi hung gar, choy li fut, bajiquan i xingyiquan. W XX wieku państwo uporządkowało część tego materiału jako wushu sportowe: formy taolu i walkę sanda. Tradycyjna szkoła nie staje się przez to sandą.

### How it is fought

Taolu is a routine with or without a weapon, judged as a form. A traditional school adds paired applications and its own weapons. Sanda is a separate fight on a platform. Taijiquan has its own card here, because forms, push-hands and the sport version are already a different set.

Taolu to układ z bronią albo bez, oceniany jak forma. W tradycyjnej szkole dochodzą zastosowania w parze i własna broń. Sanda jest osobną walką na platformie. Taijiquan ma tu własną kartę, bo formy, pchnięcia rąk i sport to już inny zestaw.

### Facts

Brak osobnego faktu.

### Relations

- Z kartą Wing Chun: Wing chun is one school in the kung fu family, not an IWUF taolu routine and not sanda.
Wing chun jest jedną ze szkół w rodzinie kung fu, nie formą taolu IWUF i nie sandą.
- Z kartą Taijiquan: Taijiquan has its own schools, forms and push-hands. It is not a synonym for all of wushu.
Taijiquan ma własne szkoły, formy i pchnięcia rąk. Nie jest synonimem całego wushu.



## Sanda

Nazwa PL: Sanda

### About

Sanda is a modern Chinese combat sport associated with sport wushu, usually contested on a raised platform and combining punches, kicks and throws. It is not the name of Hung Gar or Wing Chun. It shares throws with shuai jiao, but adds strikes and a different fighting surface.

Sanda to współczesny chiński sport walki związany ze sportowym wushu, zwykle rozgrywany na podwyższonej platformie i łączący pięści, kopnięcia oraz rzuty. Nie jest nazwą hung gar ani wing chun. Z shuai jiao łączy ją stosowanie rzutów, ale sanda dokłada uderzenia i inną płaszczyznę walki.

### History

In the twentieth century sanda grew up beside wushu as sparring, then as an IWUF discipline. The platform and the throw off it are part of the rule. This is not a Muay Thai ring: the knee clinch is not the axis, and forcing someone off the platform can end the action.

W XX wieku sanda urosła przy wushu jako sparring, a potem jako dyscyplina IWUF. Platforma i rzut z niej są częścią przepisu. To nie jest ring muay thai: klincz kolanami nie jest tu osią, a zepchnięcie z platformy może kończyć akcję.

### How it is fought

You stand on a raised platform, you strike and you look for a throw. There is no continuing ground fighting after a throw; the action ends under the sanda rules. A full Muay Thai clinch, with knees to the head, is not a description of a sanda exchange. Shuai jiao stays with the jacket grip, without this set of strikes.

Stoisz na podwyższeniu, uderzasz i szukasz rzutu. Parter nie jest kontynuowany po rzucie; akcja kończy się zgodnie z regulaminem sanda. Pełny klincz muay thai, z kolanami przy głowie, nie jest opisem sandowej wymiany. Shuai jiao zostaje przy chwycie za kurtkę, bez tego zestawu ciosów.

### Facts

Brak osobnego faktu.

### Relations

- Z kartą Wushu / kung fu: Sanda is a contemporary sport tied to wushu, not a substyle equal to every traditional kung fu form.
Sanda to współczesny sport związany z wushu, a nie podstyl równy wszystkim tradycyjnym formom kung fu.
- Z kartą Shuai Jiao: Sanda adds strikes and a platform to the throw. Shuai jiao stays with the jacket, without that set of strikes.
Sanda dokłada do rzutu uderzenia i platformę. Shuai jiao zostaje przy kurtce, bez tego zestawu ciosów.



## Aikido

Nazwa PL: Aikido

### About

Aikido practises getting off the line, throws and locks, usually with a partner who offers a grip. In most of the main organisations tournament fighting is not the centre of training, though there are forms with contests or randori. Training weapons include the jo and the bokken.

Aikido ćwiczy zejście z linii, rzuty i dźwignie, zwykle z partnerem, który podaje uchwyt. W większości głównych organizacji rywalizacja turniejowa nie jest centrum treningu, choć istnieją odmiany z zawodami lub randori. Broń treningowa to między innymi jo i bokken.

### History

Morihei Ueshiba developed aikido in the twentieth century out of arts he himself trained, including Daito-ryu. Later organisations differ on pace, weapons and whether they spar at all, so one hall doesn't stand for all of them.

Morihei Ueshiba rozwijał aikido w XX wieku na bazie sztuk, które sam ćwiczył, w tym Daito-ryu. Późniejsze organizacje różnią się tempem, podejściem do broni i tym, czy w ogóle sparingują, więc jedna sala nie reprezentuje wszystkich.

### How it is fought

You practise paired forms, falling and work with a wooden weapon. Contact is often set in advance, and in many schools it is not sparring for a score.

Ćwiczy się formy w parach, upadki i pracę z bronią drewnianą. Kontakt bywa z góry ustalony, a w wielu szkołach nie jest to sparing na wynik.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Krav Maga

Nazwa PL: Krav maga

### About

Krav maga is the name used by several self-defence programmes, not one federation. Organisations and instructors associated with military or law-enforcement training teach different syllabuses under the same label. What they share is the job: a plain response to an attack, with no sporting score.

Krav maga to nazwa używana przez kilka programów samoobrony, nie jednej federacji. Organizacje i instruktorzy związani ze szkoleniem wojskowym lub policyjnym uczą pod tym samym szyldem różnych sylabusów. Wspólne jest zadanie: prosta reakcja na atak, bez sportowego punktowania.

### History

Imi Lichtenfeld put the system together in the mid twentieth century, first around real fights, then around training. Later the organisations split, and each one keeps its own programme. There is no single world rulebook to quote here the way there is for boxing.

Imi Lichtenfeld ułożył system w połowie XX wieku, najpierw przy realnych bójkach, potem przy szkoleniu. Później organizacje rozeszły się i każda trzyma własny program. Nie ma jednego światowego regulaminu, który dałoby się tu zacytować jak w boksie.

### How it is fought

Training goes through scenarios: a strike, a grab, a knife or a stick, and a way out. A points spar is usually absent. The differences between IKMF, KMG and military programmes show up in what the course includes, not in the name on the door.

Trening idzie przez scenariusze: cios, chwyt, zagrożenie nożem albo kijem, i wyjście z tego. Sparingu sportowego na punkty zwykle nie ma. Różnice między IKMF, KMG i programami wojskowymi widać w tym, co wchodzi do kursu, nie w nazwie na drzwiach.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Hapkido

Nazwa PL: Hapkido

### About

Hapkido is a Korean art of locks, throws and kicks. What separates it from taekwondo is the aim: in hapkido the grip and the lock are the base, not a pause in a kicking match. School lines differ in how much striking they keep and how much grappling.

Hapkido to koreańska sztuka dźwigni, rzutów i kopnięć. Od taekwondo dzieli je cel: w hapkido chwyt i dźwignia są podstawą, a nie przerwą w walce na kopnięcia. Linie szkół różnią się tym, ile zostawiają uderzeń, a ile chwytów.

### History

Modern hapkido grew in Korea in the twentieth century. Organisations differ in the lineage, so this card does not name one master as the only source. Taekwondo has sport federations and protective equipment. Hapkido more often stays with paired techniques and self-defence.

Współczesne hapkido rozwinęło się w Korei w XX wieku. Organizacje różnią się w rodowodzie, więc ta karta nie wskazuje jednego mistrza jako jedynego źródła. Taekwondo ma federacje sportowe i ochraniacze. Hapkido częściej pozostaje przy technikach wykonywanych w parach i samoobronie.

### How it is fought

A typical pair is a wrist or sleeve grip, a lock and a throw, plus kicks from a distance. There is no WT chest guard and no ITF scoring. Training depends on the line: some add weapons, others stay with the empty hand.

Typowa technika w parach to chwyt nadgarstka albo rękawa, dźwignia i rzut, plus kopnięcia z dystansu. Nie ma tu kamizelki WT ani punktowania ITF. Trening zależy od linii: jedne dokładają broń, inne zostają przy pustej ręce.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Savate

Nazwa PL: Savate

### About

Savate is French boxing with the foot and the fist, in shoes. Canne de combat, a stick sport, sits beside it in the federation, not as a round of savate. The shoe and the kick change the hip compared with barefoot kickboxing.

Savate to francuski boks nogą i pięścią, w butach. Osobno istnieje canne de combat, sport na lasce, który federacja trzyma obok, a nie jako rundę savate. But i kopnięcie zmieniają biodro względem kickboxingu bez obuwia.

### History

In the nineteenth century Parisian street boxing combined with English boxing into the sport that the French federation runs today. Canne and bâton are separate work with a cane and a staff, under a shared institution, not in a shared fight.

W XIX wieku paryski boks uliczny złożył się z angielskim boksem w sport, który dziś prowadzi francuska federacja. Canne i bâton to osobna praca laską i kijem, ze wspólną instytucją, nie z wspólną walką.

### How it is fought

In savate you kick with the toe, the sole and the instep, in shoes, and the fists stay boxing fists. Assaut and combat differ in how much contact is allowed. Canne is judged as an exchange of canes in a mask, not as kicks.

W savate kopie się czubkiem, podeszwą i podbiciem, w butach, a pięści zostają bokserskie. Formy assaut i combat różnią się dopuszczonym kontaktem. Canne ocenia się jako wymianę lasek w masce, nie jako kopnięcia.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Capoeira

Nazwa PL: Capoeira

### About

Capoeira is an Afro-Brazilian game joining movement, kicks, evasions and music in the circle, the roda. Depending on the group it can lean more on play, acrobatics, tradition or sparring, but it is not simply kickboxing.

Capoeira to afrobrazylijska gra i sztuka walki, która łączy ruch, kopnięcia, uniki i muzykę w kręgu zwanym roda. W zależności od grupy może być bardziej zabawą, akrobatyką, praktyką tradycyjną albo sparingiem, ale nie jest po prostu kickboxingiem.

### History

It took shape in Brazil among enslaved Africans and their descendants. For part of the nineteenth and twentieth centuries it was outlawed, then it entered schools. Sources differ on the details of its beginnings.

Kształtowała się w Brazylii wśród zniewolonych Afrykanów i ich potomków. W części XIX i XX wieku była zakazana lub prześladowana, a później rozwijała się w szkołach i akademiach. Źródła różnią się w szczegółach jej początków.

### How it is fought

The ginga is the base, and the kicks, evasions and transitions come out of it. Music and rhythm are part of the practice, not just background.

Bazą capoeiry jest ginga — płynny ruch, z którego wyprowadza się kopnięcia, uniki i przejścia. Muzyka i rytm są integralną częścią praktyki, nie tylko tłem.

### Facts

- UNESCO inscribed the Capoeira Circle in 2014 as intangible cultural heritage.
UNESCO wpisało krąg capoeiry na reprezentatywną listę niematerialnego dziedzictwa kulturowego w 2014 roku.



### Relations

Brak osobnej relacji.

## Kendo

Nazwa PL: Kendo

### About

Kendo is Japanese fencing with a shinai, in bogu armour, scored on points. Iaido and kenjutsu sit beside it, not inside that scoring: iaido is sword forms, kenjutsu is the older sword schools.

Kendo to japońska szermierka na shinai, w zbroi bogu, rozgrywana na punkty. Iaido i kenjutsu są obok, nie wewnątrz tego punktowania: iaido to formy z mieczem, kenjutsu to starsze szkoły miecza.

### History

In the twentieth century kendo arranged material from kenjutsu schools into a sport with a Japanese federation and grade exams. Iaido went another way: drawing the sword and kata, with no shinai fight. Kenjutsu is not a kendo division.

Kendo ułożyło w XX wieku materiał ze szkół kenjutsu w sport z japońskim związkiem i egzaminami na stopnie. Iaido poszło w inną stronę: wyciągnięcie miecza i kata, bez walki na shinai. Kenjutsu nie jest kategorią kendo.

### How it is fought

In kendo a valid hit to a target, with a shout and good posture, scores on the shinai. Iaido is practised as a catalogue of forms, often with a training sword, and there is no point for a strike to the men. Kenjutsu stays with the school and its pairs, not with a kendo tournament.

W kendo liczy się poprawne trafienie w dozwoloną strefę, z krzykiem i z dobrą postawą, na shinai. Iaido ćwiczy się katalogiem form, często na mieczu treningowym, bez punktu za cios w men. Kenjutsu zostaje przy szkole i jej parach, nie przy turnieju kendo.

### Facts

Brak osobnego faktu.

### Relations

- Z kartą Iaido: Kendo scores a shinai hit in armour. Iaido practises drawing the sword in forms and is not a kendo division.
Kendo punktuje trafienie shinai w zbroi. Iaido ćwiczy dobywanie miecza w formach i nie jest kategorią kendo.



## Sport fencing

Nazwa PL: Szermierka sportowa

### About

Sport fencing covers foil, epee and sabre, and electrical kit records the touches. Distance, timing and a hit under that weapon's rules are what count. Foil and sabre use right of way; epee has different rules.

Szermierka sportowa obejmuje trzy konkurencje: floret, szpadę i szablę. Trafienia są rejestrowane przez elektroniczną aparaturę. Kluczowe znaczenie mają dystans, timing i przestrzeganie zasad danej broni. Floret i szabla mają zasadę pierwszeństwa, a szpada podlega innym zasadom.

### History

It grew out of the European bladed-weapon tradition and the nineteenth-century salle. The mask, protective kit and electrical judging helped turn it into a modern Olympic sport.

Szermierka sportowa wywodzi się z europejskiej tradycji broni białej i XIX-wiecznych sal szermierczych. Wprowadzenie maski, sprzętu ochronnego i elektronicznego sędziowania pozwoliło przekształcić ją w nowoczesny sport olimpijski.

### How it is fought

A lesson with a coach, footwork, the lunge and sparring on the piste.

Trening obejmuje lekcje z trenerem, pracę nóg, wypad i sparing na planszy.

### Facts

- Sport fencing records a touch with electrical kit. HEMA tries to reconstruct techniques described in old treatises. They are two different practices.
W szermierce sportowej trafienie rejestruje aparatura elektryczna. HEMA próbuje odtworzyć techniki opisane w dawnych traktatach. To dwie różne praktyki.



### Relations

Brak osobnej relacji.

## HEMA

Nazwa PL: HEMA (Historical European Martial Arts)

### About

HEMA is a modern attempt to reconstruct European weapon arts from treatises: the longsword, the rapier, the sidesword, the dussack and others. It is not Olympic fencing and it is not Japanese kenjutsu.

HEMA to współczesna próba odtworzenia europejskich sztuk broni z traktatów: miecz długi, rapier, miecz boczny, dussack i inne. To nie jest szermierka olimpijska i nie jest japońskie kenjutsu.

### History

The treatises are historical, and the clubs and tournaments that train from them today are mostly from the late twentieth century. Readings of the same source are sometimes disputed. Kenjutsu is a neighbouring Japanese sword practice, from its own schools, not a branch of HEMA.

Traktaty są historyczne, a kluby i turnieje, które dziś z nich trenują, są w większości z końca XX wieku. Czytanie tego samego źródła bywa sporne. Kenjutsu to sąsiednia, japońska praktyka miecza, z własnych szkół, nie dział HEMA.

### How it is fought

You drill sets from a treatise, pairs and sparring with blunt weapons in protection matched to the weapon. Sport fencing has foil, épée and sabre, with electrical scoring. Here historical sources and tournament rules determine how techniques and hits are interpreted; there is no single HEMA scoring system.

Ćwiczy się zestawy z traktatu, pary i sparing na broni tępej w ochraniaczach dobranych do broni. Szermierka sportowa ma floret, szpadę i szablę oraz elektroniczne sędziowanie trafień. Tutaj sposób interpretacji technik i trafień zależy od źródeł historycznych oraz regulaminu turnieju; nie ma jednego systemu punktowania HEMA.

### Facts

- Sport fencing records a touch with electrical kit. HEMA tries to reconstruct techniques described in old treatises. They are two different practices.
W szermierce sportowej trafienie rejestruje aparatura elektryczna. HEMA próbuje odtworzyć techniki opisane w dawnych traktatach. To dwie różne praktyki.



### Relations

- Z kartą Szermierka sportowa: Both practices work with European bladed weapons, but HEMA reconstructs techniques from historical treatises, while sport fencing has three weapons and its own rules. It is not the same training.
Szermierka sportowa i HEMA to dwie różne praktyki: w szermierce trafienia rejestruje aparatura, a HEMA odtwarza historyczne techniki z traktatów.



## Arnis / kali / eskrima

Nazwa PL: Arnis / Kali / Eskrima

### About

Arnis, kali and eskrima are Philippine arts with stick, knife and empty hand. The names depend on the region and the school, not on three different sports. Sport formats for the stick sit beside the tradition.

Arnis, kali i eskrima to filipińskie sztuki z kijem, nożem i pustą ręką. Nazwy zależą od regionu i szkoły, nie od trzech różnych sportów. Obok tradycji są też formuły sportowe na kij.

### History

The short weapon is the axis, and the empty hand comes in as a continuation of the same angles. Known currents include Modern Arnis, Doce Pares and Balintawak. Each one arranges the stick, the knife and the entry to empty-hand range differently. In 2009, the Philippines declared arnis the national martial art and sport through Republic Act No. 9850.

Broń krótka jest osią, a pusta ręka dochodzi jako kontynuacja tych samych kątów. Znane nurty to między innymi Modern Arnis, Doce Pares i Balintawak. Każdy układa inaczej kij, nóż i wejście na dystans ręki. W 2009 roku Filipiny uznały arnis za narodową sztukę walki i sport na mocy Republic Act No. 9850.

### How it is fought

Training starts with sticks: angles, a block and a counter. Then the knife, two weapons or the empty hand. In sport the usual tools are a stick and protection. A traditional school does not end at points for hitting with a foam stick.

Trening zaczyna się od kijów: kąty, blok i kontra. Potem nóż, dwie bronie albo pusta ręka. W sporcie liczy się zwykle kij i ochraniacze. Szkoła tradycyjna nie kończy się na punktach za trafienie piankowym kijem.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Silat

Nazwa PL: Silat

### About

Pencak silat is a family of arts from Indonesia, Malaysia and nearby regions, not one rule set. There are regional traditions and weapons, and in PERSILAT competition the main categories are tanding and jurus, with jurus including tunggal, ganda and regu.

Pencak silat to rodzina sztuk z Indonezji, Malezji i pobliskich regionów, nie jeden regulamin. Są nurty regionalne i broń, a w zawodach PERSILAT główne kategorie to tanding i jurus, przy czym jurus obejmuje tunggal, ganda i regu.

### History

The name gathers island and court styles, empty hand and weapons. In 2019 UNESCO inscribed the traditions of pencak silat as heritage, not as a tournament rulebook. PERSILAT and national federations hold the sporting rules.

Nazwa zbiera style wysp i dworów, z pustą ręką i z bronią. UNESCO w 2019 roku wpisało tradycje pencak silat jako dziedzictwo, a nie regulamin turnieju. Zasady walki sportowej trzyma PERSILAT i federacje krajowe.

### How it is fought

Jurus refers to forms or movement sequences in the practice and is also a competition category under the PERSILAT rules. The jurus categories include tunggal, ganda and regu; tanding is the combat category. A school's training can also include weapons. Forms are not the match.

Jurus oznacza formy lub sekwencje ruchów w praktyce i jest także kategorią zawodów według regulaminu PERSILAT. Kategorie jurus obejmują tunggal, ganda i regu, a tanding jest kategorią walki. Trening szkoły może też obejmować broń. Formy nie są walką.

### Facts

- In the 2026 PERSILAT competition regulations, the main competition categories are Tanding and Jurus; Jurus includes Tunggal, Ganda and Regu.
W regulaminie zawodów PERSILAT z 2026 roku główne kategorie to Tanding i Jurus; Jurus obejmuje Tunggal, Ganda i Regu.



### Relations

Brak osobnej relacji.

## Lethwei

Nazwa PL: Lethwei

### About

Lethwei is Burmese boxing: fists, legs, knees, elbows and, in traditional formats, the head. Traditional formats use hand wraps rather than boxing gloves; modern Lethwei events can use different rules and equipment. It is not Muay Thai, even with a similar set of limbs.

Lethwei to birmański boks: pięści, nogi, kolana, łokcie i, w tradycyjnych formułach, głowa. Tradycyjne formuły używają owijek zamiast rękawic bokserskich; współczesne gale lethwei mogą stosować inne regulaminy i wyposażenie. To nie jest muay thai, mimo podobnego zestawu kończyn.

### History

Local fights are older than today's cards. Modern federations have tightened rounds and kit, but traditional formats use hand wraps rather than boxing gloves; modern Lethwei events can use different rules and equipment. Looking like Muay Thai did not make the rules the same.

Lokalne walki są starsze niż dzisiejsze gale. Współczesne federacje doprecyzowały rundy i sprzęt, ale tradycyjne formuły używają owijek zamiast rękawic bokserskich; współczesne gale lethwei mogą stosować inne regulaminy i wyposażenie. Podobieństwo do muay thai nie zrównało przepisów.

### How it is fought

The exchange is hard and stays standing. The head comes in as a strike when the rules do not switch it off. The lack of a thick glove changes the fist compared with Muay Thai and K-1. There is no ground game.

Wymiana jest twarda i stoi. Głowa wchodzi jako uderzenie, gdy regulamin jej nie wyłączy. Brak grubej rękawicy zmienia pięść względem muay thai i K-1. Parteru tu nie ma.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Kyokushin karate

Nazwa PL: Kyokushin

### About

Kyokushin is a full-contact karate style. In classic and many modern knockdown formats punches to the head are illegal and kicks to the head are allowed. The details still depend on the organisation and the rules.

Kyokushin to pełnokontaktowy styl karate. W klasycznych i wielu współczesnych formułach knockdown ciosy pięścią na głowę są zazwyczaj zakazane, a kopnięcia na głowę dozwolone. Szczegóły zależą od organizacji i regulaminu.

### History

Masutatsu Oyama founded Kyokushin in the mid twentieth century as a hard form of karate, and organisations began to split after his death. Kyokushin remains a form of karate, not a tradition from outside karate.

Masutatsu Oyama założył kyokushin w połowie XX wieku jako twardą odmianę karate. Kyokushin pozostaje odmianą karate, a nie osobną tradycją spoza karate.

### How it is fought

You practise kihon, kata and kumite with contact. Conditioning and sparring are the axis, not the form alone.

Trening kyokushin obejmuje kihon (ćwiczenia podstaw), kata (formy) oraz kumite (sparing z kontaktem). Nacisk kładzie się na kondycję i sparing, a nie tylko na formę.

### Facts

- The WKF scores controlled kumite, including punches to the head. A knockdown format, as in Kyokushin, leaves the head for kicks. That is not one karate rulebook.
WKF punktuje kontrolowane kumite, w tym ciosy w głowę. Formuła knockdown, jak w kyokushin, zostawia głowę dla kopnięć. To nie jest jeden regulamin karate.
- In the KWU knockdown rules, hand and elbow strikes to the face are forbidden. The KWU also runs separate full-contact formats in which punches to the head are allowed. The ban is not a rule of all karate.
W regulaminie knockdown KWU ciosy ręką i łokciem w twarz są zabronione. KWU prowadzi też osobne formuły full contact, w których ciosy w głowę wchodzą. Zakaz nie jest więc regułą całego karate.



### Relations

- Z kartą Karate: Kyokushin is a full-contact style of karate, not a tradition from outside karate.
Kyokushin to pełnokontaktowa odmiana karate, a nie osobna tradycja spoza karate.



## Wing Chun

Nazwa PL: Wing Chun

### About

Wing Chun is a southern Chinese short-range art: structure, straight strikes and chi sao, the sticking hands. The story of a founding woman, Yim Wing-chun, belongs to school tradition, not to a documented biography.

Wing Chun to południowochińska sztuka walki krótkiego dystansu, charakteryzująca się prostymi uderzeniami i ćwiczeniem chi sao („klejące ręce”). Opowieść o założycielce, Yim Wing-chun, należy do tradycji szkoły, a nie do udokumentowanej historii.

### History

The practice is tied to southern China and to twentieth-century teaching, including the Ip Man line. The legend of Ng Mui and Yim Wing-chun belongs to the school's later tradition, and that's how I mark it.

Praktyka wiąże się z południowymi Chinami i XX-wiecznym nauczaniem, w tym linią Ip Mana. Legenda o Ng Mui i Yim Wing-chun należy do późniejszej tradycji szkoły i tak ją tutaj oznaczam.

### How it is fought

You practise forms on the wooden dummy, chi sao and close strikes. Sparring depends on the hall.

Trening obejmuje ćwiczenie form na drewnianym manekinie, chi sao oraz uderzeń z bliska. Sparing może występować, ale zależy to od konkretnej szkoły lub instruktora.

### Facts

- The story of Ng Mui and Yim Wing-chun belongs to Wing Chun school tradition, not to documented history you can use to pin down an exact founding date.
Opowieść o Ng Mui i Yim Wing-chun należy do tradycji szkoły wing chun, a nie do udokumentowanej historii, na której można oprzeć dokładną datę powstania stylu.



### Relations

Brak osobnej relacji.

## Jeet Kune Do

Nazwa PL: Jeet Kune Do (JKD)

### About

Jeet Kune Do is Bruce Lee's approach: take what works, without one closed catalogue of forms. It is not a sport federation and not a style with one tournament rulebook.

Jeet Kune Do (JKD) to podejście stworzone przez Bruce'a Lee: bierze to, co działa, bez jednego zamkniętego katalogu form. JKD nie jest federacją sportową ani stylem z jednym turniejowym regulaminem.

### History

Lee developed and described JKD in the 1960s, moving beyond his earlier Wing Chun work. After his death, students read differently whether JKD should be a closed set of techniques or a way of searching further.

Bruce Lee rozwijał JKD w latach 60. XX wieku, wychodząc poza swoje wcześniejsze doświadczenia z wing chun. Po jego śmierci uczniowie różnie interpretowali, czy JKD powinno być zestawem technik, czy raczej metodą dalszego poszukiwania.

### How it is fought

You train with kit, spar, and mix strikes, clinch and simple takedowns, depending on the teacher.

Trening JKD obejmuje ćwiczenia ze sprzętem, sparing oraz łączenie uderzeń, klinczu i prostych obaleń. Metody treningowe mogą się różnić w zależności od nauczyciela.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Jujutsu

Nazwa PL: Jujutsu

### About

Jujutsu is the name for Japanese grappling schools from before judo and for later club ju-jitsu. Koryu, sporting duo and self-defence are not the same fight. Judo developed from older jujutsu schools, while Brazilian jiu-jitsu developed later through Brazilian practice of judo and related grappling. Both have their own cards.

Jujutsu to nazwa na japońskie szkoły chwytów sprzed judo i na późniejsze klubowe ju-jitsu. Koryu, sportowe duo i samoobrona nie grają tą samą walką. Judo rozwinęło się ze starszych szkół jujutsu, natomiast brazylijskie jiu-jitsu rozwinęło się później poprzez brazylijską praktykę judo i pokrewnych form grapplingu. Obie praktyki mają własne karty.

### History

Historical schools, koryu, taught grips, throws, locks and often weapons inside a samurai school. Kano took material from that and built judo. Twentieth-century club ju-jitsu in Europe is a different practice: pairs, self-defence systems and duo contests, not a reconstruction of one Edo school.

Historyczne szkoły, koryu, uczyły chwytów, rzutów, dźwigni i często broni przy szkole samurajskiej. Kano wybrał z tego materiał na judo. XX-wieczne ju-jitsu klubowe w Europie to już inna praktyka: pary, systemy samoobrony i zawody duo, nie odtworzenie jednej szkoły z Edo.

### How it is fought

In koryu you work paired forms and whatever the school counts as technique, weapons included. In club ju-jitsu you more often see atemi, throws, holds and set pairs for a score. That is not judo randori and it is not a points fight in BJJ.

W koryu pracuje się formami pary i tym, co szkoła uznaje za technikę, łącznie z bronią. W klubowym ju-jitsu częściej są atemi, rzuty, trzymania i ułożone pary na ocenę. To nie jest randori judo ani walka BJJ na punkty.

### Facts

Brak osobnego faktu.

### Relations

- Z kartą Judo: Kano arranged judo from the material of older jujutsu schools. Today's sporting judo is not those schools.
Kano ułożył judo z materiału starszych szkół jujutsu. Dzisiejsze judo sportowe nie jest tymi szkołami.
- Z kartą Brazylijskie jiu-jitsu: Some accounts tie BJJ to Maeda's judo and jujutsu. That is not today's club ju-jitsu.
Część opracowań wiąże BJJ z judo i jujutsu Maedy. To nie jest dzisiejsze klubowe ju-jitsu.



## Pankration

Nazwa PL: Pankration

### About

Pankration was a contest at the Greek games: a grip and a strike in one fight. Contemporary groups reconstruct it from vases, texts and commentaries. There is no single federation that is pankration the way UWW is wrestling.

Pankration był konkurencją igrzysk w Grecji: chwyt i uderzenie w jednej walce. Współczesne grupy odtwarzają go z waz, tekstów i przypisów. Nie ma jednej federacji, która byłaby pankrationem tak, jak UWW jest zapaśnictwem.

### History

In antiquity pankration stood beside wrestling and boxing, with a broader combination of striking and grappling than wrestling alone. Today's reconstructions, and sports that borrow the name, are not that ancient contest. The rules from Olympia cannot simply be applied to a modern competition.

W starożytności pankration stał obok zapasów i pięściarstwa jako szersze połączenie uderzeń i chwytów niż same zapasy. Dzisiejsze rekonstrukcje i sporty, które pożyczają nazwę, nie są tym samym antycznym turniejem. Przepisów z Olimpii nie można po prostu zastosować do współczesnych zawodów.

### How it is fought

The ancient picture is a fight standing and on the ground, with strikes and grips, and without modern gloves. A contemporary gym may train that as a reconstruction or as its own sporting rules. You then have to read whose rule it is, because there is not one.

Antyczny obraz to walka w stójce i w parterze, z ciosami i chwytami, bez dzisiejszych rękawic. Współczesna sala może to ćwiczyć jako rekonstrukcję albo jako własny regulamin sportowy. Wtedy trzeba czytać, czyja to zasada, bo jednej nie ma.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Shuai jiao

Nazwa PL: Shuai Jiao

### About

Shuai jiao is Chinese jacket wrestling. Beijing style and other variants differ in the entry and the sleeve grip, but they stay wrestling, not sanda. Strikes do not decide this fight.

Shuai jiao to chińskie zapasy w kurtce. Styl pekiński i inne odmiany różnią się wejściem i chwytem za rękaw, ale zostają zapasami, nie sandą. Uderzenia nie rozstrzygają tej walki.

### History

Jacket wrestling has a long practice in China, and modern contests tidied up the divisions and the grip. Sanda took some of the throws onto its platform and added strikes. That is a neighbourhood, not a second name for the same fight.

Zapasy w kurtce mają w Chinach długą praktykę, a współczesne zawody uporządkowały kategorie i chwyt. Sanda wzięła część rzutów na swoją platformę i dołożyła ciosy. To sąsiedztwo, nie druga nazwa tej samej walki.

### How it is fought

You grip the jacket and the sleeve, enter with the hip or the leg and throw. In Beijing style the stress falls on particular entries; other centres hold the grip differently. There are no kicks scored as in sanda, and no knee clinch.

Łapiesz kurtkę i rękaw, wchodzisz biodrem albo nogą i rzucasz. W stylu pekińskim nacisk pada na określone wejścia; inne ośrodki trzymają chwyt inaczej. Nie ma kopnięć punktowanych jak w sandzie ani klinczu kolanem.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Taekkyeon

Nazwa PL: Taekkyeon

### About

Taekkyeon is a Korean art of fluid, rhythmic movement. The foot matters as much as the hand, and the action can be a strike or a trip. It is not taekwondo.

Taekkyeon to koreańska sztuka o płynnym, rytmicznym ruchu. Stopa jest tu tak ważna jak ręka, a akcja może być uderzeniem albo podcięciem. To nie jest taekwondo.

### History

UNESCO inscribed taekkyeon in 2011 as a traditional martial art, not as the rulebook of World Taekwondo or the ITF. A shared country does not make these practices one sport.

UNESCO wpisało taekkyeon w 2011 roku jako tradycyjną sztukę walki, nie jako regulamin World Taekwondo ani ITF. Wspólny kraj nie łączy tych praktyk w jeden sport.

### How it is fought

The movement is circular and rhythmic, and then it can be sharp. You practise strikes and trips, not an electronic chest guard and not tul forms. A partner is needed when the movement becomes a fight.

Ruch jest okrągły i rytmiczny, a potem może być ostry. Ćwiczy się uderzenia i podcięcia, nie kamizelkę elektroniczną i nie formy tul. Partner jest potrzebny, gdy z ruchu robi się walka.

### Facts

- UNESCO describes taekkyeon as a rhythmic art in which the foot can strike or trip. The 2011 inscription is not a taekwondo rulebook.
UNESCO opisuje taekkyeon jako rytmiczną sztukę, w której stopą można uderzyć albo podciąć. Wpis z 2011 roku nie jest regulaminem taekwondo.



### Relations

Brak osobnej relacji.

## Taijiquan

Nazwa PL: Taijiquan

### About

Taijiquan is a Chinese practice of forms, push-hands and its own sport version. The name gathers schools, among them Chen, Yang, Wu, Sun and Wu (Hao). It is not an abbreviation for all of wushu.

Taijiquan to chińska praktyka form, pchnięć rąk i własnej wersji sportowej. Nazwa zbiera szkoły, między innymi Chen, Yang, Wu, Sun i Wu (Hao). To nie jest skrót na całe wushu.

### History

The schools differ in tempo, in the shape of the movement and in how much application they keep. The IWUF arranged a sport taolu from this, with its own time limit and a list of required movements. Sport forms do not replace the school they came from.

Szkoły różnią się tempem, charakterem ruchu i tym, ile zostawiają zastosowań. IWUF ułożyło z tego sportowe taolu, z osobnym czasem i listą wymaganych ruchów. Formy sportowe nie zastępują szkoły, z której wyszły.

### How it is fought

Solo work is a routine, often slow, sometimes with a sharper release of force. In pairs, push-hands are added: breaking balance without a strike as in sanda. A weapon, for example the taiji sword, is a separate routine, not a points fight.

Solo to układ, często wolny, czasem z ostrzejszym wypuszczeniem siły. W parze dochodzą pchnięcia rąk: wytrącenie równowagi bez ciosu jak w sandzie. Broń, na przykład miecz taiji, jest osobnym układem, nie walką na punkty.

### Facts

- The IWUF lists taijiquan among the taolu and names Chen, Yang, Wu, Sun and Wu (Hao) as competition versions. That is a sporting frame, not the whole practice of those schools.
IWUF wymienia taijiquan wśród taolu i podaje szkoły Chen, Yang, Wu, Sun i Wu (Hao) jako wersje zawodnicze. To sportowa rama, nie cała praktyka tych szkół.



### Relations

Brak osobnej relacji.

## Catch wrestling

Nazwa PL: Catch wrestling

### About

Catch is wrestling in which a submission, a lock or a choke, sits beside the throw and the control. It is not Olympic freestyle or Greco-Roman, because those bouts do not go looking for a lock as the aim.

Catch to zapasy, w których obok rzutu i kontroli jest poddanie: dźwignia albo duszenie. To nie jest olimpijski styl wolny ani klasyczny, bo tam walka nie idzie po dźwignię jako cel.

### History

Catch-as-catch-can developed within British wrestling traditions and later became influential in the United States. Historical and modern forms differ in rules and in how central submissions are. Freestyle and Greco-Roman remained separate Olympic styles with their own rules on points and falls.

Catch-as-catch-can rozwinęło się w ramach brytyjskich tradycji zapaśniczych, a później stało się wpływowe w Stanach Zjednoczonych. Formy historyczne i współczesne różnią się regulaminami oraz tym, jak centralną rolę odgrywają poddania. Styl wolny i klasyczny pozostały odrębnymi stylami olimpijskimi z własnymi zasadami punktowania i zakończenia walki.

### How it is fought

You level for the grip, take the opponent down and look for a position from which a lock can be put on. There are no strikes. A judo jacket is usually absent too: the grip goes to the body and the joint.

Schodzisz do chwytu, obalasz i szukasz pozycji, z której da się założyć dźwignię. Nie ma ciosów. Kurtki judo też zwykle nie ma: chwyt idzie na ciało i na staw.

### Facts

- Catch differs from Olympic wrestling in that a submission is part of the fight. Freestyle and Greco-Roman do not have that aim.
Catch różni się od zapasów olimpijskich tym, że poddanie jest częścią walki. Styl wolny i klasyczny tego celu nie mają.



### Relations

Brak osobnej relacji.

## Luta livre esportiva

Nazwa PL: Luta livre esportiva

### About

Luta livre esportiva is Brazilian grappling without the gi: takedowns, control and submissions, with no strikes. Historically it stood beside BJJ, not as BJJ's no-gi rule.

Luta livre esportiva to brazylijski grappling bez kimona: obalenia, kontrola i poddania, bez uderzeń. Historycznie stała obok BJJ, a nie jako jego reguła no-gi.

### History

In Brazil luta livre grew as wrestling with submissions, beside the Gracie line. The esportiva format leaves strikes out. Vale tudo, where the strikes come back, is a different practice and closer to early MMA than to this card.

W Brazylii luta livre urosła jako zapasy z poddaniami, obok linii Gracie. Formuła esportiva zostawia ciosy na boku. Vale tudo, w którym uderzenia wracają, jest inną praktyką i bliższą wczesnemu MMA niż tej karcie.

### How it is fought

You fight without the gi. The grip goes to the wrist, the neck and the leg, not to the collar. Sparring looks for a submission. It is not judo randori and it is not points BJJ in the gi, even when some techniques look alike.

Walczysz bez kimona. Chwyt idzie na nadgarstek, szyję i nogę, a nie na kołnierz. Sparing szuka poddania. To nie jest randori judo i nie jest punktowe BJJ w gi, nawet gdy część technik wygląda podobnie.

### Facts

- Luta livre esportiva is grappling without strikes and without the gi. It is not the same as BJJ, even when both practices go to the ground.
Luta livre esportiva jest grapplingiem bez uderzeń i bez kimona. Nie jest tym samym co BJJ, nawet gdy obie praktyki schodzą do parteru.



### Relations

Brak osobnej relacji.

## Iaido

Nazwa PL: Iaido

### About

Iaido is sword forms: draw, cut and sheathe, usually solo. The All Japan Kendo Federation has its own set of kata, but iaido is not scored kendo with a shinai.

Iaido to formy z mieczem: dobyć, ciąć i schować, zwykle solo. All Japan Kendo Federation ma własny zestaw kata, ale iaido nie jest punktowanym kendo na shinai.

### History

The sword schools are older than the shared catalogue. In 1969 the AJKF arranged standardised kata, later extended, so a performance could be compared. Kenjutsu stays with the school and its pairs, without that catalogue and without a kendo tournament.

Szkoły miecza są starsze niż wspólny katalog. W 1969 roku AJKF ułożyła standaryzowane kata, później rozszerzone, żeby dało się porównać wykonanie. Kenjutsu zostaje przy szkole i jej parach, bez tego katalogu i bez turnieju kendo.

### How it is fought

You practise a catalogue of forms, often with a training sword, sometimes with a live blade under the school's supervision. There is no bogu armour and no point for a men strike. A score, if there is one, is about the cut, the posture and the draw, not an exchange of blows.

Ćwiczy się katalog form, często mieczem treningowym, czasem ostrzem pod nadzorem szkoły. Nie ma zbroi bogu ani punktu za men. Ocena, jeśli jest, dotyczy cięcia, postawy i dobycia, nie wymiany ciosów.

### Facts

- The AJKF describes iaido as drawing the sword in forms. Iaido contests judge kata, not a shinai hit in kendo armour.
AJKF opisuje iaido jako dobywanie miecza w formach. Zawody iaido oceniają kata, a nie trafienie shinai w zbroi kendo.



### Relations

Brak osobnej relacji.

## Kyudo

Nazwa PL: Kyudo

### About

Kyudo is Japanese archery as budō: the bow, the arrow, the ceremony of the shot and training of posture. It is not a variant of kendo and it is not timed Olympic archery.

Kyudo to japońskie łucznictwo jako budō: łuk, strzała, ceremonia strzału i trening postawy. To nie jest odmiana kendo i nie jest łucznictwem olimpijskim na czas.

### History

The bow was a weapon in Japan, and later a way of training. The International Kyudo Federation, founded in 2006, runs contests and exams outside Japan together with the All Nippon Kyudo Federation. The kendo shinai and armour are not part of this kit.

Łuk był w Japonii bronią, a potem drogą treningu. International Kyudo Federation, założona w 2006 roku, prowadzi zawody i egzaminy poza Japonią razem z All Nippon Kyudo Federation. Shinai i zbroja kendo nie wchodzą do tego sprzętu.

### How it is fought

You stand, nock the arrow and release it in a set form. A partner does not parry with a sword. Contests are shooting at a mato, not an unarmed fight.

Stoisz, nakładasz strzałę i wypuszczasz ją w ustalonej formie. Partner nie zasłania się mieczem. Zawody są strzelaniem do mato, nie walką wręcz.

### Facts

- Kyudo is archery as budō. The International Kyudo Federation runs it separately from kendo.
Kyudo jest łucznictwem jako budō. International Kyudo Federation prowadzi je osobno od kendo.



### Relations

Brak osobnej relacji.

## Bökh

Nazwa PL: Bökh

### About

Bökh is the Mongolian wrestling of Naadam, not the name of the whole festival. It is defined by the zodog and shuudag costume, an upper-body grip, and a win when the opponent touches the ground in a way defined by the local rules. There are no strikes.

Bökh to mongolskie zapasy Naadam, nie nazwa całego święta. Charakterystyczne są strój zodog i shuudag, chwyt za górę ciała oraz zwycięstwo, gdy rywal dotknie ziemi w sposób określony przez lokalne zasady. Ciosów nie ma.

### History

Naadam is wrestling, archery and horse racing. Bökh is one of those three. The entrance ritual and the costume are part of the contest, not an interval before the real fight.

Naadam składa się z zapasów, łucznictwa i wyścigów konnych. Bökh jest jedną z tych trzech rzeczy. Rytuał wejścia i strój są częścią zawodów, a nie przerywnikiem przed właściwą walką.

### How it is fought

The grip goes to the jacket and the torso. The bout ends when the opponent touches the ground in a way defined by the local rules; the details vary between variants. There is no belt as in ssireum, no Olympic mat, and it is not fought to the clock the way freestyle is.

Chwyt idzie za kurtkę i za tors. Starcie kończy się, gdy rywal dotknie ziemi w sposób określony przez lokalne zasady; szczegóły różnią się między odmianami. Nie ma pasa jak w ssireum, nie ma maty olimpijskiej i nie walczy się do upływu czasu w ten sam sposób co w stylu wolnym.

### Facts

- Naadam in Mongolia is wrestling, archery and horse racing. Bökh is one of those three contests, not the whole festival.
Naadam w Mongolii to zapasy, łucznictwo i wyścigi konne. Bökh jest jedną z tych trzech konkurencji, a nie całym świętem.



### Relations

Brak osobnej relacji.

## Ssireum

Nazwa PL: Ssireum

### About

Ssireum is Korean belt wrestling on sand, with the satba. You hold the opponent by the belt and throw so that a part of the body above the knee touches the ground. UNESCO inscribed ssireum in 2018 as a tradition shared by both Koreas.

Ssireum to koreańskie zapasy na pasie satba, na piasku. Obejmujesz rywala za pas i rzucasz tak, by część ciała powyżej kolana dotknęła ziemi. UNESCO wpisało ssireum w 2018 roku jako tradycję wspólną dla obu Korei.

### History

The satba wraps the waist and the thigh, so the grip has a fixed place, unlike Olympic wrestling. In the traditional adult format the final winner used to receive an ox. Modern contests have divisions, but the sand and the belt remain.

Satba owija biodro i udo, więc chwyt ma stałe miejsce, inaczej niż w zapasach olimpijskich. W tradycyjnej formule dorosłych zwycięzca finału bywał nagradzany wołem. Współczesne zawody mają kategorie, ale piasek i pas zostają.

### How it is fought

You do not attack the leg the way you do in freestyle. The force goes through the belt, and the torso touching the sand ends the action. This is not taekwondo and it is not taekkyeon: there are no kicks.

Nie łapiesz nogi jak w stylu wolnym. Siła idzie przez pas, a dotknięcie piasku tułowiem kończy akcję. To nie jest taekwondo i nie jest taekkyeon: nie ma kopnięć.

### Facts

- UNESCO inscribed ssireum in 2018 as a tradition shared by both Koreas. The satba belt, the sand and an ox for the winner of the adult final are part of that description, not decoration.
UNESCO wpisało ssireum w 2018 roku jako tradycję wspólną dla obu Korei. Pas satba, piasek i wół dla zwycięzcy finału dorosłych są częścią tego opisu, nie ozdobnikiem.



### Relations

Brak osobnej relacji.

## Chidaoba

Nazwa PL: Chidaoba

### About

Chidaoba is Georgian wrestling in the chokha. A throw with a grip wins, and the catalogue of holds is large. Zurna and doli play by the arena. UNESCO inscribed chidaoba in 2018.

Chidaoba to gruzińskie zapasy w stroju chokha. Wygrywa rzut przy chwytach, których katalog jest duży. Przy arenie grają zurna i doli. UNESCO wpisało chidaobę w 2018 roku.

### History

The costume, the music and the names of the holds are part of the description, not a folklore extra. This is not Greco-Roman on a UWW mat: a different space, a different grip and a different way to end the action.

Strój, muzyka i nazwy chwytów są częścią opisu, nie dodatkiem folklorystycznym. To nie jest styl klasyczny na macie UWW: inna przestrzeń, inny chwyt i inne zakończenie akcji.

### How it is fought

You fight by gripping the costume and the body, with no strikes. The opponent's fall decides it. Music and traditional presentation remain part of the setting, alongside the rules of the contest.

Walczy się w chwycie za strój i za ciało, bez ciosów. Upadek rywala rozstrzyga. Muzyka i tradycyjna oprawa pozostają częścią otoczenia walki, obok zasad samego konkursu.

### Facts

- UNESCO inscribed chidaoba in 2018. The chokha costume and the zurna and doli music beside the fight belong to that description.
UNESCO wpisało chidaobę w 2018 roku. Do opisu należą strój chokha oraz muzyka zurna i doli przy walce.



### Relations

Brak osobnej relacji.

## Laamb

Nazwa PL: Laamb

### About

Laamb is Senegalese wrestling. The avec frappe format adds strikes, and the format without strikes stays with grips and throws. One name does not mean one rule set.

Laamb to senegalskie zapasy. W formule avec frappe dochodzą uderzenia, a w formule bez uderzeń zostają chwyty i rzuty. Jedna nazwa nie znaczy jednego regulaminu.

### History

Wrestling is a major spectacle in Senegal, with its own ground and an entrance ceremony. Cards with frappe are a newer layer. This entry cannot be reduced to the sentence “grips, throws, no strikes”.

Walka zapaśnicza jest w Senegalu dużym widowiskiem, z własnym polem i z ceremonią wejścia. Gale z frappe to warstwa nowsza. Nie da się tego wpisu sprowadzić do zdania „chwyty, rzuty, bez uderzeń”.

### How it is fought

In the format without strikes you look for a throw to the ground. In the avec frappe format you may strike before the grip. The ground is not an Olympic mat, and the end of the fight depends on the format, not on a rule shared with bökh.

W formule bez uderzeń szukasz rzutu na ziemię. W formule z uderzeniami (frappe) wolno bić, zanim dojdzie do chwytu. Pole nie jest matą olimpijską, a koniec walki zależy od formuły, nie od wspólnego przepisu z bökh.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Glíma

Nazwa PL: Glíma

### About

Glíma is Icelandic wrestling, most often with a belt, moving in a circle. A throw ends the action. There are no strikes. Medieval continuity cannot be proved from the training alone.

Glíma to islandzkie zapasy, najczęściej w pasie, z ruchem po kole. Rzut kończy akcję. Uderzeń nie ma. Średniowiecznej ciągłości nie da się tu dowieść z samego treningu.

### History

The belt and the circular step distinguish glíma from freestyle. A story of a straight line from the sagas is weaker than the description of the grip itself, so I leave it as a story, not as a certificate.

Pas i krok po okręgu odróżniają glímę od stylu wolnego. Opowieść o linii prostej od sag jest słabsza niż opis samego chwytu, więc zostawiam ją jako opowieść, nie jako metrykę.

### How it is fought

You stand in the belt, hold the grip and break balance on the move, not in an Olympic clinch. The ground after a throw decides it. There is no ssireum sand and no bökh jacket.

Stoisz w pasie, trzymasz uchwyt i wytrącasz rywala z równowagi w ruchu, nie w klinczu olimpijskim. Dotknięcie ziemi po rzucie rozstrzyga. Nie ma piasku ssireum ani kurtki bökh.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Alysh

Nazwa PL: Alysh

### About

Alysh is Central Asian belt wrestling, especially in Kyrgyzstan. The grip goes to the belt, and a throw ends the action. It is not kurash, even though the region is the same.

Alysh to środkowoazjatyckie zapasy na pasie, szczególnie w Kirgistanie. Chwyt idzie na pas, a rzut kończy akcję. To nie jest kurash, choć region jest ten sam.

### History

International starts are a newer frame on older folk wrestling. Kurash has its own jacket grip and its own federation. A shared map does not make a belt and a jacket the same.

Międzynarodowe starty są nowszą ramą na starszych zapasach ludowych. Kurash ma własny chwyt za kurtkę i własną federację. Wspólna mapa nie zrówna pasa z kurtką.

### How it is fought

You hold the belt with both hands and enter a hip throw. There are no strikes. It cannot be described as freestyle: the belt fixes the grip from the start and the bout follows its own rules.

Trzymasz pas obiema rękami i wchodzisz na rzut biodrem. Ciosów nie ma. Nie można opisać tego jako stylu wolnego: pas wyznacza chwyt od początku, a walka ma własne zasady.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Kurash

Nazwa PL: Kurash

### About

Kurash is Uzbek jacket wrestling. A grip on the jacket decides the throw, with no ground fight after the fall. It is not belt alysh and it is not judo, even with a similar jacket.

Kurash to uzbeckie zapasy w kurtce. Chwyt za połę rozstrzyga rzut, bez walki w parterze po upadku. To nie jest alysh na pasie i nie jest judo, mimo podobnej kurtki.

### History

The international kurash federation tidied the contests in the twentieth and twenty-first centuries. The older practice is Central Asian. Alysh stays with the belt, sambo with its own jacket and with locks that are not part of this.

Międzynarodowa federacja kurash uporządkowała zawody w XX i XXI wieku. Starsza praktyka jest środkowoazjatycka. Alysh zostaje przy pasie, sambo przy własnej kurtce i przy dźwigniach, których tu nie ma.

### How it is fought

A throw under the rules can score or end the bout, and the action does not continue on the ground. There are no strikes. The jacket is part of the rules, not only the costume.

Rzut zgodny z regulaminem może dać punkty albo zakończyć walkę, a akcja nie jest kontynuowana w parterze. Uderzeń nie ma. Kurtka jest częścią zasad walki, a nie tylko strojem.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Gatka

Nazwa PL: Gatka

### About

Gatka is a Sikh weapon art, practised with a stick, a sword and other tools, often at demonstrations and at nagar kirtan.

Gatka to sikhijska sztuka broni, ćwiczona kijem, mieczem i innymi narzędziami, często przy pokazach i przy nagar kirtan.

### History

Weapons and the Sikh community are the context, not decoration. Contemporary schools teach gatka both as a martial practice and as a cultural and religious tradition. It is not HEMA and it is not kendo: different sources, different weapons and a different context.

Broń i wspólnota sikhijska są kontekstem, nie ozdobnikiem. Współczesne szkoły uczą gatki zarówno jako praktyki walki, jak i tradycji kulturowej i religijnej. Nie jest to HEMA ani kendo: inne źródła, inna broń i inny kontekst.

### How it is fought

You drill forms and pairs with a stick and with weapons, often in a circular movement. Tournament contact is not the axis, the way it is in fencing. The demonstration and the training of a religious community stay part of the practice.

Ćwiczy się formy i pary na kiju oraz na broni, często w ruchu kołowym. Kontakt turniejowy nie jest tu osią, tak jak w szermierce. Pokaz i szkolenie religijnej wspólnoty zostają częścią praktyki.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Kalaripayattu

Nazwa PL: Kalaripayattu

### About

Kalaripayattu is an art from Kerala, practised in a kalari, a training space that is often sunken. There are northern and southern currents, forms, weapons and body work. It is not an Indian name for kickboxing.

Kalaripayattu to sztuka z Kerali, ćwiczona w kalari, czyli często zagłębionej sali treningowej. Są nurty północny i południowy, formy, broń i praca z ciałem. To nie jest indyjska nazwa na kickboxing.

### History

Northern and southern styles differ in forms, weapons and in the emphasis placed on massage and treatment in the kalari tradition. Sources for a medieval unbroken line are thinner than the description of the practice in Kerala, so the card does not turn them into one founding date.

Północne i południowe style różnią się formami, bronią oraz naciskiem na masaż i leczenie w tradycji kalari. Źródła dotyczące nieprzerwanej średniowiecznej ciągłości są słabsze niż źródła opisujące samą praktykę w Kerali, dlatego karta nie sprowadza ich do jednej daty założenia.

### How it is fought

Warm-up and forms come before weapons: stick, dagger, sword and shield, depending on the current. The empty hand is in the set, but the kalari and the sequences do not look like a round in a ring. A partner is needed for weapons and for applications.

Rozgrzewka i formy idą przed bronią: kij, sztylet, miecz i tarcza zależnie od nurtu. Pusta ręka jest w zestawie, ale sala kalari i sekwencje nie wyglądają jak runda na ringu. Partner jest potrzebny przy broni i przy zastosowaniach.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Dambe

Nazwa PL: Dambe

### About

Dambe is a fighting style that comes from Hausa tradition. Traditionally one hand is wrapped in a distinctive way, and kicks also appear in the fight. It is something different from gloved boxing.

Dambe to tradycyjna sztuka walki wywodząca się z kultury ludu Hausa w Afryce Zachodniej. Charakteryzuje się owijaniem jednej ręki w charakterystyczny sposób oraz wykorzystaniem kopnięć. Różni się od boksu w rękawicach.

### History

Dambe is tied to Hausa tradition, historically also to particular occupational groups and to shows. Modern events can change protection, judging and other details, so not every modern bout looks identical to a traditional fight.

Dambe jest ściśle związane z kulturą Hausa i historycznie z określonymi grupami zawodowymi oraz pokazami. Współczesne pojedynki mogą różnić się od tradycyjnych starć pod względem zabezpieczeń i zasad sędziowania.

### How it is fought

You fight with a wrapped fist, in a guard, with kicks. Contact is part of the traditional bout.

Walczy się z owiniętą pięścią, w gardzie, z kopnięciami. Kontakt jest częścią tradycyjnego starcia.

### Facts

Brak osobnego faktu.

### Relations

Brak osobnej relacji.

## Do sprawdzenia

- Drugie źródło części kart nadal jest tylko stroną „discovery” (Encyclopaedia Britannica o kraju albo o sztukach walki w ogóle, nie o danej praktyce): krav maga, hapkido, bökh, laamb, glíma, gatka, kalaripayattu, dambe. Rozszerzony opis opiera się na haśle Wikipedii już podpiętym do karty.
- Nazwy szkół wewnątrz parasoli (Shotokan, goju-ryu, Modern Arnis, Doce Pares, Balintawak, IKMF, KMG, hung gar i inne) nie mają tu osobnego adresu federacji. Stoją w opisie karty-matki.
- Drugie źródło catchu to hasło Brittaniki o zapasach, bliższe stylowi wolnemu i klasycznemu niż poddaniom. Zdanie o poddaniu opiera się na haśle Wikipedii o catch wrestling.
- Lethwei: International Lethwei Unified Ruleset (LFC, 14 June 2025) nie jest w tej chwili pod publicznym, stałym URL na stronie promocji; opis sprzętu opiera się na Wikipedii i na rozróżnieniu form tradycyjnych i współczesnych, bez uogólniania formuły międzynarodowej na całe tradycyjne lethwei.
- Luta livre ma dwa hasła Wikipedii, angielskie i portugalskie, bez strony federacji.
- Przy chidaobie nie wpisałem liczby chwytów. UNESCO potwierdza wpis, strój i oprawę, a konkretnej liczby tu nie przypinam.
- Kenjutsu jest zdaniem przy kendo i przy HEMA, nie osobną kartą.



## Prompt do wklejenia

Sprawdź poniższy katalog sztuk i sportów walki. Został napisany jako pary: najpierw angielski, pod nim polski. Nie przepisuj całości i nie dodawaj profilu liczbowego (niski, średni, wysoki ani skali 1–5).

Zrób pięć rzeczy:

1. Wiarygodność. Przy każdej uwadze podaj, czego dotyczy karta, co budzi wątpliwość i źródło, na którym się oprzesz (federacja, UNESCO, encyklopedia, regulamin). Odznacz też zdania, które są w porządku, ale nie cytuj całych akapitów.
2. Granice kart. Napisz, czy obecny podział jest trafny: co jest słusznie zlane w jedną kartę, co jest zdublowane i co zostało potraktowane jako jedna sztuka, choć regulaminy albo tradycje się rozjeżdżają.
3. Braki. Zaproponuj sporty i sztuki, których tu nie ma. Przy każdej napisz, czy to odmiana karty, która już jest, czy osobna karta. Nie zakładaj, że każda nazwa szkoły zasługuje na własny wpis.
4. Polski wobec angielskiego. Wskaż miejsca, w których polski gubi, zaostrza albo przekręca sens angielskiego nad nim. Nie wygładzaj stylu, jeśli sens się zgadza.
5. Zostaw głos tekstu. Krótkie zdania sprawdzalne mają zostać. Nie dopisuj żartów, tagów ani ocen „jak bardzo” coś jest kontaktowe.

Odpowiedź pogrupuj: błędy, sporne granice kart, propozycje braków (odmiana albo nowa karta), rozjazdy PL/EN. Na końcu krótka lista tego, czego nie dało się sprawdzić.

## Sekcja C — quizopasowanie.md



# Quizopasowanie — do oceny



## Polecenie

Oceń quiz dopasowania ze strony wiciędze. Nie jest testem osobowości, nie mierzy skuteczności w walce i nie jest walidowanym kwestionariuszem. Pyta, jak ktoś chce trenować, i układa z odpowiedzi krótką listę stylów do poczytania.

Najpierw angielski, pod nim polski. Angielski jest tekstem roboczym. Polski ma trzymać ten sam sens.

Zrób cztery rzeczy, w tej kolejności.

1. Wiarygodność mechanizmu. Czy z tych pytań i wag da się uczciwie ułożyć listę „do poczytania”, czy quiz obiecuje więcej, niż liczy? Wskaż pytania, które mierzą dwie rzeczy naraz, nie mają odpowiedzi dla czyjegoś realnego treningu albo ruszają oś, której człowiek w pytaniu nie słyszy. Przy każdej uwadze napisz, którego pytania dotyczy i co by się przez to stało z listą.
2. Jakość pytań i zdań na wyniku. Czy da się odpowiedzieć bez zgadywania, czy skala 1–5 jest jasna, czy opcje A/B i sytuacja naprawdę się wykluczają, czy ostatnie pytanie (kilka odpowiedzi) nie gryzie się z „nic z tego”. Osobno oceń zdania, które quiz dokleja pod stylem: czy nie mówią „dużo”, kiedy obie strony są tylko średnie, i czy nie brzmią jak werdykt o człowieku.
3. Polski wobec angielskiego. Wskaż miejsca, w których polski gubi, zaostrza albo przekręca sens angielskiego nad nim. Nie wygładzaj stylu, jeśli sens się zgadza. Głos ma zostać krótki i konkretny.
4. Rozszerzenie tylko tam, gdzie dziura zmienia listę. Brakującą oś albo brakującą odpowiedź zgłoś jako nowe pytanie albo jako poprawkę istniejącego. Napisz, jaką oś by ruszało i jakiej odpowiedzi dziś nie ma. Nie dopisuj pytań „dla kompletności”, jeśli i tak nie zmieniają dopasowania. Nie proponuj testu osobowości.

Nie przepisuj całego quizu. Nie dodawaj skali skuteczności. Nie wymyślaj, który styl „powinien” wygrać, chyba że liczysz to wprost z zasad poniżej i piszesz, jakie odpowiedzi założyłeś.

Odpowiedź pogrupuj: błędy mechanizmu, słabe pytania, rozjazdy PL/EN, propozycje (nowe pytanie albo poprawka), rzeczy do zostawienia.

## Jak to jest liczone

Każdy styl ma ręczny profil: 22 osie, każda od 0 do 5. To opis treningu, nie ranking siły. Quiz nie pokazuje tej liczby. Pokazuje listę.

Oś ze skali 1–5 wchodzi jako 0, 1,25, 2,5, 3,75 albo 5. Jedna odpowiedź A/B lub z sytuacji ma wagi. Waga +2 staje się 5, +1 staje się 3,75, −1 staje się 1,25, −2 staje się 0. Gdy kilka odpowiedzi tyka tę samą oś, quiz bierze średnią. Osi, której nikt nie tyknął, nie ma w rachunku. Odległość to średnia z modułów różnic na wspólnych osiach. Mniejsza odległość jest wyżej. Przy remisie wygrywa slug wcześniejszy alfabetycznie.

Na listę wchodzi pięć stylów, najwyżej dwa z jednej rodziny (uderzenia, chwyty, mieszane, broń). Jeśli dwa z tej piątki są w katalogu powiązane, późniejszy nie dostaje własnej karty: zostaje dopiskiem „Blisko tego jest” pod wcześniejszym, a na wolne miejsce quiz bierze kolejny styl, dalej z limitem rodziny i bez dokładania kolejnego powiązanego.

Pod stylem są najwyżej trzy zdania zgody i dwa zdania różnicy. Zgoda: różnica co najwyżej 1 i obie strony co najmniej 3, albo obie niskie (człowiek do 1,5, styl do 1). Różnica: odstęp co najmniej 2,5. Zdanie mówi wtedy, czy w stylu jest tego więcej, czy mniej. Oś bez zdania w banku nie dostaje komentarza.

Wymagane są skale, oba wybory A/B i sytuacja. Ostatnie pytanie można zostawić puste. „Nic z tego” ma puste wagi: samo nic nie wnosi, a zaznaczone razem z innymi punktami ich nie kasuje.

Osie pytanie wprost: uderzenia, chwyt, parter, broń, kopnięcia, kontakt, zawody, tradycja. Osie tylko z opcji: solo, partner, klincz, rzuty, obalenia, poddania, pięści, kolana, łokcie, wytrzymałość, eksplozywność, sprzęt. Osie, których quiz wcale nie tyka: złożoność techniczna, obciążenie fizyczne.

## Tekst wokół quizu



### Wejście

Click around and you get a short list of styles matched to your answers.

Se poklikaj, a dostaniesz krótką listę stylów dopasowanych do Twoich odpowiedzi.

### Błąd, gdy brakuje odpowiedzi

Mark every scale, both choices and the situation. Only then does the list show up.

Zaznacz każdą skalę, oba wybory i sytuację. Dopiero wtedy pokaże się lista.

### Skala

1 means not at all, 5 — very much.

1 oznacza wcale, 5 — bardzo.

### Wynik

Five styles to read about — starting with the one that best matches your answers.

Pięć stylów do poczytania — od tego, który najbardziej pasuje do Twoich odpowiedzi.

Next to this sits …

Blisko tego jest …

It's an umbrella name, not one rule set, so this description doesn't fit every school or hall.

To nazwa zbiorcza, nie jeden regulamin, więc ten opis nie pasuje do każdej szkoły ani sali.

Less obvious

Mniej oczywiste

„Mniej oczywiste” dostaje styl z zestawu pobocznego, jeśli wejdzie na listę. Nazwa zbiorcza dostaje pierwsze zdanie, gdy kartoteka tak ją oznacza.

## Pytania



### 1. Skala, wymagane. Oś: uderzenia

How much do you want to strike?

Jak bardzo chcesz uderzać?

1 wcale … 5 bardzo. Ta liczba jest całą wartością osi uderzeń.

### 2. Skala, wymagane. Oś: chwyt

How much do you want to grapple and hold?

Jak bardzo chcesz chwytać i trzymać?

### 3. Skala, wymagane. Oś: parter

How much do you want to fight on the ground?

Jak bardzo chcesz walczyć w parterze?

### 4. Skala, wymagane. Oś: broń

How much do you want a weapon in training?

Jak bardzo chcesz mieć broń na treningu?

### 5. Skala, wymagane. Oś: kopnięcia

How much do you want to kick?

Jak bardzo chcesz kopać?

### 6. Skala, wymagane. Oś: kontakt

How hard should the contact be?

Jak mocny ma być kontakt?

### 7. Skala, wymagane. Oś: zawody

How much do you want to compete?

Jak bardzo chcesz startować w zawodach?

### 8. Skala, wymagane. Oś: tradycja

How much do traditions and hall customs matter to you?

Jak ważne są dla Ciebie tradycje i zwyczaje w sali?

### 9. Wybór jednego, wymagane

Would you rather train alone, or with a partner?

Wolisz ćwiczyć sam czy z partnerem?

- Alone, with technique or a bag. — solo +2 (wartość 5), partner −2 (wartość 0).
Sam, technika albo worek.
- With a partner who moves. — partner +2 (wartość 5), solo −2 (wartość 0).
Z partnerem, który się rusza.



### 10. Wybór jednego, wymagane

Would you rather stay far, or step in close?

Wolisz zostać daleko czy wejść blisko?

- At a distance, let the leg do the work. — kopnięcia +2 (wartość 5), klincz −2 (wartość 0). Średnia z pytania 5, jeśli ktoś już ustawił kopnięcia.
Z daleka, niech noga robi robotę.
- Up close, a clinch or a grip. — klincz +2 (wartość 5), kopnięcia −1 (wartość 1,25).
Z bliska, klincz albo chwyt.



### 11. Sytuacja, jeden wybór, wymagane

In training it comes to close range. What should happen next?

Na treningu dochodzi do zwarcia. Co ma być dalej?

- A throw. — rzuty +2 (wartość 5), obalenia +1 (wartość 3,75).
Rzut.
- You go to the ground and look for a submission. — poddania +2 (wartość 5), parter +2 (wartość 5). Średnia z pytania 3 na osi parteru.
Schodzicie do parteru i szukacie poddania.
- A strike and a step out. — pięści +2 (wartość 5), uderzenia +1 (wartość 3,75). Średnia z pytania 1 na osi uderzeń.
Uderzenie i odskok.



### 12. Kilka odpowiedzi, niewymagane

Tick what should be in your training week. You can pick several, or leave it blank if none of it matters to you.

Zaznacz, co ma być w Twoim tygodniu treningowym. Możesz wybrać kilka rzeczy naraz, a jeśli nic z tego Cię nie rusza, zostaw puste.

- Knees and elbows. — kolana +2 (wartość 5), łokcie +2 (wartość 5).
Kolana i łokcie.
- Armour or a mask. — sprzęt +2 (wartość 5).
Zbroja albo maska.
- Gloves. — sprzęt +1 (wartość 3,75). Średnia ze „zbroja albo maska”, jeśli oba są zaznaczone.
Rękawice.
- Endurance, long rounds. — wytrzymałość +2 (wartość 5).
Wytrzymałość, długie rundy.
- An explosive entry. — eksplozywność +2 (wartość 5).
Szybkie, mocne wejście.
- None of these. — brak wag. Nie zeruje pozostałych ptaszków.
Nic z tego.



## Zdania pod wynikiem

Quiz bierze gotowe zdanie dla osi. Nie wstawia nazwy stylu. Kolejność przy każdej osi: zgoda na wysokiej wartości, w stylu jest tego więcej, w stylu jest tego mniej, zgoda na niskiej wartości.

### Uderzenia

You want a lot of striking, and there's a lot of it here.

Chcesz dużo uderzeń i tutaj jest ich dużo.

There's more striking here than you're after.

Uderzeń jest tu więcej, niż szukasz.

There's less striking here than you're after.

Uderzeń jest tu mniej, niż szukasz.

There's little striking here — and that's what you want.

Uderzeń jest tu mało — i dobrze, bo właśnie tego szukasz.

### Chwyt

You want a lot of grappling, and there's a lot of it here.

Chcesz dużo chwytów i tutaj jest ich dużo.

There's more grappling here than you're after.

Chwytów jest tu więcej, niż szukasz.

There's less grappling here than you're after.

Chwytów jest tu mniej, niż szukasz.

There's little grappling here — and that's what you want.

Chwytów jest tu mało — i dobrze, bo właśnie tego szukasz.

### Klincz

Close-range work matters here about as much as you want.

Walka w zwarciu jest tu mniej więcej tak ważna, jak chcesz.

There's more close-range work here than you're after.

Zwarcia jest tu więcej, niż szukasz.

There's less close-range work here than you're after.

Zwarcia jest tu mniej, niż szukasz.

There's little close-range work here — and that's what you want.

Zwarcia jest tu mało — i dobrze, bo właśnie tego szukasz.

### Rzuty

Throws matter here about as much as you want.

Rzuty są tu mniej więcej tak ważne, jak chcesz.

There are more throws here than you're after.

Rzutów jest tu więcej, niż szukasz.

There are fewer throws here than you're after.

Rzutów jest tu mniej, niż szukasz.

There are few throws here — and that's what you want.

Rzutów jest tu mało — i dobrze, bo właśnie tego szukasz.

### Obalenia

There are about as many takedowns here as you want.

Obaleń jest tu mniej więcej tyle, ile chcesz.

There are more takedowns here than you're after.

Obaleń jest tu więcej, niż szukasz.

There are fewer takedowns here than you're after.

Obaleń jest tu mniej, niż szukasz.

There are few takedowns here — and that's what you want.

Obaleń jest tu mało — i dobrze, bo właśnie tego szukasz.

### Parter

There's about as much ground work here as you want.

Parteru jest tu mniej więcej tyle, ile chcesz.

There's more ground work here than you're after.

Parteru jest tu więcej, niż szukasz.

There's less ground work here than you're after.

Parteru jest tu mniej, niż szukasz.

There's little ground work here — and that's what you want.

Parteru jest tu mało — i dobrze, bo właśnie tego szukasz.

### Poddania

Going for a submission fits this training about as much as you want.

Szukanie poddania pasuje do tego treningu mniej więcej tak, jak chcesz.

Submissions matter more here than you're after.

Poddania liczą się tu bardziej, niż szukasz.

Submissions matter less here than you're after.

Poddania liczą się tu mniej, niż szukasz.

Submissions barely matter here — and that's what you want.

Poddania prawie tu nie mają znaczenia — i dobrze, bo właśnie tego szukasz.

### Pięści

Fist work matters here about as much as you want.

Praca pięścią jest tu mniej więcej tak ważna, jak chcesz.

Fists matter more here than you're after.

Pięści liczą się tu bardziej, niż szukasz.

Fists matter less here than you're after.

Pięści liczą się tu mniej, niż szukasz.

Fists barely matter here — and that's what you want.

Pięści prawie tu nie mają znaczenia — i dobrze, bo właśnie tego szukasz.

### Kopnięcia

Kicks are about as common here as you want.

Kopnięcia są tu mniej więcej tak częste, jak chcesz.

There are more kicks here than you're after.

Kopnięć jest tu więcej, niż szukasz.

There are fewer kicks here than you're after.

Kopnięć jest tu mniej, niż szukasz.

There are few kicks here — and that's what you want.

Kopnięć jest tu mało — i dobrze, bo właśnie tego szukasz.

### Kolana

Knees matter here about as much as you want.

Kolana są tu mniej więcej tak ważne, jak chcesz.

Knees matter more here than you're after.

Kolana liczą się tu bardziej, niż szukasz.

Knees matter less here than you're after.

Kolana liczą się tu mniej, niż szukasz.

Knees barely matter here — and that's what you want.

Kolana prawie tu nie mają znaczenia — i dobrze, bo właśnie tego szukasz.

### Łokcie

Elbows matter here about as much as you want.

Łokcie są tu mniej więcej tak ważne, jak chcesz.

Elbows matter more here than you're after.

Łokcie liczą się tu bardziej, niż szukasz.

Elbows matter less here than you're after.

Łokcie liczą się tu mniej, niż szukasz.

Elbows barely matter here — and that's what you want.

Łokcie prawie tu nie mają znaczenia — i dobrze, bo właśnie tego szukasz.

### Broń

Weapons matter in this training about as much as you want.

Broń na tym treningu jest mniej więcej tak ważna, jak chcesz.

Weapons matter more here than you're after.

Broń jest tu ważniejsza, niż szukasz.

Weapons matter less here than you're after.

Broń jest tu mniej ważna, niż szukasz.

There's almost no weapon here — and that's what you want.

Broni jest tu prawie nie ma — i dobrze, bo właśnie tego szukasz.

### Praca solo

There's room here for the solo work you're after.

Jest tu miejsce na pracę solo, której szukasz.

There's more solo work here than you need.

Pracy solo jest tu więcej, niż potrzebujesz.

There's less solo work here than you're after.

Pracy solo jest tu mniej, niż szukasz.

There's little solo work here — and that's what you want.

Pracy solo jest tu mało — i dobrze, bo właśnie tego szukasz.

### Partner

Partner work matters here about as much as you want.

Praca z partnerem jest tu mniej więcej tak ważna, jak chcesz.

There's more partner work here than you're after.

Pracy z partnerem jest tu więcej, niż szukasz.

There's less partner work here than you're after.

Pracy z partnerem jest tu mniej, niż szukasz.

There's little partner work here — and that's what you want.

Pracy z partnerem jest tu mało — i dobrze, bo właśnie tego szukasz.

### Kontakt

The amount of contact fits what you're after.

Poziom kontaktu pasuje do tego, czego szukasz.

The contact is harder than you want.

Kontakt jest mocniejszy, niż chcesz.

The contact is lighter than you want.

Kontakt jest lżejszy, niż chcesz.

There's little contact here — and that's what you want.

Kontaktu jest tu mało — i dobrze, bo właśnie tego szukasz.

### Zawody

There's about as much competition here as you want.

Zawodów jest tu mniej więcej tyle, ile chcesz.

Competition matters more here than you're after.

Zawody są tu ważniejsze, niż szukasz.

Competition matters less here than you're after.

Zawody są tu mniej ważne, niż szukasz.

There's little competition here — and that's what you want.

Zawodów jest tu mało — i dobrze, bo właśnie tego szukasz.

### Tradycja

There's about as much hall custom and tradition here as you want.

Zwyczajów i tradycji w sali jest tu mniej więcej tyle, ile chcesz.

There's more hall custom and tradition here than you're after.

Zwyczajów i tradycji w sali jest tu więcej, niż szukasz.

There's less hall custom and tradition here than you're after.

Zwyczajów i tradycji w sali jest tu mniej, niż szukasz.

There's little hall custom and tradition here — and that's what you want.

Zwyczajów i tradycji w sali jest tu mało — i dobrze, bo właśnie tego szukasz.

### Złożoność techniczna

The technical load fits what you're after.

Złożoność techniczna pasuje do tego, czego szukasz.

There's more technique here than you're after.

Techniki jest tu więcej, niż szukasz.

There's less technique here than you're after.

Techniki jest tu mniej, niż szukasz.

Technically it's simpler here — and that's what you want.

Technicznie jest tu prościej — i dobrze, bo właśnie tego szukasz.

Ta oś nie dostaje liczby z quizu. Zdania leżą w banku, ale ten quiz ich nie uruchamia.

### Obciążenie fizyczne

The physical demand is about what you're after.

Obciążenie ciała jest tu mniej więcej takie, jakiego szukasz.

The body is loaded harder here than you want.

Ciało jest tu obciążane mocniej, niż chcesz.

The body is loaded lighter here than you want.

Ciało jest tu obciążane lżej, niż chcesz.

The physical demand is low here — and that's what you want.

Obciążenia fizycznego jest tu mało — i dobrze, bo właśnie tego szukasz.

Ta oś też nie dostaje liczby z quizu.

### Wytrzymałość

Endurance matters here about as much as you want.

Wytrzymałość jest tu mniej więcej tak ważna, jak chcesz.

It takes more endurance here than you're after.

Wytrzymałości trzeba tu więcej, niż szukasz.

It takes less endurance here than you're after.

Wytrzymałości trzeba tu mniej, niż szukasz.

You don't need much endurance here — and that's what you want.

Nie trzeba jej tu wiele — i dobrze, bo właśnie tego szukasz.

### Zryw

The pace and the burst fit what you're after.

Tempo i zryw pasują do tego, czego szukasz.

There's more burst here than you want.

Jest tu więcej zrywu, niż chcesz.

There's less burst here than you want.

Jest tu mniej zrywu, niż chcesz.

There's little burst here — and that's what you want.

Zrywu jest tu mało — i dobrze, bo właśnie tego szukasz.

### Sprzęt

There's about as much kit here as you want.

Sprzętu jest tu mniej więcej tyle, ile chcesz.

There's more kit here than you need.

Sprzętu jest tu więcej, niż potrzebujesz.

There's less kit here than you need.

Sprzętu jest tu mniej, niż potrzebujesz.

There's little kit here — and that's what you want.

Sprzętu jest tu mało — i dobrze, bo właśnie tego szukasz.