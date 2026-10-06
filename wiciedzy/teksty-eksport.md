# wiciędze — teksty na stronie (obecny UI)

Wygenerowano: **2026-10-03 13:32 UTC** poleceniem `python manage.py export_wiciedzy_texts`.

Źródło: aktywne trasy w `wiciedzy/urls.py`, szablony z listy LIVE_TEMPLATES, modele `Style` (`active=True`), `PreferenceQuestion` (`active=True`), teksty generowane z `dimensions.py` / `display.py` (profil, porównanie, dopasowanie).

**Nie wchodzi:** `/wiciedze/quiz/`, archetyp, `joke_*` w katalogu, `_quick.html` (nigdzie nie renderowany), stary `teksty.md`.

**Sekcja 1** = to, co widzisz w treści strony (plus pasek i stopka). Opisy `<meta>` i tytuły karty są w **załączniku SEO** na końcu — nie na home.

---
## 1. Teksty widoczne w przeglądarce (PL/EN)

### Wspólne: nawigacja i stopka (każda strona)

- Marka: **wiciędze** (bez przełącznika języka)
- Przełącznik: **PL** / **EN**

**PL:** Przejdź do treści
**EN:** Skip to content

**PL:** Potraktuj to z dystansem, mordko. Sport jest spoko — rusz dupkę.
**EN:** Take it with a pinch of salt, pal. Sport's good — get moving.

### `/wiciedze/`
_Szablon:_ `home.html` — stałe napisy; nazwy stylów i opisy z sekcji 4.

**PL:** Siemasz na wiciędze, obczaj niżej.
**EN:** Hey, welcome to wiciędze, check it out below.

**PL:** Katalog
**EN:** Catalog

**PL:** Obczaj różne sporty i sztuki walki. Możesz je też porównywać.
**EN:** Check out all kinds of combat sports and martial arts. You can compare them too.

**PL:** Quizopasowanie
**EN:** Quizmatch

**PL:** Se poklikaj, a dostaniesz krótką listę stylów dopasowanych do Twoich odpowiedzi.
**EN:** Click around and you get a short list of styles matched to your answers.

### `/wiciedze/spis/`
_Szablon:_ `list.html` — stałe napisy; nazwy stylów i opisy z sekcji 4.

**PL:** Katalog
**EN:** Catalog

**PL:** Obczaj różne sporty i sztuki walki — możesz je też porównywać.
**EN:** Check out all kinds of combat sports and martial arts — you can compare them too.

**PL:** Se porównaj:
**EN:** Go on, compare:

**PL:** Pierwszy
**EN:** First

**PL:** {{ style.name_pl }}
**EN:** {{ style.name_en }}

**PL:** Drugi
**EN:** Second

**PL:** Porównaj
**EN:** Compare

**PL:** Wszystkie tagi
**EN:** All tags

**PL:** {{ tag.name_pl }}
**EN:** {{ tag.name_en }}

**PL:** {{ style.get_family_display }}
**EN:** {{ style.family_en }}

**PL:** {{ style.summary_pl }}
**EN:** {{ style.summary_en }}

**PL:** Żaden styl nie ma tego tagu.
**EN:** No style has this tag.

**PL:** Pokaż wszystkie
**EN:** Show all

### `/wiciedze/spis/<styl>/`
_Szablon:_ `detail.html` — stałe napisy; nazwy stylów i opisy z sekcji 4.

**PL:** {{ style.get_family_display }}
**EN:** {{ style.family_en }}

**PL:** {{ style.name_pl }}
**EN:** {{ style.name_en }}

**PL:** O stylu
**EN:** About

**PL:** {{ style.summary_pl }}
**EN:** {{ style.summary_en }}

**PL:** To nazwa zbiorcza, nie jeden regulamin, więc ten opis nie pasuje do każdej szkoły ani sali.
**EN:** It's an umbrella name, not one rule set, so this description doesn't fit every school or hall.

**PL:** {{ item.name_pl }}
**EN:** {{ item.name_en }}

**PL:** Pochodzenie
**EN:** Origin

**PL:** {{ style.origin_pl }}
**EN:** {{ style.origin_en }}

**PL:** Okres
**EN:** Period

**PL:** {{ style.period_pl }}
**EN:** {{ style.period_en }}

**PL:** Region
**EN:** Region

**PL:** Historia
**EN:** History

**PL:** Źródła się nie zgadzają.
**EN:** The sources don't agree.

**PL:** Opis jest krótszy, bo drugie źródło tylko wspomina o tym temacie.
**EN:** The description is shorter because the second source only mentions this topic.

**PL:** {{ style.history_pl }}
**EN:** {{ style.history_en }}

**PL:** Jak się walczy
**EN:** How it is fought

**PL:** {{ style.practice_pl }}
**EN:** {{ style.practice_en }}

**PL:** Charakter treningu
**EN:** Training character

**PL:** {{ row.pl }}
**EN:** {{ row.en }}

**PL:** {{ row.word_pl }}
**EN:** {{ row.word_en }}

**PL:** Pokaż pełny profil
**EN:** Show the full profile

**PL:** {{ group.pl }}
**EN:** {{ group.en }}

**PL:** Relacje
**EN:** Relations

**PL:** {{ relation.to_style.name_pl }}
**EN:** {{ relation.to_style.name_en }}

**PL:** {{ relation.note_pl }}
**EN:** {{ relation.note_en }}

**PL:** Fakty
**EN:** Facts

**PL:** {{ fact.text_pl }}
**EN:** {{ fact.text_en }}

**PL:** Późniejsza tradycja / legenda.
**EN:** Later tradition / legend.

**PL:** Źródła
**EN:** Sources

### `/wiciedze/test/`
_Szablon:_ `test.html` — stałe napisy; nazwy stylów i opisy z sekcji 4.

**PL:** Quizopasowanie
**EN:** Quizmatch

**PL:** Se poklikaj, a dostaniesz krótką listę stylów dopasowanych do Twoich odpowiedzi.
**EN:** Click around and you get a short list of styles matched to your answers.

**PL:** Zaznacz każdą skalę, oba wybory i sytuację. Dopiero wtedy pokaże się lista.
**EN:** Mark every scale, both choices and the situation. Only then does the list show up.

**PL:** Pytanie 1 z {{ total }}
**EN:** Question 1 of {{ total }}

**PL:** {{ question.text_pl }}
**EN:** {{ question.text_en }}

**PL:**  Wymagane.
**EN:**  Required.

**PL:** , wcale
**EN:** , not at all

**PL:** , bardzo
**EN:** , very much

**PL:** 1 oznacza wcale, 5 — bardzo.
**EN:** 1 means not at all, 5 — very much.

**PL:** {{ option.text_pl }}
**EN:** {{ option.text_en }}

**PL:** Pokaż listę
**EN:** Show the list

### `/wiciedze/dopasowanie/`
_Szablon:_ `match.html` — stałe napisy; nazwy stylów i opisy z sekcji 4.

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

**PL:** {{ row.style.name_pl }}
**EN:** {{ row.style.name_en }}

**PL:** {{ line.pl }}
**EN:** {{ line.en }}

**PL:** Blisko tego jest
**EN:** Next to this sits

**PL:** {{ other.name_pl }}
**EN:** {{ other.name_en }}

### `/wiciedze/porownaj/`
_Szablon:_ `compare_form.html` — stałe napisy; nazwy stylów i opisy z sekcji 4.

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

**PL:** {{ style.name_pl }}
**EN:** {{ style.name_en }}

**PL:** Drugi
**EN:** Second

### `/wiciedze/porownaj/<a>/<b>/`
_Szablon:_ `compare.html` — stałe napisy; nazwy stylów i opisy z sekcji 4.

**PL:** {{ left.name_pl }}
**EN:** {{ left.name_en }}

**PL:** {{ right.name_pl }}
**EN:** {{ right.name_en }}

**PL:** Historia i typ
**EN:** History and type

**PL:** To nazwa zbiorcza, nie jeden regulamin, więc ten opis nie pasuje do każdej szkoły ani sali.
**EN:** It's an umbrella name, not one rule set, so this description doesn't fit every school or hall.

**PL:** {{ item.name_pl }}
**EN:** {{ item.name_en }}

**PL:** {{ left.period_pl }}
**EN:** {{ left.period_en }}

**PL:** {{ left.history_pl }}
**EN:** {{ left.history_en }}

**PL:** {{ right.period_pl }}
**EN:** {{ right.period_en }}

**PL:** {{ right.history_pl }}
**EN:** {{ right.history_en }}

**PL:** Najważniejsze różnice
**EN:** Main differences

**PL:** {{ line.pl }}
**EN:** {{ line.en }}

**PL:** Techniki i trening
**EN:** Technique and training

**PL:** {{ group.pl }}
**EN:** {{ group.en }}

**PL:** {{ row.pl }}
**EN:** {{ row.en }}

**PL:** {{ row.left_pl }}
**EN:** {{ row.left_en }}

**PL:** {{ row.right_pl }}
**EN:** {{ row.right_en }}

**PL:** Psychologia / badania
**EN:** Psychology / research

**PL:** {{ study.finding_pl }}
**EN:** {{ study.finding_en }}

**PL:** {{ study.limitation_pl }}
**EN:** {{ study.limitation_en }}

### `/wiciedze/test/ (brak pytań)`
_Szablon:_ `empty.html` — stałe napisy; nazwy stylów i opisy z sekcji 4.

**PL:** Brak pytań
**EN:** No questions

**PL:** Na razie nie mam dla Ciebie pytań. Katalog dalej czeka.
**EN:** I don't have any questions for you right now. The catalog is still waiting.

**PL:** Katalog
**EN:** Catalog

### `404 w wiciędze`
_Szablon:_ `404.html` — stałe napisy; nazwy stylów i opisy z sekcji 4.

**PL:** Tu nic nie ma.
**EN:** There's nothing here.

**PL:** Adres nie pasuje do żadnej strony w wiciędze. Wróć na start albo obczaj katalog.
**EN:** The address doesn't match any page in wiciędze. Go back to the start or check out the catalog.

**PL:** Start
**EN:** Start

**PL:** Katalog
**EN:** Catalog

---
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

---
## 3. Typy stylu (StyleType)

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

---
## 4. Katalog stylów (`active=True`)

### boks — Boks

**PL:** Boks
**EN:** Boxing

Rodzina: **PL** Uderzenia | **EN** Striking
Zestaw: `core`

#### Streszczenie
**PL:** Boks to sport walki na pięści, rozgrywany w ringu i w rękawicach. W typowym boksie sportowym dozwolone ciosy pięścią kieruje się w określone strefy głowy i tułowia, zgodnie z regulaminem zawodów. W typowym regulaminie boksu sportowego nie ma też kopnięć ani kontynuowania walki w parterze.
**EN:** Boxing is a gloved fist sport fought in a ring. In typical sporting boxing, legal punches go to set zones of the head and torso, under the contest rules. Typical sporting boxing also has no kicks and no continuing the fight on the ground.

#### Pochodzenie
**PL:** Anglia, walki na gołe pięści
**EN:** England, bare-knuckle prize fights

#### Okres
**PL:** Nowoczesne reguły od 1867
**EN:** Modern rules from 1867

#### Region

Europa

#### Typy
**PL:** Sport walki
**EN:** Combat sport

#### Historia
**PL:** Współczesny boks wykształcił się w Anglii z wcześniejszych walk na gołe pięści. Reguły Queensberry z 1867 roku ujednoliciły model walki w rękawicach i rundach oraz zakazały zapasów. Z czasem wykształcił się z tego osobny sport, dziś zarówno olimpijski, jak i zawodowy.
**EN:** Modern boxing took shape in England out of earlier bare-knuckle fights. The 1867 Queensberry rules standardised gloved, round-based fighting and banned wrestling. Over time that became a sport in its own right, Olympic and professional.

#### Jak się walczy
**PL:** Na treningu ćwiczy się gardę, pracę nóg, uderzenia na łapach i worku oraz sparing. W obronie liczą się uniki, bloki i krótki klincz, który sędzia rozdziela.
**EN:** Training is the guard, footwork, punching on pads and the bag, and sparring. Defence means slips, blocks and a short clinch that the referee breaks.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: wysoko / high
- Pięści / Punches: wysoko / high
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: nisko / low
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: nisko / low
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: średnio / medium
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: wysoko / high
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: wysoko / high

Status zawodów (meta): **PL** Zawody | **EN** Competition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Fakty
**PL:** Reguły Queensberry z 1867 roku ujednoliciły model walki w rękawicach i rundach oraz zakazały zapasów. Wcześniejsze walki na gołe pięści dopuszczały więcej chwytów.
**EN:** The 1867 Queensberry rules standardised gloved, round-based fighting and banned wrestling. Earlier bare-knuckle bouts had allowed more holding.


#### Źródła (tytuły na stronie)
- Boxing — Encyclopaedia Britannica
- International Boxing Association — IBA


### muay-thai — Muay thai

**PL:** Muay thai
**EN:** Muay Thai

Rodzina: **PL** Uderzenia | **EN** Striking
Zestaw: `core`
Źródła się nie zgadzają: tak

#### Streszczenie
**PL:** Muay thai to tajski boks. Bywa popularyzatorsko nazywane sztuką ośmiu kończyn, ponieważ wykorzystuje pięści, łokcie, kolana i golenie. W klinczu można trzymać rywala i atakować kolanami, a w typowej walce sportowej nie ma parteru.
**EN:** Muay Thai is Thai boxing. It is often popularly called the art of eight limbs, because it uses fists, elbows, knees and shins. In the clinch you can hold your opponent and attack with knees, and in a typical sporting bout there is no ground fighting.

#### Pochodzenie
**PL:** Tajlandia
**EN:** Thailand

#### Okres
**PL:** Tradycja lokalna, sportowa forma w XX wieku
**EN:** Local tradition, sporting form in the 20th century

#### Region

Azja Południowo-Wschodnia

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** Korzenie muay thai wiążą się z tajskimi tradycjami walki, treningiem wojskowym i lokalnymi zawodami; szczegóły najdawniejszego rozwoju są przedmiotem dyskusji. W XX wieku rozwinęła się współczesna forma sportowa z ringiem, rundami i rękawicami, a rytuał ram muay pozostał częścią praktyki.
**EN:** The roots of Muay Thai are tied to Thai fighting traditions, military training and local contests; the earliest development is still debated. In the twentieth century a modern sporting form grew with the ring, rounds and gloves, and the ram muay ritual stayed part of the practice.

#### Jak się walczy
**PL:** Dużo tu kopnięć, klinczu i kolan. Na początku pracuje się na worku i tarczach, a technikę ćwiczy bez pełnej mocy.
**EN:** There are a lot of kicks, clinch work and knees. You start on the bag and the pads, and you practise technique without full power.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: wysoko / high
- Pięści / Punches: wysoko / high
- Kopnięcia / Kicks: wysoko / high
- Kolana / Knees: wysoko / high
- Łokcie / Elbows: wysoko / high

**Chwyt / Grappling**
- Chwyt / Grappling: średnio / medium
- Klincz / Clinch: wysoko / high
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: nisko / low
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: wysoko / high
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Zawody i tradycja | **EN** Competition and tradition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Muay Thai — Wikipedia contributors, CC BY-SA 4.0
- International Federation of Muaythai Associations — IFMA


### kickboxing — Kickboxing

**PL:** Kickboxing
**EN:** Kickboxing

Rodzina: **PL** Uderzenia | **EN** Striking
Zestaw: `core`

#### Streszczenie
**PL:** Kickboxing łączy w stójce pięści z kopnięciami. Zakres klinczu i dozwolonych kolan zależy od formuły. Walka nie jest kontynuowana w parterze.
**EN:** Kickboxing joins punches and kicks while standing. How much clinch and legal knees you get depends on the format. The fight is not continued on the ground.

#### Pochodzenie
**PL:** Japonia i Stany Zjednoczone, formuły pełnokontaktowe
**EN:** Japan and the United States, full-contact formats

#### Okres
**PL:** XX wiek
**EN:** 20th century

#### Region

Globalny

#### Typy
**PL:** Sport walki
**EN:** Combat sport

#### Historia
**PL:** W XX wieku japońskie i amerykańskie formuły pełnego kontaktu połączyły boks z kopnięciami wywodzącymi się między innymi z karate. Nazwa zaczęła obejmować różne sporty ringowe, więc kickboxing nie jest jedną dawną szkołą o jednym regulaminie.
**EN:** In the twentieth century Japanese and American full-contact formats joined boxing with kicks that came, among other things, from karate. The name came to cover different ring sports, so kickboxing is not one ancient school with one rulebook.

#### Jak się walczy
**PL:** Walczy się w stójce: kopnięcia okrężne, frontalne i niskie plus pięści. W obronie służy osłona, praca nóg i odskok.
**EN:** You stay standing: round kicks, front kicks and low kicks, plus punches. Defence is the shell, footwork and the step-out.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: wysoko / high
- Pięści / Punches: wysoko / high
- Kopnięcia / Kicks: wysoko / high
- Kolana / Knees: średnio / medium
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: nisko / low
- Klincz / Clinch: nisko / low
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: nisko / low
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: średnio / medium
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: wysoko / high
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Zawody | **EN** Competition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Kickboxing — Encyclopaedia Britannica
- World Association of Kickboxing Organizations — WAKO


### mma — MMA

**PL:** MMA
**EN:** Mixed martial arts

Rodzina: **PL** Mieszane | **EN** Mixed
Zestaw: `core`

#### Streszczenie
**PL:** MMA łączy stójkę i parter w jednej walce, w granicach regulaminu danej organizacji. To zestaw narzędzi i zasad, a nie jedna tradycyjna szkoła.
**EN:** MMA puts stand-up and the ground into one fight, inside a promotion's rules. It's a set of tools and rules, not one traditional school.

#### Pochodzenie
**PL:** Wiele starszych formuł, współczesna forma od lat 90.
**EN:** Many older formats, current form from the 1990s

#### Okres
**PL:** Współczesna forma od lat 90. XX wieku
**EN:** Current form from the 1990s

#### Region

Globalny

#### Typy
**PL:** Mieszane
**EN:** Hybrid

**PL:** Sport walki
**EN:** Combat sport

#### Historia
**PL:** Starsze poprzedniczki to między innymi vale tudo i japońskie formuły mieszane. Współczesna postać MMA ukształtowała się w latach dziewięćdziesiątych, gdy zaczęto porządkować zasady, sprzęt i ograniczenia. W historii rozwoju MMA ważne miejsce zajmuje też brazylijskie jiu-jitsu.
**EN:** Older predecessors include vale tudo and Japanese mixed formats. The current shape of MMA settled in the 1990s, when rules, kit and limits began to be tidied up. Brazilian jiu-jitsu also has an important place in how MMA developed.

#### Jak się walczy
**PL:** Trenuje się kilka rzeczy naraz: uderzenia, zapasy, zejście do parteru, kontrolę i obronę przed poddaniami.
**EN:** You train several things at once: striking, wrestling, the takedown, control and defence against submissions.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: wysoko / high
- Pięści / Punches: wysoko / high
- Kopnięcia / Kicks: wysoko / high
- Kolana / Knees: średnio / medium
- Łokcie / Elbows: średnio / medium

**Chwyt / Grappling**
- Chwyt / Grappling: wysoko / high
- Klincz / Clinch: wysoko / high
- Rzuty / Throws: średnio / medium
- Obalenia / Takedowns: wysoko / high
- Parter / Ground fighting: wysoko / high
- Poddania / Submissions: wysoko / high

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: nisko / low
- Złożoność techniczna / Technical complexity: wysoko / high
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: wysoko / high
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: wysoko / high

Status zawodów (meta): **PL** Zawody | **EN** Competition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Mixed martial arts — Encyclopaedia Britannica
- International Mixed Martial Arts Federation — IMMAF


### zapasy — Zapasy

**PL:** Zapasy
**EN:** Wrestling

Rodzina: **PL** Chwyty | **EN** Grappling
Zestaw: `core`

#### Streszczenie
**PL:** Zapasy sportowe polegają na obaleniu rywala, kontroli i zdobywaniu punktów lub uzyskaniu przewagi wystarczającej do zakończenia walki. Uderzeń nie ma. W stylu klasycznym nogi nie służą do atakowania poniżej pasa, a w wolnym można atakować nogi.
**EN:** Sport wrestling is about taking someone down, controlling them, and scoring or getting enough advantage to end the bout. There are no strikes. In Greco-Roman the legs are not used to attack below the waist, and in freestyle you can attack the legs.

#### Pochodzenie
**PL:** Wiele tradycji, sport olimpijski w dwóch stylach
**EN:** Many traditions, Olympic sport in two styles

#### Okres
**PL:** Sportowa forma z XIX i XX wieku
**EN:** Sporting form from the 19th and 20th centuries

#### Region

Globalny

#### Typy
**PL:** Sport walki
**EN:** Combat sport

#### Historia
**PL:** Zapasy są starsze niż współczesne regulaminy i występują w wielu kulturach. Wersja olimpijska ukształtowała się w XIX i XX wieku, rozdzielając się na styl klasyczny i wolny. Ten opis dotyczy zapasów sportowych, a nie wszystkich zapasów ludowych.
**EN:** Wrestling is older than modern rulebooks and appears in many cultures. The Olympic version settled in the nineteenth and twentieth centuries into Greco-Roman and freestyle. This entry covers sport wrestling, not every folk wrestling style.

#### Jak się walczy
**PL:** Schodzisz niżej, łapiesz za kark, ramię albo nogę i próbujesz sprowadzić rywala do parteru. Potem go kontrolujesz albo wstajesz do kolejnej akcji.
**EN:** You change level, catch the neck, an arm or a leg, and try to take the opponent down. Then you control them or stand up for the next shot.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: nisko / low
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: wysoko / high
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: średnio / medium
- Obalenia / Takedowns: wysoko / high
- Parter / Ground fighting: wysoko / high
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: średnio / medium
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: wysoko / high
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Zawody | **EN** Competition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Wrestling — Encyclopaedia Britannica
- United World Wrestling — UWW


### judo — Judo

**PL:** Judo
**EN:** Judo

Rodzina: **PL** Chwyty | **EN** Grappling
Zestaw: `core`

#### Streszczenie
**PL:** Judo to japońska sztuka walki w judogi. W sportowym judo zwycięstwo może przynieść między innymi rzut, unieruchomienie albo dozwolone poddanie, zależnie od regulaminu. Uderzeń nie ma w typowej walce sportowej.
**EN:** Judo is a Japanese art fought in a judogi. In sporting judo a win can come from a throw, a hold-down or a legal submission, depending on the rules. There are no strikes in a typical sporting bout.

#### Pochodzenie
**PL:** Japonia, Jigoro Kano
**EN:** Japan, Jigoro Kano

#### Okres
**PL:** Koniec XIX wieku
**EN:** Late 19th century

#### Region

Azja Wschodnia

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Sztuka walki
**EN:** Martial art

#### Historia
**PL:** Jigoro Kano ułożył judo pod koniec XIX wieku na bazie starszych szkół jujutsu, między innymi z myślą o edukacji i wychowaniu. Późniejszy sport wyczynowy zawęził część tego, co wolno na zawodach.
**EN:** Jigoro Kano arranged judo at the end of the nineteenth century out of older jujutsu schools, among other things with education in mind. Later competitive sport narrowed some of what is legal in contest.

#### Jak się walczy
**PL:** Chwytasz judogi przeciwnika, wytrącasz go z równowagi i rzucasz. Na ziemi możesz go unieruchomić albo szukać poddania dopuszczonego przez regulamin.
**EN:** You grip the opponent's judogi, break their balance and throw. On the ground you can hold them or look for a submission the rules allow.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: nisko / low
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: wysoko / high
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: wysoko / high
- Obalenia / Takedowns: wysoko / high
- Parter / Ground fighting: średnio / medium
- Poddania / Submissions: średnio / medium

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: wysoko / high
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: średnio / medium
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Zawody i tradycja | **EN** Competition and tradition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Judo — Encyclopaedia Britannica
- International Judo Federation — IJF


### bjj — Brazylijskie jiu-jitsu

**PL:** Brazylijskie jiu-jitsu
**EN:** Brazilian jiu-jitsu

Rodzina: **PL** Chwyty | **EN** Grappling
Zestaw: `core`

#### Streszczenie
**PL:** Brazylijskie jiu-jitsu (BJJ) szuka poddania rywala przez dźwignię albo duszenie. Większość pracy odbywa się w parterze, a w sportowym gi i no-gi uderzeń zwykle nie ma.
**EN:** Brazilian jiu-jitsu (BJJ) looks for a submission by a joint lock or a choke. Most of the work is on the ground, and sporting gi and no-gi usually have no strikes.

#### Pochodzenie
**PL:** Brazylia, XX wiek. Źródła wiążą początki z judo i jujutsu, które ćwiczył Maeda.
**EN:** Brazil, 20th century. Sources tie the start to judo and jujutsu practiced by Maeda.

#### Okres
**PL:** XX wiek
**EN:** 20th century

#### Region

Ameryka Południowa

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Sztuka walki
**EN:** Martial art

#### Historia
**PL:** Część opracowań wiąże początki z judo i jujutsu, które do Brazylii przywiózł Mitsuyo Maeda, oraz z późniejszą pracą rodziny Gracie nad parterem. Nie jest to jeden bezsporny rodowód, a dzisiejsze zawody BJJ to nie judo. Szczegóły rodzinnych opowieści bywają późniejszą tradycją.
**EN:** Some accounts tie the start to the judo and jujutsu Mitsuyo Maeda brought to Brazil, and to later Gracie work on the ground. That isn't one undisputed origin, and today's BJJ contests are not judo. Details of family stories are sometimes later tradition.

#### Jak się walczy
**PL:** Przechodzisz gardę, bierzesz plecy albo wchodzisz w dosiad i szukasz dźwigni lub duszenia. Sparingi opierają się na ciągłej pracy z partnerem.
**EN:** You pass the guard, take the back or mount, and look for a lock or a choke. Sparring is built around continuous work with a partner.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: nisko / low
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: wysoko / high
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: średnio / medium
- Obalenia / Takedowns: średnio / medium
- Parter / Ground fighting: wysoko / high
- Poddania / Submissions: wysoko / high

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: średnio / medium
- Złożoność techniczna / Technical complexity: wysoko / high
- Obciążenie fizyczne / Athletic demand: średnio / medium
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: średnio / medium
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Zawody | **EN** Competition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Relacje
- → Judo / Judo
**PL:** Część opracowań wiąże początki BJJ z judo i jujutsu, które ćwiczył Maeda. To nie jest jeden bezsporny rodowód, a dzisiejsze zawody BJJ to nie judo.
**EN:** Some accounts tie the start of BJJ to the judo and jujutsu Maeda practiced. That isn't one undisputed origin, and today's BJJ contests are not judo.

#### Źródła (tytuły na stronie)
- International Brazilian Jiu-Jitsu Federation — IBJJF
- Brazilian jiu-jitsu — Wikipedia contributors, CC BY-SA 4.0


### karate — Karate

**PL:** Karate
**EN:** Karate

Rodzina: **PL** Uderzenia | **EN** Striking
Zestaw: `core`
Nazwa zbiorcza (umbrella): tak

#### Streszczenie
**PL:** Karate to szeroka grupa okinawskich i japońskich szkół walki, których podstawą są uderzenia, kopnięcia, obrona i praca ciałem. Zakres rzutów, dźwigni, kata oraz treningu z bronią zależy od szkoły.
**EN:** Karate is a broad group of Okinawan and Japanese fighting schools, built around strikes, kicks, defence and body work. Throws, locks, kata and weapon training depend on the school.

#### Pochodzenie
**PL:** Okinawa, potem Japonia
**EN:** Okinawa, then Japan

#### Okres
**PL:** Tradycja okinawska, upowszechnienie w XX wieku
**EN:** Okinawan tradition, spread in the 20th century

#### Region

Azja Wschodnia

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** Na Okinawie lokalne metody zmieszały się z wpływami z Chin. W XX wieku Funakoshi i inni przenieśli karate do Japonii. Nazwa obejmuje wiele stylów, a kyokushin to tylko jeden z nich, nie całe karate.
**EN:** On Okinawa local methods mixed with Chinese influence. In the twentieth century Funakoshi and others carried karate to Japan. The name covers many styles, and Kyokushin is just one of them, not the whole of karate.

#### Jak się walczy
**PL:** Zależnie od szkoły najpierw jest pozycja i kata, potem kumite. W jednej szkole liczy się sportowe punktowanie, w innej kontakt, a w jeszcze innej przede wszystkim tradycja i zastosowania kata.
**EN:** Depending on the school, first comes the stance and the kata, then kumite. In one school sporting points count, in another contact, and in another the tradition and uses of kata.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: wysoko / high
- Pięści / Punches: wysoko / high
- Kopnięcia / Kicks: wysoko / high
- Kolana / Knees: średnio / medium
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: nisko / low
- Klincz / Clinch: nisko / low
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: nisko / low
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: wysoko / high
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: średnio / medium
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: wysoko / high
- Obciążenie fizyczne / Athletic demand: średnio / medium
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: średnio / medium
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Zawody i tradycja | **EN** Competition and tradition
Broń (meta): **PL** Broń opcjonalna | **EN** Optional weapon

#### Źródła (tytuły na stronie)
- Karate — Encyclopaedia Britannica
- World Karate Federation — WKF


### taekwondo — Taekwondo

**PL:** Taekwondo
**EN:** Taekwondo

Rodzina: **PL** Uderzenia | **EN** Striking
Zestaw: `core`
Źródła się nie zgadzają: tak

#### Streszczenie
**PL:** Taekwondo słynie z kopnięć, często wysokich i szybkich. W odmianie olimpijskiej World Taekwondo jest to sport punktowy w ochraniaczach, a w innych szkołach dochodzą między innymi formy, rozbijanie desek i elementy tradycyjnego treningu.
**EN:** Taekwondo is known for kicks, often high and fast. In the Olympic World Taekwondo form it is a points sport in body armour, and other schools add forms, board breaking and traditional training.

#### Pochodzenie
**PL:** Korea
**EN:** Korea

#### Okres
**PL:** XX wiek, sport olimpijski jako dyscyplina medalowa od 2000
**EN:** 20th century, Olympic medal sport from 2000

#### Region

Azja Wschodnia

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Sztuka walki
**EN:** Martial art

#### Historia
**PL:** Współczesne taekwondo ukształtowało się w Korei w XX wieku z kilku szkół. Źródła różnie opisują, na ile czerpie wprost ze starszych koreańskich sztuk. Sportowa forma World Taekwondo ma dziś własny, dokładnie określony regulamin.
**EN:** Modern taekwondo took shape in Korea in the twentieth century out of several schools. Sources describe differently how directly it draws on older Korean arts. The World Taekwondo sporting form now has its own, precisely defined rule set.

#### Jak się walczy
**PL:** Dużo tu kopnięć z dystansu, pracy nóg i sparingu w ochraniaczach. Pięści też są, ale to kopnięcia najmocniej nadają sportowej odmianie charakter.
**EN:** There are a lot of kicks from range, footwork and sparring in armour. Punches exist, but the kicks most strongly define the sporting form.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: wysoko / high
- Pięści / Punches: średnio / medium
- Kopnięcia / Kicks: wysoko / high
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: nisko / low
- Klincz / Clinch: nisko / low
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: nisko / low
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: średnio / medium
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: wysoko / high
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Zawody i tradycja | **EN** Competition and tradition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Taekwondo — Encyclopaedia Britannica
- World Taekwondo — World Taekwondo


### sumo — Sumo

**PL:** Sumo
**EN:** Sumo

Rodzina: **PL** Chwyty | **EN** Grappling
Zestaw: `core`

#### Streszczenie
**PL:** Sumo rozstrzyga się w kole: trzeba wypchnąć rywala albo sprawić, by dotknął ziemi czymś innym niż podeszwa stopy. Dozwolone są między innymi uderzenia otwartą dłonią, ale walki w parterze nie ma.
**EN:** Sumo is decided in a ring: you push the opponent out, or make them touch the ground with anything but the sole of the foot. Open-hand strikes, among other things, are allowed, but there's no ground fight.

#### Pochodzenie
**PL:** Japonia
**EN:** Japan

#### Okres
**PL:** Tradycja dworska i świątynna, zawodowy sport nowożytny
**EN:** Court and shrine tradition, modern professional sport

#### Region

Azja Wschodnia

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** Sumo ma w Japonii długą historię jako rytuał i widowisko, a zawodowa organizacja i ranking powstały później. Rytuał przed walką jest częścią praktyki, a nie ozdobą dorzuconą po drodze.
**EN:** Sumo has a long history in Japan as ritual and spectacle, and the professional organisation and the ranking came later. The pre-bout ritual is part of the practice, not a decoration added along the way.

#### Jak się walczy
**PL:** Niska pozycja, zderzenie, chwyt za mawashi i próba wypchnięcia albo rzutu. Trening jest ciężki i mocno opiera się na pracy z partnerem.
**EN:** A low stance, the charge, a grip on the mawashi, and an attempt to push out or throw. Training is heavy and leans hard on work with a partner.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: nisko / low
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: wysoko / high
- Klincz / Clinch: wysoko / high
- Rzuty / Throws: wysoko / high
- Obalenia / Takedowns: wysoko / high
- Parter / Ground fighting: średnio / medium
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Zawody i tradycja | **EN** Competition and tradition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Sumo — Encyclopaedia Britannica
- Nihon Sumo Kyokai — Japan Sumo Association


### sambo — Sambo

**PL:** Sambo
**EN:** Sambo

Rodzina: **PL** Mieszane | **EN** Mixed
Zestaw: `core`

#### Streszczenie
**PL:** Sambo sportowe obejmuje rzuty, obalenia i dźwignie, a combat sambo dodaje do tego uderzenia. To różne odmiany z własnymi regulaminami, rozwijane w ramach radzieckiego systemu szkoleniowego.
**EN:** Sport sambo covers throws, takedowns and locks, and combat sambo adds strikes. They are different forms with their own rules, developed inside a Soviet training system.

#### Pochodzenie
**PL:** Związek Radziecki
**EN:** Soviet Union

#### Okres
**PL:** Lata 20.–30. XX wieku
**EN:** 1920s–1930s

#### Region

Europa Wschodnia

#### Typy
**PL:** Mieszane
**EN:** Hybrid

**PL:** Sport walki
**EN:** Combat sport

#### Historia
**PL:** W Związku Radzieckim w pierwszej połowie XX wieku rozwijano system wykorzystujący elementy zapasów ludowych, judo, jujutsu i innych metod. Z czasem wyodrębniły się różne odmiany sambo i ich regulaminy.
**EN:** In the first half of the twentieth century the Soviet Union developed a system that used folk wrestling, judo, jujutsu and other methods. Over time different forms of sambo and their rule sets branched off.

#### Jak się walczy
**PL:** Kurtka, rzut, zejście na ziemię i dźwignia, a w combat sambo także ciosy w stójce.
**EN:** A jacket, a throw, the trip to the ground and a lock, and in combat sambo also strikes while standing.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: średnio / medium
- Pięści / Punches: średnio / medium
- Kopnięcia / Kicks: średnio / medium
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: wysoko / high
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: wysoko / high
- Obalenia / Takedowns: wysoko / high
- Parter / Ground fighting: wysoko / high
- Poddania / Submissions: wysoko / high

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: średnio / medium
- Złożoność techniczna / Technical complexity: wysoko / high
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: wysoko / high
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Zawody | **EN** Competition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Sambo (martial art) — Wikipedia contributors, CC BY-SA 4.0
- International Sambo Federation — FIAS


### wushu — Wushu / kung fu

**PL:** Wushu / kung fu
**EN:** Wushu / kung fu

Rodzina: **PL** Uderzenia | **EN** Striking
Zestaw: `core`
Nazwa zbiorcza (umbrella): tak
Źródła się nie zgadzają: tak

#### Streszczenie
**PL:** Wushu i kung fu to nazwy zbiorcze chińskich sztuk walki, a nie jeden styl. Są formy bez broni i z bronią, a osobno istnieje sanda, czyli współczesna walka sportowa. Ta karta dotyczy szerokiej grupy praktyk, a sanda ma własną.
**EN:** Wushu and kung fu are umbrella names for Chinese arts, not one style. There are empty-hand forms and weapon forms, and separately there is sanda, a modern sporting fight. This card is about a broad group of practices, and sanda has its own.

#### Pochodzenie
**PL:** Chiny, wiele szkół
**EN:** China, many schools

#### Okres
**PL:** Tradycje lokalne, nowoczesne wushu od XX wieku
**EN:** Local traditions, modern wushu from the 20th century

#### Region

Azja Wschodnia

#### Typy
**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** Poszczególne szkoły mają własne tradycje i opowieści. Nowoczesne wushu jako system zawodów i taolu ukształtowało się w XX wieku, więc nie da się uczciwie podać jednej daty powstania całego „kung fu”.
**EN:** Individual schools have their own traditions and stories. Modern wushu as a contest and taolu system took shape in the twentieth century, so there's no honest single date for the birth of all of kung fu.

#### Jak się walczy
**PL:** Zależnie od szkoły ćwiczy się formy, broń treningową i kondycję, a w odmianach sportowych także taolu albo sandę. Program może wyglądać zupełnie inaczej w tradycyjnej szkole i na sali sportowej.
**EN:** Depending on the school you practise forms, training weapons and conditioning, and in sporting forms also taolu or sanda. The programme can look completely different in a traditional school and in a sporting hall.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: wysoko / high
- Pięści / Punches: średnio / medium
- Kopnięcia / Kicks: wysoko / high
- Kolana / Knees: średnio / medium
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: średnio / medium
- Klincz / Clinch: nisko / low
- Rzuty / Throws: średnio / medium
- Obalenia / Takedowns: nisko / low
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: średnio / medium

**Trening / Training**
- Trening solo / Solo training: wysoko / high
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: średnio / medium
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: wysoko / high
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Zawody i tradycja | **EN** Competition and tradition
Broń (meta): **PL** Broń opcjonalna | **EN** Optional weapon

#### Źródła (tytuły na stronie)
- Kung fu — Encyclopaedia Britannica
- International Wushu Federation — IWUF


### sanda — Sanda

**PL:** Sanda
**EN:** Sanda

Rodzina: **PL** Mieszane | **EN** Mixed
Zestaw: `core`

#### Streszczenie
**PL:** Sanda to współczesna walka sportowa na platformie, obejmująca uderzenia, kopnięcia i rzuty. Jest związana historycznie i organizacyjnie z wushu, ale nie jest podstylem równym wszystkim tradycyjnym formom kung fu.
**EN:** Sanda is a modern sporting fight on a platform, covering strikes, kicks and throws. It is historically and organisationally tied to wushu, but it is not a substyle equal to every traditional kung fu form.

#### Pochodzenie
**PL:** Chiny, współczesny sport związany z wushu
**EN:** China, a contemporary sport tied to wushu

#### Okres
**PL:** XX wiek
**EN:** 20th century

#### Region

Azja Wschodnia

#### Typy
**PL:** Sport walki
**EN:** Combat sport

#### Historia
**PL:** Ukształtowała się w XX wieku jako współczesny sport walki rozwijany przy wushu. Związek z wushu nie oznacza, że każda tradycyjna szkoła kung fu jest sandą.
**EN:** It took shape in the twentieth century as a modern combat sport developed alongside wushu. The link with wushu does not mean every traditional kung fu school is sanda.

#### Jak się walczy
**PL:** Pięści, kopnięcia i rzuty. Wyjście poza platformę może być karane, a parter nie jest celem walki.
**EN:** Punches, kicks and throws. Stepping off the platform can be punished, and the ground is not the aim of the fight.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: wysoko / high
- Pięści / Punches: wysoko / high
- Kopnięcia / Kicks: wysoko / high
- Kolana / Knees: średnio / medium
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: średnio / medium
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: średnio / medium
- Obalenia / Takedowns: wysoko / high
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: średnio / medium
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: wysoko / high
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Zawody | **EN** Competition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Relacje
- → Wushu / kung fu / Wushu / kung fu
**PL:** Sanda to współczesny sport związany z wushu, a nie podstyl równy wszystkim tradycyjnym formom kung fu.
**EN:** Sanda is a contemporary sport tied to wushu, not a substyle equal to every traditional kung fu form.

#### Źródła (tytuły na stronie)
- International Wushu Federation — IWUF
- Sanda (sport) — Wikipedia contributors, CC BY-SA 4.0


### aikido — Aikido

**PL:** Aikido
**EN:** Aikido

Rodzina: **PL** Chwyty | **EN** Grappling
Zestaw: `core`

#### Streszczenie
**PL:** Aikido ćwiczy zejście z linii, rzuty i dźwignie, zwykle z partnerem, który podaje uchwyt. W większości głównych organizacji rywalizacja turniejowa nie jest centrum treningu, choć istnieją odmiany z zawodami lub randori. Broń treningowa to między innymi jo i bokken.
**EN:** Aikido practises getting off the line, throws and locks, usually with a partner who offers a grip. In most of the main organisations tournament fighting is not the centre of training, though there are forms with contests or randori. Training weapons include the jo and the bokken.

#### Pochodzenie
**PL:** Japonia, Morihei Ueshiba
**EN:** Japan, Morihei Ueshiba

#### Okres
**PL:** XX wiek
**EN:** 20th century

#### Region

Azja Wschodnia

#### Typy
**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** Morihei Ueshiba rozwijał aikido w XX wieku na bazie sztuk, które sam ćwiczył, w tym Daito-ryu. Późniejsze organizacje różnią się tempem, podejściem do broni i tym, czy w ogóle sparingują, więc jedna sala nie reprezentuje wszystkich.
**EN:** Morihei Ueshiba developed aikido in the twentieth century out of arts he himself trained, including Daito-ryu. Later organisations differ on pace, weapons and whether they spar at all, so one hall doesn't stand for all of them.

#### Jak się walczy
**PL:** Ćwiczy się formy w parach, upadki i pracę z bronią drewnianą. Kontakt bywa z góry ustalony, a w wielu szkołach nie jest to sparing na wynik.
**EN:** You practise paired forms, falling and work with a wooden weapon. Contact is often set in advance, and in many schools it is not sparring for a score.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: nisko / low
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: wysoko / high
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: wysoko / high
- Obalenia / Takedowns: średnio / medium
- Parter / Ground fighting: średnio / medium
- Poddania / Submissions: średnio / medium

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: średnio / medium
- Zawody / Competition: nisko / low
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: wysoko / high
- Obciążenie fizyczne / Athletic demand: średnio / medium
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: średnio / medium
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Praktyka tradycyjna | **EN** Traditional practice
Broń (meta): **PL** Broń treningowa | **EN** Training weapon

#### Źródła (tytuły na stronie)
- Aikido — Encyclopaedia Britannica
- Aikido — Wikipedia contributors, CC BY-SA 4.0


### krav-maga — Krav maga

**PL:** Krav maga
**EN:** Krav Maga

Rodzina: **PL** Mieszane | **EN** Mixed
Zestaw: `core`

#### Streszczenie
**PL:** Krav maga to system samoobrony, a nie jeden sportowy styl walki. Uczy reakcji na chwyt, cios i różne scenariusze zagrożenia. Nie ma jednego światowego regulaminu zawodów.
**EN:** Krav Maga is a self-defence system, not one sporting fighting style. It teaches reactions to a grab, a strike and different threat scenarios. There is no single world contest rule set.

#### Pochodzenie
**PL:** Izrael / Europa Środkowa, Imi Lichtenfeld
**EN:** Israel / Central Europe, Imi Lichtenfeld

#### Okres
**PL:** XX wiek
**EN:** 20th century

#### Region

Bliski Wschód

#### Typy
**PL:** Samoobrona
**EN:** Self-defence

#### Historia
**PL:** Krav maga wiąże się z Imim Lichtenfeldem i rozwojem systemu w XX wieku, najpierw w Europie Środkowej, a później w Izraelu. Późniejsze organizacje cywilne różnie rozwinęły program, więc sama nazwa nie gwarantuje jednej treści zajęć.
**EN:** Krav Maga is tied to Imi Lichtenfeld and to the system's development in the twentieth century, first in Central Europe, then in Israel. Later civilian organisations developed the curriculum differently, so the name alone doesn't guarantee one class content.

#### Jak się walczy
**PL:** Ćwiczy się scenariusze, pracę na tarczach i z partnerem, który stawia opór. Form ani zawodów nie traktuje się tu jako podstawy treningu.
**EN:** You practise scenarios, pad work and a partner who resists. Forms and contests are not treated as the base of training.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: wysoko / high
- Pięści / Punches: wysoko / high
- Kopnięcia / Kicks: średnio / medium
- Kolana / Knees: średnio / medium
- Łokcie / Elbows: średnio / medium

**Chwyt / Grappling**
- Chwyt / Grappling: średnio / medium
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: średnio / medium
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: nisko / low
- Tradycja / Tradition: nisko / low
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: średnio / medium
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: średnio / medium
- Sprzęt / Equipment: nisko / low

Status zawodów (meta): **PL** Bez zawodów | **EN** No competition
Broń (meta): **PL** Broń opcjonalna | **EN** Optional weapon

#### Źródła (tytuły na stronie)
- Krav Maga — Wikipedia contributors, CC BY-SA 4.0
- Martial art — Encyclopaedia Britannica


### hapkido — Hapkido

**PL:** Hapkido
**EN:** Hapkido

Rodzina: **PL** Mieszane | **EN** Mixed
Zestaw: `core`
Źródła się nie zgadzają: tak

#### Streszczenie
**PL:** Hapkido łączy dźwignie, rzuty, kopnięcia i elementy samoobrony. To nie taekwondo, a zawody nie są osią większości sal.
**EN:** Hapkido joins locks, throws, kicks and self-defence work. It's not taekwondo, and contests aren't the axis of most halls.

#### Pochodzenie
**PL:** Korea
**EN:** Korea

#### Okres
**PL:** XX wiek
**EN:** 20th century

#### Region

Azja Wschodnia

#### Typy
**PL:** Samoobrona
**EN:** Self-defence

**PL:** Sztuka walki
**EN:** Martial art

#### Historia
**PL:** Współczesne hapkido jest związane z Koreą i rozwojem organizacji w XX wieku. Opowieści o dokładnym rodowodzie różnią się między organizacjami, dlatego ta karta nie wskazuje jednego mistrza jako jedynego źródła.
**EN:** Modern hapkido is tied to Korea and to organisations that grew in the twentieth century. Stories of the exact lineage differ between organisations, so this card doesn't name one master as the only source.

#### Jak się walczy
**PL:** Ćwiczy się dźwignie na nadgarstek, upadki, kopnięcia i scenariusze z partnerem.
**EN:** You practise wrist locks, falling, kicks and scenarios with a partner.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: średnio / medium
- Pięści / Punches: średnio / medium
- Kopnięcia / Kicks: średnio / medium
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: wysoko / high
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: średnio / medium
- Obalenia / Takedowns: średnio / medium
- Parter / Ground fighting: średnio / medium
- Poddania / Submissions: średnio / medium

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: średnio / medium
- Zawody / Competition: średnio / medium
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: wysoko / high
- Obciążenie fizyczne / Athletic demand: średnio / medium
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: średnio / medium
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Praktyka tradycyjna | **EN** Traditional practice
Broń (meta): **PL** Broń opcjonalna | **EN** Optional weapon

#### Źródła (tytuły na stronie)
- Hapkido — Wikipedia contributors, CC BY-SA 4.0
- Martial art — Encyclopaedia Britannica


### savate — Savate

**PL:** Savate
**EN:** Savate

Rodzina: **PL** Uderzenia | **EN** Striking
Zestaw: `core`

#### Streszczenie
**PL:** Savate to francuski sport walki łączący pięści i kopnięcia, często wykonywane w specjalnych butach. Z savate historycznie wiążą się także odrębne praktyki walki laską, między innymi canne de combat.
**EN:** Savate is a French combat sport joining fists and kicks, often done in special shoes. Separate cane-fighting practices, including canne de combat, are also historically tied to savate.

#### Pochodzenie
**PL:** Francja
**EN:** France

#### Okres
**PL:** XIX wiek
**EN:** 19th century

#### Region

Europa

#### Typy
**PL:** Sport walki
**EN:** Combat sport

#### Historia
**PL:** W XIX wieku paryskie metody uliczne i salowe złożyły się w nauczaną sztukę, a później w sport. Z czasem powstały konkretne regulaminy i federacje. Praktyki walki laską rozwijały się obok savate, a nie jako po prostu jedna z jego współczesnych odmian.
**EN:** In the nineteenth century Parisian street and salon methods became a taught art, then a sport. Concrete rules and federations came later. Cane fighting grew alongside savate, not as simply one of its modern forms.

#### Jak się walczy
**PL:** Liczy się dystans, kopnięcia i pięści w rękawicach. Charakter jest sportowy i techniczny.
**EN:** It's about range, kicks and gloved fists. The character is sporting and technical.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: wysoko / high
- Pięści / Punches: wysoko / high
- Kopnięcia / Kicks: wysoko / high
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: nisko / low
- Klincz / Clinch: nisko / low
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: nisko / low
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: średnio / medium
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: średnio / medium
- Złożoność techniczna / Technical complexity: wysoko / high
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: wysoko / high
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: wysoko / high

Status zawodów (meta): **PL** Zawody | **EN** Competition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Savate — Wikipedia contributors, CC BY-SA 4.0
- Fédération Française de Savate — FFSavate


### capoeira — Capoeira

**PL:** Capoeira
**EN:** Capoeira

Rodzina: **PL** Uderzenia | **EN** Striking
Zestaw: `core`
Źródła się nie zgadzają: tak

#### Streszczenie
**PL:** Capoeira to afrobrazylijska gra łącząca ruch, kopnięcia, uniki i muzykę w kole, czyli roda. W zależności od grupy może mocniej stawiać na grę, akrobatykę, tradycję albo sparing, ale nie jest po prostu kickboxingiem.
**EN:** Capoeira is an Afro-Brazilian game joining movement, kicks, evasions and music in the circle, the roda. Depending on the group it can lean more on play, acrobatics, tradition or sparring, but it is not simply kickboxing.

#### Pochodzenie
**PL:** Brazylia
**EN:** Brazil

#### Okres
**PL:** Czasy niewoli oraz XIX i XX wiek
**EN:** Slavery era and the 19th–20th centuries

#### Region

Ameryka Południowa

#### Typy
**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** Ukształtowała się w Brazylii wśród zniewolonych Afrykanów i ich potomków. W części XIX i XX wieku była ścigana, a później weszła do szkół. Źródła różnią się w szczegółach dotyczących jej początków.
**EN:** It took shape in Brazil among enslaved Africans and their descendants. For part of the nineteenth and twentieth centuries it was outlawed, then it entered schools. Sources differ on the details of its beginnings.

#### Jak się walczy
**PL:** Bazą jest ginga, z której wychodzą kopnięcia, uniki i przejścia. Muzyka i rytm są częścią praktyki, a nie tylko tłem.
**EN:** The ginga is the base, and the kicks, evasions and transitions come out of it. Music and rhythm are part of the practice, not just background.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: wysoko / high
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: wysoko / high
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: nisko / low
- Klincz / Clinch: nisko / low
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: nisko / low
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: średnio / medium
- Zawody / Competition: średnio / medium
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: wysoko / high
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: wysoko / high
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Praktyka tradycyjna | **EN** Traditional practice
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Capoeira — Encyclopaedia Britannica
- Capoeira — Wikipedia contributors, CC BY-SA 4.0


### kendo — Kendo

**PL:** Kendo
**EN:** Kendo

Rodzina: **PL** Broń | **EN** Weapons
Zestaw: `core`

#### Streszczenie
**PL:** Kendo to japońska dyscyplina budō oparta na walce treningowym mieczem shinai w zbroi bogu. Punktowane są określone cięcia i pchnięcia. To nie jest walka ostrą kataną.
**EN:** Kendo is a Japanese budō discipline based on fighting with a training shinai in bogu armour. Specified cuts and thrusts score. It is not a fight with a sharp katana.

#### Pochodzenie
**PL:** Japonia, z ćwiczeń mieczem
**EN:** Japan, from sword practice

#### Okres
**PL:** Nowoczesna forma od XIX i XX wieku
**EN:** Modern form from the 19th–20th centuries

#### Region

Azja Wschodnia

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Z bronią
**EN:** Weapon-based

#### Historia
**PL:** Wyrosło z ćwiczeń kenjutsu. W XIX i XX wieku bambusowy miecz, zbroja, etykieta i ujednolicone zasady stworzyły współczesne kendo. Nie jest ono prostą rekonstrukcją dawnego kenjutsu.
**EN:** It grew out of kenjutsu practice. In the nineteenth and twentieth centuries the bamboo sword, the armour, etiquette and unified rules made modern kendo. It is not a simple reconstruction of old kenjutsu.

#### Jak się walczy
**PL:** Ćwiczy się pracę nóg, podstawowe cięcia i sparing w zbroi. Etykieta sali jest częścią treningu.
**EN:** You practise footwork, basic cuts and sparring in armour. Hall etiquette is part of the training.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: średnio / medium
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: nisko / low
- Klincz / Clinch: nisko / low
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: nisko / low
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: wysoko / high

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: średnio / medium
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: wysoko / high
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: wysoko / high
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: wysoko / high

Status zawodów (meta): **PL** Zawody i tradycja | **EN** Competition and tradition
Broń (meta): **PL** Broń treningowa | **EN** Training weapon

#### Źródła (tytuły na stronie)
- All Japan Kendo Federation — AJKF
- Kendo — Wikipedia contributors, CC BY-SA 4.0


### szermierka — Szermierka sportowa

**PL:** Szermierka sportowa
**EN:** Sport fencing

Rodzina: **PL** Broń | **EN** Weapons
Zestaw: `core`

#### Streszczenie
**PL:** Szermierka sportowa obejmuje floret, szpadę i szablę, a trafienia rejestruje aparatura elektryczna. Liczą się dystans, timing i trafienie zgodnie z zasadami konkretnej broni. We florecie i szabli obowiązuje konwencja pierwszeństwa, natomiast szpada ma inne zasady.
**EN:** Sport fencing covers foil, epee and sabre, and electrical kit records the touches. Distance, timing and a hit under that weapon's rules are what count. Foil and sabre use right of way; epee has different rules.

#### Pochodzenie
**PL:** Europa, pojedynki i sale szermiercze
**EN:** Europe, the duel and the salle

#### Okres
**PL:** Sportowa forma z XIX i XX wieku
**EN:** Sporting form, 19th–20th century

#### Region

Europa

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Z bronią
**EN:** Weapon-based

#### Historia
**PL:** Wyrosła z europejskiej tradycji broni białej i XIX-wiecznej sali szermierczej. Maska, sprzęt ochronny i elektryczne sędziowanie pomogły przekształcić ją w nowoczesny sport olimpijski.
**EN:** It grew out of the European bladed-weapon tradition and the nineteenth-century salle. The mask, protective kit and electrical judging helped turn it into a modern Olympic sport.

#### Jak się walczy
**PL:** Lekcja z trenerem, praca nóg, wypad i sparing na planszy.
**EN:** A lesson with a coach, footwork, the lunge and sparring on the piste.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: nisko / low
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: nisko / low
- Klincz / Clinch: nisko / low
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: nisko / low
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: wysoko / high

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: średnio / medium
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: średnio / medium
- Złożoność techniczna / Technical complexity: wysoko / high
- Obciążenie fizyczne / Athletic demand: średnio / medium
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: wysoko / high

Status zawodów (meta): **PL** Zawody | **EN** Competition
Broń (meta): **PL** Broń treningowa | **EN** Training weapon

#### Fakty
**PL:** W szermierce sportowej trafienie rejestruje aparatura elektryczna. HEMA próbuje odtworzyć techniki opisane w dawnych traktatach. To dwie różne praktyki.
**EN:** Sport fencing records a touch with electrical kit. HEMA tries to reconstruct techniques described in old treatises. They are two different practices.


#### Źródła (tytuły na stronie)
- Fencing — Encyclopaedia Britannica
- International Fencing Federation — FIE


### hema — HEMA

**PL:** HEMA
**EN:** HEMA

Rodzina: **PL** Broń | **EN** Weapons
Zestaw: `core`
Źródła się nie zgadzają: tak

#### Streszczenie
**PL:** HEMA to współczesna próba odtworzenia europejskich sztuk walki na podstawie historycznych traktatów: miecza długiego, rapiera, szpady i innych broni. Ćwiczy się tępą bronią i w ochraniaczach, więc nie jest to to samo co szermierka olimpijska.
**EN:** HEMA is a modern attempt to reconstruct European fighting arts from historical treatises: the longsword, the rapier, the smallsword and other weapons. You train with blunt weapons and protection, so it is not the same as Olympic fencing.

#### Pochodzenie
**PL:** Współczesna rekonstrukcja europejskich sztuk broni
**EN:** A modern reconstruction of European weapon arts

#### Okres
**PL:** Rekonstrukcja od końca XX wieku, źródła od średniowiecza
**EN:** Reconstruction from the late 20th century, sources from the Middle Ages

#### Region

Europa

#### Typy
**PL:** Rekonstrukcja historyczna
**EN:** Historical reconstruction

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Z bronią
**EN:** Weapon-based

#### Historia
**PL:** Same traktaty są historyczne, ale ruch, który dziś ćwiczy je w klubach i na zawodach, jest stosunkowo młody, głównie od końca XX wieku. Interpretacje tych samych źródeł bywają sporne. Kiedy tak jest, ta karta mówi wprost, że źródła się nie zgadzają.
**EN:** The treatises themselves are historical, but the movement that now trains them in clubs and contests is relatively young, mostly from the end of the twentieth century. Readings of the same sources are sometimes disputed. When that's the case, the card says plainly that the sources don't agree.

#### Jak się walczy
**PL:** Ćwiczy się według traktatów, pracuje w parach i wykonuje ćwiczenia z kontrolowanym kontaktem. Przy sparingu stosuje się broń treningową i ochraniacze dobrane do rodzaju broni oraz poziomu kontaktu.
**EN:** You drill from the treatises, work in pairs and do controlled-contact exercises. For sparring you use training weapons and protection matched to the weapon and the contact level.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: średnio / medium
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: średnio / medium
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: nisko / low
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: wysoko / high

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: średnio / medium
- Zawody / Competition: średnio / medium
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: wysoko / high
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: wysoko / high
- Eksplozywność / Explosiveness: średnio / medium
- Sprzęt / Equipment: wysoko / high

Status zawodów (meta): **PL** Zawody i tradycja | **EN** Competition and tradition
Broń (meta): **PL** Broń treningowa | **EN** Training weapon

#### Relacje
- → Szermierka sportowa / Sport fencing
**PL:** Obie praktyki pracują z europejską bronią białą, ale HEMA odtwarza techniki na podstawie historycznych traktatów, a szermierka sportowa ma trzy bronie i własne zasady. To nie jest ten sam trening.
**EN:** Both practices work with European bladed weapons, but HEMA reconstructs techniques from historical treatises, while sport fencing has three weapons and its own rules. It is not the same training.

#### Fakty
**PL:** W szermierce sportowej trafienie rejestruje aparatura elektryczna. HEMA próbuje odtworzyć techniki opisane w dawnych traktatach. To dwie różne praktyki.
**EN:** Sport fencing records a touch with electrical kit. HEMA tries to reconstruct techniques described in old treatises. They are two different practices.


#### Źródła (tytuły na stronie)
- HEMA Alliance — HEMA Alliance
- Historical European martial arts — Wikipedia contributors, CC BY-SA 4.0


### arnis — Arnis / kali / eskrima

**PL:** Arnis / kali / eskrima
**EN:** Arnis / kali / eskrima

Rodzina: **PL** Broń | **EN** Weapons
Zestaw: `core`
Nazwa zbiorcza (umbrella): tak
Źródła się nie zgadzają: tak

#### Streszczenie
**PL:** Arnis, kali i eskrima to nazwy używane dla różnych filipińskich sztuk walki. W wielu szkołach najważniejsze są kije, ale pojawiają się też nóż treningowy, broń długa i praca pustą ręką. To nie jedna szkoła i nie kendo.
**EN:** Arnis, kali and eskrima are names used for different Filipino arts. In many schools the sticks matter most, but a training knife, a long weapon and empty-hand work also appear. It is not one school and it is not kendo.

#### Pochodzenie
**PL:** Filipiny
**EN:** The Philippines

#### Okres
**PL:** Tradycje lokalne, nazwy nowożytne
**EN:** Local traditions, modern names

#### Region

Azja Południowo-Wschodnia

#### Typy
**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Z bronią
**EN:** Weapon-based

#### Historia
**PL:** Praktyki są filipińskie i bardzo różne lokalnie. Nazwy arnis, kali i eskrima bywają używane wymiennie, ale ich zakres zależy od regionu, szkoły i organizacji. Sportowy arnis ma własne zawody i regulaminy.
**EN:** The practices are Filipino and very different locally. The names arnis, kali and eskrima are sometimes used interchangeably, but their scope depends on the region, the school and the organisation. Sport arnis has its own contests and rules.

#### Jak się walczy
**PL:** Ćwiczy się drille kijem w parach, obiema rękami, czasem z nożem treningowym, a na sparing zakłada ochraniacze.
**EN:** You do paired stick drills with both hands, sometimes with a training knife, and you put protection on for sparring.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: średnio / medium
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: nisko / low
- Klincz / Clinch: nisko / low
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: nisko / low
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: wysoko / high

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: średnio / medium
- Zawody / Competition: średnio / medium
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: wysoko / high
- Obciążenie fizyczne / Athletic demand: średnio / medium
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: średnio / medium
- Sprzęt / Equipment: wysoko / high

Status zawodów (meta): **PL** Zawody i tradycja | **EN** Competition and tradition
Broń (meta): **PL** Broń główna | **EN** Weapon first

#### Źródła (tytuły na stronie)
- Arnis — Wikipedia contributors, CC BY-SA 4.0
- Martial art — Encyclopaedia Britannica


### silat — Silat

**PL:** Silat
**EN:** Silat

Rodzina: **PL** Mieszane | **EN** Mixed
Zestaw: `core`
Nazwa zbiorcza (umbrella): tak

#### Streszczenie
**PL:** Silat to szeroka nazwa obejmująca wiele sztuk walki z Indonezji, Malezji i okolic: postawy, uderzenia, rzuty, pracę w zwarciu i czasem broń. Pencak silat ma własny, sportowy system zasad.
**EN:** Silat is a broad name covering many arts from Indonesia, Malaysia and nearby: stances, strikes, throws, close-range work and sometimes a weapon. Pencak silat has its own sporting rule system.

#### Pochodzenie
**PL:** Archipelag Malajski
**EN:** The Malay archipelago

#### Okres
**PL:** Tradycje lokalne, sport pencak silat w XX wieku
**EN:** Local traditions, pencak silat sport in the 20th century

#### Region

Azja Południowo-Wschodnia

#### Typy
**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** Nie ma jednej daty ani jednej szkoły, która reprezentowałaby całe silat. PERSILAT jest jedną z głównych organizacji międzynarodowych związanych z pencak silat i jego systemem sportowym. Tradycyjne szkoły i ich linie przekazu mogą wyglądać bardzo różnie.
**EN:** There is no single date and no single school that stands for all of silat. PERSILAT is one of the main international organisations tied to pencak silat and its sporting system. Traditional schools and their lineages can look very different.

#### Jak się walczy
**PL:** Ćwiczy się formy i pracę w parach, a w odmianach sportowych walkę albo układ. Broń zależy od szkoły.
**EN:** You practise forms and paired work, and in sporting forms a match or a routine. Weapons depend on the school.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: wysoko / high
- Pięści / Punches: średnio / medium
- Kopnięcia / Kicks: wysoko / high
- Kolana / Knees: średnio / medium
- Łokcie / Elbows: średnio / medium

**Chwyt / Grappling**
- Chwyt / Grappling: średnio / medium
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: średnio / medium
- Obalenia / Takedowns: średnio / medium
- Parter / Ground fighting: średnio / medium
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: średnio / medium

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: średnio / medium
- Zawody / Competition: średnio / medium
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: wysoko / high
- Obciążenie fizyczne / Athletic demand: średnio / medium
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: średnio / medium
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Zawody i tradycja | **EN** Competition and tradition
Broń (meta): **PL** Broń opcjonalna | **EN** Optional weapon

#### Źródła (tytuły na stronie)
- Pencak silat — Wikipedia contributors, CC BY-SA 4.0
- Traditions of Pencak Silat — UNESCO


### lethwei — Lethwei

**PL:** Lethwei
**EN:** Lethwei

Rodzina: **PL** Uderzenia | **EN** Striking
Zestaw: `core`

#### Streszczenie
**PL:** Lethwei to birmański boks wykorzystujący pięści, nogi, kolana, łokcie, a w niektórych regulaminach także uderzenia głową. W części formuł walczy się bez klasycznych rękawic. To nie muay thai, choć oba style używają podobnego zestawu narzędzi.
**EN:** Lethwei is Burmese boxing using fists, legs, knees, elbows and, in some rule sets, headbutts. In some formats it is fought without classic gloves. It is not Muay Thai, even though both styles use a similar set of tools.

#### Pochodzenie
**PL:** Mjanma
**EN:** Myanmar

#### Okres
**PL:** Tradycja lokalna, współczesne gale XX–XXI wiek
**EN:** Local tradition, modern cards in the 20th–21st centuries

#### Region

Azja Południowo-Wschodnia

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** Praktyka jest birmańska, a współczesne gale i federacje są znacznie młodsze od lokalnych tradycji walki. Podobieństwo do muay thai nie oznacza, że są to te same sporty.
**EN:** The practice is Burmese, and modern cards and federations are much younger than the local fighting traditions. Looking like Muay Thai does not mean they are the same sports.

#### Jak się walczy
**PL:** Twarda stójka, kolana, łokcie i — zależnie od regulaminu — uderzenia głową. Kontakt jest wysoki, a sprzętu ochronnego może być mniej niż w wielu formułach kickboxingu.
**EN:** A hard stand-up with knees, elbows and — depending on the rules — headbutts. Contact is high, and there may be less protective kit than in many kickboxing formats.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: wysoko / high
- Pięści / Punches: wysoko / high
- Kopnięcia / Kicks: wysoko / high
- Kolana / Knees: wysoko / high
- Łokcie / Elbows: wysoko / high

**Chwyt / Grappling**
- Chwyt / Grappling: średnio / medium
- Klincz / Clinch: wysoko / high
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: nisko / low
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: wysoko / high
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Zawody | **EN** Competition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Lethwei — Wikipedia contributors, CC BY-SA 4.0
- Myanmar — Encyclopaedia Britannica


### kyokushin — Kyokushin

**PL:** Kyokushin
**EN:** Kyokushin karate

Rodzina: **PL** Uderzenia | **EN** Striking
Zestaw: `core`

#### Streszczenie
**PL:** Kyokushin to pełnokontaktowy styl karate. W klasycznych i wielu współczesnych formułach knock-down ciosy pięścią na głowę są zakazane, a kopnięcia na głowę dozwolone. Szczegóły zależą jednak od organizacji i regulaminu.
**EN:** Kyokushin is a full-contact karate style. In classic and many modern knockdown formats punches to the head are illegal and kicks to the head are allowed. The details still depend on the organisation and the rules.

#### Pochodzenie
**PL:** Japonia, Masutatsu Oyama, w obrębie karate
**EN:** Japan, Masutatsu Oyama, inside karate

#### Okres
**PL:** Połowa XX wieku
**EN:** Mid 20th century

#### Region

Azja Wschodnia

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Sztuka walki
**EN:** Martial art

#### Historia
**PL:** Masutatsu Oyama założył kyokushin w połowie XX wieku jako twardą odmianę karate, a po jego śmierci organizacje zaczęły się dzielić. Kyokushin pozostaje odmianą karate, a nie osobną tradycją spoza karate.
**EN:** Masutatsu Oyama founded Kyokushin in the mid twentieth century as a hard form of karate, and organisations began to split after his death. Kyokushin remains a form of karate, not a tradition from outside karate.

#### Jak się walczy
**PL:** Ćwiczy się kihon, kata i kumite z kontaktem. Osią są kondycja i sparing, nie tylko forma.
**EN:** You practise kihon, kata and kumite with contact. Conditioning and sparring are the axis, not the form alone.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: wysoko / high
- Pięści / Punches: wysoko / high
- Kopnięcia / Kicks: wysoko / high
- Kolana / Knees: średnio / medium
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: nisko / low
- Klincz / Clinch: nisko / low
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: nisko / low
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: wysoko / high
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Zawody | **EN** Competition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Relacje
- → Karate / Karate
**PL:** Kyokushin to pełnokontaktowa odmiana karate, a nie osobna tradycja spoza karate.
**EN:** Kyokushin is a full-contact style of karate, not a tradition from outside karate.

#### Źródła (tytuły na stronie)
- Kyokushin — Wikipedia contributors, CC BY-SA 4.0
- Karate — Encyclopaedia Britannica


### wing-chun — Wing chun

**PL:** Wing chun
**EN:** Wing Chun

Rodzina: **PL** Uderzenia | **EN** Striking
Zestaw: `core`

#### Streszczenie
**PL:** Wing chun to południowochińska sztuka walki krótkiego dystansu: struktura, proste uderzenia i chi sao, czyli „klejące ręce”. Opowieść o założycielce należy do tradycji szkoły, a nie do udokumentowanej biografii.
**EN:** Wing Chun is a southern Chinese short-range art: structure, straight strikes and chi sao, the sticking hands. The story of a founding woman belongs to school tradition, not to a documented biography.

#### Pochodzenie
**PL:** Południowe Chiny
**EN:** Southern China

#### Okres
**PL:** Tradycja południowochińska, popularyzacja w XX wieku
**EN:** Southern Chinese tradition, popularised in the 20th century

#### Region

Azja Wschodnia

#### Typy
**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** Praktyka wiąże się z południowymi Chinami i XX-wiecznym nauczaniem, w tym linią Ip Mana. Legenda o Ng Mui i Yim Wing-chun należy do późniejszej tradycji szkoły i tak ją tutaj oznaczam.
**EN:** The practice is tied to southern China and to twentieth-century teaching, including the Ip Man line. The legend of Ng Mui and Yim Wing-chun belongs to the school's later tradition, and that's how I mark it.

#### Jak się walczy
**PL:** Ćwiczy się formy na drewnianym manekinie, chi sao i uderzenia z bliska. Sparing zależy od sali.
**EN:** You practise forms on the wooden dummy, chi sao and close strikes. Sparring depends on the hall.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: wysoko / high
- Pięści / Punches: wysoko / high
- Kopnięcia / Kicks: średnio / medium
- Kolana / Knees: nisko / low
- Łokcie / Elbows: średnio / medium

**Chwyt / Grappling**
- Chwyt / Grappling: średnio / medium
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: nisko / low
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: wysoko / high
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: średnio / medium
- Zawody / Competition: nisko / low
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: wysoko / high
- Obciążenie fizyczne / Athletic demand: średnio / medium
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: średnio / medium
- Sprzęt / Equipment: nisko / low

Status zawodów (meta): **PL** Praktyka tradycyjna | **EN** Traditional practice
Broń (meta): **PL** Broń opcjonalna | **EN** Optional weapon

#### Fakty
**PL:** Opowieść o Ng Mui i Yim Wing-chun należy do tradycji szkoły wing chun, a nie do udokumentowanej historii, na której można oprzeć dokładną datę powstania stylu.
**EN:** The story of Ng Mui and Yim Wing-chun belongs to Wing Chun school tradition, not to documented history you can use to pin down an exact founding date.

_Późniejsza tradycja / legenda._

#### Źródła (tytuły na stronie)
- Wing Chun — Wikipedia contributors, CC BY-SA 4.0
- Kung fu — Encyclopaedia Britannica


### jeet-kune-do — Jeet kune do

**PL:** Jeet kune do
**EN:** Jeet Kune Do

Rodzina: **PL** Mieszane | **EN** Mixed
Zestaw: `core`
Źródła się nie zgadzają: tak

#### Streszczenie
**PL:** Jeet kune do to podejście Bruce'a Lee: brać to, co działa, bez jednego zamkniętego katalogu form. Nie jest to federacja sportowa ani styl z jednym regulaminem turniejowym.
**EN:** Jeet Kune Do is Bruce Lee's approach: take what works, without one closed catalogue of forms. It is not a sport federation and not a style with one tournament rulebook.

#### Pochodzenie
**PL:** Stany Zjednoczone, Bruce Lee
**EN:** United States, Bruce Lee

#### Okres
**PL:** Lata 60. XX wieku
**EN:** 1960s

#### Region

Ameryka Północna

#### Typy
**PL:** Mieszane
**EN:** Hybrid

**PL:** Sztuka walki
**EN:** Martial art

#### Historia
**PL:** Lee rozwijał i opisywał JKD w latach sześćdziesiątych, wychodząc poza wcześniejsze doświadczenia z wing chun. Po jego śmierci uczniowie różnie interpretowali, czy JKD ma być zamkniętym zestawem technik, czy raczej sposobem dalszego poszukiwania.
**EN:** Lee developed and described JKD in the 1960s, moving beyond his earlier Wing Chun work. After his death, students read differently whether JKD should be a closed set of techniques or a way of searching further.

#### Jak się walczy
**PL:** Ćwiczy się ze sprzętem, sparinguje i łączy uderzenia, klincz oraz proste obalenia, zależnie od nauczyciela.
**EN:** You train with kit, spar, and mix strikes, clinch and simple takedowns, depending on the teacher.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: wysoko / high
- Pięści / Punches: wysoko / high
- Kopnięcia / Kicks: wysoko / high
- Kolana / Knees: średnio / medium
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: średnio / medium
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: średnio / medium
- Parter / Ground fighting: średnio / medium
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: średnio / medium
- Zawody / Competition: nisko / low
- Tradycja / Tradition: średnio / medium
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: średnio / medium
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: średnio / medium
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Bez zawodów | **EN** No competition
Broń (meta): **PL** Broń opcjonalna | **EN** Optional weapon

#### Źródła (tytuły na stronie)
- Jeet Kune Do — Wikipedia contributors, CC BY-SA 4.0
- Bruce Lee — Encyclopaedia Britannica


### jujutsu — Jujutsu

**PL:** Jujutsu
**EN:** Jujutsu

Rodzina: **PL** Chwyty | **EN** Grappling
Zestaw: `core`
Nazwa zbiorcza (umbrella): tak

#### Streszczenie
**PL:** Jujutsu to szeroka nazwa obejmująca japońskie szkoły chwytów, rzutów i dźwigni, czasem także z bronią. Z jego tradycji wywodzi się między innymi judo, a BJJ jest historycznie wiązane z judo i jujutsu. Nie są jednak całym jujutsu, a jedna sala „ju-jitsu” może uczyć czegoś zupełnie innego niż inna.
**EN:** Jujutsu is a broad name covering Japanese schools of gripping, throwing and locking, sometimes also with a weapon. Judo comes from that tradition, among other things, and BJJ is historically tied to judo and jujutsu. They are not the whole of jujutsu, and one ju-jitsu hall may teach something quite different from another.

#### Pochodzenie
**PL:** Japonia, wiele szkół
**EN:** Japan, many schools

#### Okres
**PL:** Szkoły od okresu wczesnonowożytnego, nazwa zbiorcza
**EN:** Schools from the early modern period, an umbrella name

#### Region

Azja Wschodnia

#### Typy
**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** Historyczne koryu mają własne tradycje, a nowoczesne organizacje używają tej samej nazwy dla różnych programów, między innymi samoobrony. Dlatego ta karta opisuje nazwę zbiorczą, a nie jeden konkretny system.
**EN:** Historical koryu have their own traditions, and modern organisations use the same name for different programmes, including self-defence. That's why this card describes an umbrella name, not one specific system.

#### Jak się walczy
**PL:** Rzuty, dźwignie, upadki i praca w parach. Uderzenia i broń zależą od szkoły.
**EN:** Throws, locks, falling and paired work. Strikes and weapons depend on the school.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: średnio / medium
- Pięści / Punches: średnio / medium
- Kopnięcia / Kicks: średnio / medium
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: wysoko / high
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: wysoko / high
- Obalenia / Takedowns: średnio / medium
- Parter / Ground fighting: średnio / medium
- Poddania / Submissions: wysoko / high

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: średnio / medium
- Zawody / Competition: średnio / medium
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: wysoko / high
- Obciążenie fizyczne / Athletic demand: średnio / medium
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: średnio / medium
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Praktyka tradycyjna | **EN** Traditional practice
Broń (meta): **PL** Broń opcjonalna | **EN** Optional weapon

#### Źródła (tytuły na stronie)
- Jujutsu — Encyclopaedia Britannica
- Jujutsu — Wikipedia contributors, CC BY-SA 4.0


### pankration — Pankration

**PL:** Pankration
**EN:** Pankration

Rodzina: **PL** Mieszane | **EN** Mixed
Zestaw: `core`

#### Streszczenie
**PL:** Starożytny pankration łączył uderzenia i zapasy. Współczesne sporty używające tej nazwy są nowymi formami inspirowanymi źródłami, a nie praktyką działającą nieprzerwanie od igrzysk antycznych.
**EN:** Ancient pankration joined strikes and wrestling. Modern sports using that name are new forms inspired by the sources, not a practice running unbroken since the ancient games.

#### Pochodzenie
**PL:** Starożytna Grecja
**EN:** Ancient Greece

#### Okres
**PL:** Starożytność; współczesne zawody to rekonstrukcja sportowa
**EN:** Antiquity; modern contests are a sporting reconstruction

#### Region

Europa

#### Typy
**PL:** Rekonstrukcja historyczna
**EN:** Historical reconstruction

**PL:** Sport walki
**EN:** Combat sport

#### Historia
**PL:** W źródłach greckich pankration był konkurencją igrzysk, ale między starożytnością a współczesnymi federacjami jest ogromna przerwa. Dzisiejszych zawodów nie należy opisywać tak, jakby obowiązywał w nich ten sam regulamin co w Olimpii.
**EN:** In Greek sources pankration was a contest of the games, but between antiquity and modern federations there is a huge gap. Today's contests should not be described as if they used the same rules as Olympia.

#### Jak się walczy
**PL:** Współczesne odmiany, tam gdzie istnieją, łączą uderzenia i chwyty według własnych regulaminów. Starożytnego sparingu nie da się odtworzyć jeden do jednego.
**EN:** Modern forms, where they exist, join strikes and grappling under their own rules. Ancient sparring can't be rebuilt one to one.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: wysoko / high
- Pięści / Punches: wysoko / high
- Kopnięcia / Kicks: średnio / medium
- Kolana / Knees: średnio / medium
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: wysoko / high
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: średnio / medium
- Obalenia / Takedowns: średnio / medium
- Parter / Ground fighting: średnio / medium
- Poddania / Submissions: średnio / medium

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: nisko / low
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: średnio / medium
- Tradycja / Tradition: średnio / medium
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: wysoko / high
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: nisko / low

Status zawodów (meta): **PL** Rekonstrukcja | **EN** Reconstruction
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Pankration — Encyclopaedia Britannica
- Pankration — Wikipedia contributors, CC BY-SA 4.0


### shuai-jiao — Shuai jiao

**PL:** Shuai jiao
**EN:** Shuai jiao

Rodzina: **PL** Chwyty | **EN** Grappling
Zestaw: `core`

#### Streszczenie
**PL:** Shuai jiao to chińskie zapasy w kurtce, w których głównym celem jest rzut. Uderzenia nie są ich osią, a praktyka należy do chińskich sztuk chwytu, nie do sandy jako sportu uderzanego.
**EN:** Shuai jiao is Chinese jacket wrestling whose main aim is the throw. Strikes are not its axis, and the practice belongs with Chinese grappling arts, not with sanda as a striking sport.

#### Pochodzenie
**PL:** Chiny
**EN:** China

#### Okres
**PL:** Tradycja zapasów, sportowa forma nowożytna
**EN:** A wrestling tradition, modern sporting form

#### Region

Azja Wschodnia

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** Zapasy w Chinach mają długie i niejednolite dzieje. Nazwa shuai jiao oraz współczesne zawody to nowsza rama dla tej praktyki, której nie przypisuję jednej legendarnej daty.
**EN:** Wrestling in China has a long and uneven history. The name shuai jiao and the modern contests are a later frame for that practice, and I don't assign it one legendary date.

#### Jak się walczy
**PL:** Kurtka, wejście i rzut. Potrzebny jest partner, a w parterze się nie zostaje.
**EN:** A jacket, an entry and a throw. A partner is required, and the ground is not where you stay.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: nisko / low
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: wysoko / high
- Klincz / Clinch: wysoko / high
- Rzuty / Throws: wysoko / high
- Obalenia / Takedowns: wysoko / high
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Zawody i tradycja | **EN** Competition and tradition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Shuai jiao — Wikipedia contributors, CC BY-SA 4.0
- Kung fu — Encyclopaedia Britannica


### bokh — Bökh

**PL:** Bökh
**EN:** Bökh

Rodzina: **PL** Chwyty | **EN** Grappling
Zestaw: `golden`

#### Streszczenie
**PL:** Bökh to mongolskie zapasy związane z festiwalem Naadam. O wyniku decyduje określony rodzaj upadku zgodnie z lokalnymi zasadami. Strój i rytuał są częścią widowiska, a nie dodatkiem.
**EN:** Bökh is Mongolian wrestling tied to the Naadam festival. A specified kind of fall under local rules decides the bout. The costume and the ritual are part of the spectacle, not an extra.

#### Pochodzenie
**PL:** Mongolia
**EN:** Mongolia

#### Okres
**PL:** Święto naadam, tradycja zapasów
**EN:** The Naadam festival, a wrestling tradition

#### Region

Azja Środkowa

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** Zapasy są jedną z trzech tradycyjnych konkurencji Naadamu, obok łucznictwa i wyścigów konnych. Bökh jest jedną z tych konkurencji, a nie nazwą całego święta.
**EN:** Wrestling is one of the three traditional contests of Naadam, beside archery and horse racing. Bökh is one of those contests, not the name of the whole festival.

#### Jak się walczy
**PL:** Chwyta się za kurtkę albo ciało, zależnie od lokalnej odmiany, i próbuje doprowadzić do uznanego upadku. Uderzeń nie ma.
**EN:** You grip the jacket or the body, depending on the local variant, and try to force a recognised fall. There are no strikes.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: nisko / low
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: wysoko / high
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: wysoko / high
- Obalenia / Takedowns: wysoko / high
- Parter / Ground fighting: średnio / medium
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: nisko / low
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: średnio / medium
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Praktyka tradycyjna | **EN** Traditional practice
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Fakty
**PL:** Naadam w Mongolii to zapasy, łucznictwo i wyścigi konne. Bökh jest jedną z tych trzech konkurencji, a nie całym świętem.
**EN:** Naadam in Mongolia is wrestling, archery and horse racing. Bökh is one of those three contests, not the whole festival.


#### Źródła (tytuły na stronie)
- Mongolian wrestling — Wikipedia contributors, CC BY-SA 4.0
- Mongolia — Encyclopaedia Britannica


### ssireum — Ssireum

**PL:** Ssireum
**EN:** Ssireum

Rodzina: **PL** Chwyty | **EN** Grappling
Zestaw: `golden`

#### Streszczenie
**PL:** Ssireum to koreańskie zapasy z pasem satba, w których celem jest powalenie rywala. To nie taekwondo.
**EN:** Ssireum is Korean wrestling with the satba belt, and the aim is to put the opponent down. It is not taekwondo.

#### Pochodzenie
**PL:** Korea
**EN:** Korea

#### Okres
**PL:** Tradycja zapasów, współczesne zawody
**EN:** A wrestling tradition, modern contests

#### Region

Azja Wschodnia

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** Wiejskie i dworskie zapasy w Korei dostały w XX wieku bardziej ujednoliconą formę zawodów i ring z piaskiem. UNESCO wpisało ssireum na listę dziedzictwa niematerialnego, co opisuje znaczenie tradycji, a nie skuteczność sportową.
**EN:** Village and court wrestling in Korea gained a more unified contest form and a sand ring in the twentieth century. UNESCO inscribed ssireum as intangible heritage, which describes the weight of a tradition, not sporting effectiveness.

#### Jak się walczy
**PL:** Chwyt za satba i rzut — liczy się siła, równowaga i praca biodrem, nie cios.
**EN:** A grip on the satba and a throw — what counts is strength, balance and hip work, not a punch.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: nisko / low
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: wysoko / high
- Klincz / Clinch: wysoko / high
- Rzuty / Throws: wysoko / high
- Obalenia / Takedowns: średnio / medium
- Parter / Ground fighting: średnio / medium
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: nisko / low
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Zawody i tradycja | **EN** Competition and tradition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Ssireum — Wikipedia contributors, CC BY-SA 4.0
- Traditional Korean wrestling (Ssirum/Ssireum) — UNESCO


### chidaoba — Chidaoba

**PL:** Chidaoba
**EN:** Chidaoba

Rodzina: **PL** Chwyty | **EN** Grappling
Zestaw: `golden`

#### Streszczenie
**PL:** Chidaoba to gruzińskie zapasy w kurtce, w których główną rolę odgrywają chwyt i rzut. Taniec przed walką jest częścią tradycji.
**EN:** Chidaoba is Georgian jacket wrestling in which the grip and the throw do the main work. The dance before the bout is part of the tradition.

#### Pochodzenie
**PL:** Gruzja
**EN:** Georgia

#### Okres
**PL:** Tradycja zapasów
**EN:** A wrestling tradition

#### Region

Kaukaz

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** To gruzińska tradycja zapaśnicza, którą UNESCO opisuje jako dziedzictwo niematerialne. Nie należy utożsamiać jej z judo tylko dlatego, że oba style używają kurtki.
**EN:** It is a Georgian wrestling tradition, described by UNESCO as intangible heritage. It should not be treated as judo just because both styles use a jacket.

#### Jak się walczy
**PL:** Kurtka, chwyt i rzut na plecy albo bok, zgodnie z zasadami danego starcia.
**EN:** A jacket, a grip and a throw to the back or the side, under the rules of that bout.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: nisko / low
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: wysoko / high
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: wysoko / high
- Obalenia / Takedowns: średnio / medium
- Parter / Ground fighting: średnio / medium
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: nisko / low
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: średnio / medium
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Praktyka tradycyjna | **EN** Traditional practice
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Chidaoba, wrestling in Georgia — UNESCO
- Chidaoba — Wikipedia contributors, CC BY-SA 4.0


### laamb — Laamb

**PL:** Laamb
**EN:** Laamb

Rodzina: **PL** Mieszane | **EN** Mixed
Zestaw: `golden`

#### Streszczenie
**PL:** Laamb to senegalskie zapasy. W odmianie z uderzeniami, nazywanej frappe, dochodzą ciosy, ale istnieje też wersja bez nich. Szczegóły zależą od odmiany i regulaminu.
**EN:** Laamb is Senegalese wrestling. In the striking form, called frappe, blows are added, but a version without them also exists. The details depend on the form and the rules.

#### Pochodzenie
**PL:** Senegal
**EN:** Senegal

#### Okres
**PL:** Tradycja zapasów, współczesne gale
**EN:** A wrestling tradition, modern cards

#### Region

Afryka Zachodnia

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** Zapasy są w Senegalu ważnym widowiskiem. Współczesne gale z frappe są nowszą warstwą tej tradycji, a samej praktyki nie da się sprowadzić do jednego regulaminu.
**EN:** Wrestling is a major spectacle in Senegal. Modern cards with frappe are a newer layer of that tradition, and the practice itself cannot be reduced to one rule set.

#### Jak się walczy
**PL:** Wejście, chwyt i rzut, a we frappe także uderzenia. Rytuał przed walką może być rozbudowany.
**EN:** An entry, a grip and a throw, and in frappe also strikes. The ritual before the bout can be elaborate.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: średnio / medium
- Pięści / Punches: średnio / medium
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: wysoko / high
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: średnio / medium
- Obalenia / Takedowns: wysoko / high
- Parter / Ground fighting: średnio / medium
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: nisko / low
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: nisko / low

Status zawodów (meta): **PL** Zawody i tradycja | **EN** Competition and tradition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Senegalese wrestling — Wikipedia contributors, CC BY-SA 4.0
- Senegal — Encyclopaedia Britannica


### glima — Glíma

**PL:** Glíma
**EN:** Glíma

Rodzina: **PL** Chwyty | **EN** Grappling
Zestaw: `golden`

#### Streszczenie
**PL:** Glíma to tradycyjna islandzka forma zapasów, często rozgrywana w pasie i z charakterystycznym ruchem po kole. Wygrywa rzut, a uderzeń nie ma.
**EN:** Glíma is a traditional Icelandic form of wrestling, often fought with a belt and with a distinctive circling movement. A throw wins, and there are no strikes.

#### Pochodzenie
**PL:** Islandia
**EN:** Iceland

#### Okres
**PL:** Tradycja zapasów, opisana też w XIX i XX wieku
**EN:** A wrestling tradition, also described in the 19th–20th centuries

#### Region

Europa Północna

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** Glíma wiąże się z tradycją nordycką i jest ważnym elementem islandzkiego dziedzictwa sportowego. O średniowieczu wiemy mniej niż o samej praktyce zapasów, dlatego opowieści o nieprzerwanej linii od czasów wikingów nie traktuję jako dowodu ciągłości.
**EN:** Glíma is tied to a Nordic tradition and is an important part of Icelandic sporting heritage. Medieval details are thinner than the wrestling practice itself, so I don't treat stories of an unbroken line from the Viking age as proof of continuity.

#### Jak się walczy
**PL:** Pas, chwyt i rzut w ruchu. Potrzebny jest partner.
**EN:** A belt, a grip and a throw on the move. A partner is required.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: nisko / low
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: wysoko / high
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: wysoko / high
- Obalenia / Takedowns: średnio / medium
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: średnio / medium
- Zawody / Competition: średnio / medium
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: średnio / medium
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Praktyka tradycyjna | **EN** Traditional practice
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Glíma — Wikipedia contributors, CC BY-SA 4.0
- Iceland — Encyclopaedia Britannica


### alysh — Alysh

**PL:** Alysh
**EN:** Alysh

Rodzina: **PL** Chwyty | **EN** Grappling
Zestaw: `golden`

#### Streszczenie
**PL:** Alysh to zapasy na pasie z Azji Środkowej: chwyt idzie w pas, a rzut kończy akcję.
**EN:** Alysh is belt wrestling from Central Asia: the grip goes to the belt, and a throw ends the action.

#### Pochodzenie
**PL:** Azja Środkowa, zwłaszcza Kirgistan
**EN:** Central Asia, especially Kyrgyzstan

#### Okres
**PL:** Tradycja zapasów na pasie
**EN:** A belt-wrestling tradition

#### Region

Azja Środkowa

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** Należy do rodziny środkowoazjatyckich zapasów ludowych, a międzynarodowe zawody są nowszą sportową ramą. Nie mylę alysh z kurash: oba pochodzą z tego regionu, ale mają inne zasady chwytu i walki.
**EN:** It belongs with Central Asian folk wrestling, and international contests are a newer sporting frame. I don't confuse alysh with kurash: both are from the region, but they have different grip and fighting rules.

#### Jak się walczy
**PL:** Pas, wejście biodrem i rzut, bez uderzeń.
**EN:** A belt, a hip entry and a throw, with no strikes.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: nisko / low
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: wysoko / high
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: wysoko / high
- Obalenia / Takedowns: średnio / medium
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: nisko / low
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: średnio / medium
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Zawody i tradycja | **EN** Competition and tradition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Alysh — Wikipedia contributors, CC BY-SA 4.0
- United World Wrestling — UWW


### kurash — Kurash

**PL:** Kurash
**EN:** Kurash

Rodzina: **PL** Chwyty | **EN** Grappling
Zestaw: `golden`

#### Streszczenie
**PL:** Kurash to zapasy z Azji Środkowej, w których rzut daje punkty, a walka pozostaje w stójce. Współczesne zasady chwytu i punktowania określa regulamin federacji.
**EN:** Kurash is Central Asian wrestling in which a throw scores and the fight stays standing. Modern grip and scoring rules are set by the federation rulebook.

#### Pochodzenie
**PL:** Uzbekistan i Azja Środkowa
**EN:** Uzbekistan and Central Asia

#### Okres
**PL:** Tradycja zapasów, federacja międzynarodowa w XX wieku
**EN:** A wrestling tradition, an international federation in the 20th century

#### Region

Azja Środkowa

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** Sama praktyka jest starsza niż współczesna federacja międzynarodowa. Organizacje sportowe z końca XX wieku stworzyły bardziej jednolity system zawodów z kategoriami i regulaminem, ale tradycyjne zapasy mają szerszą historię.
**EN:** The practice itself is older than the modern international federation. Sporting organisations from the end of the twentieth century made a more unified contest system with categories and a rulebook, but traditional wrestling has a wider history.

#### Jak się walczy
**PL:** Chwyt za strój zgodnie z regulaminem, wejście i rzut. Parter nie jest celem.
**EN:** A grip on the jacket under the rules, an entry and a throw. The ground is not the aim.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: nisko / low
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: wysoko / high
- Klincz / Clinch: średnio / medium
- Rzuty / Throws: wysoko / high
- Obalenia / Takedowns: średnio / medium
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: nisko / low
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: wysoko / high
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Zawody i tradycja | **EN** Competition and tradition
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- International Kurash Association — IKA
- Kurash — Wikipedia contributors, CC BY-SA 4.0


### gatka — Gatka

**PL:** Gatka
**EN:** Gatka

Rodzina: **PL** Broń | **EN** Weapons
Zestaw: `golden`

#### Streszczenie
**PL:** Gatka to pendżabska sztuka walki bronią, związana z tradycją sikhijską: kij, tarcza i inne rodzaje broni treningowej. Typowe są pokazy i ćwiczenia w parach.
**EN:** Gatka is a Punjabi weapon art tied to Sikh tradition: stick, shield and other training weapons. Demonstrations and paired drills are typical.

#### Pochodzenie
**PL:** Pendżab
**EN:** Punjab

#### Okres
**PL:** Tradycja sikhijska, odnowa w XX wieku
**EN:** A Sikh tradition, a revival in the 20th century

#### Region

Azja Południowa

#### Typy
**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Z bronią
**EN:** Weapon-based

#### Historia
**PL:** Łączy się z historią sikhów. Współczesne akademie są częścią odnowy tradycji, a nie prostą kontynuacją jednego, niezmiennego regulaminu turniejowego. Na treningu używa się broni treningowej, nie ostrej.
**EN:** It is tied to Sikh history. Modern academies are part of a revival of the tradition, not a simple continuation of one unchanging tournament rulebook. Training uses training weapons, not sharp ones.

#### Jak się walczy
**PL:** Ćwiczy się formy z kijem i pracuje w parach, zwykle z odpowiednimi ochraniaczami. Charakter jest tradycyjny.
**EN:** You practise stick forms and work in pairs, usually with suitable protection. The character is traditional.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: średnio / medium
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: nisko / low
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: nisko / low
- Klincz / Clinch: nisko / low
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: nisko / low
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: wysoko / high

**Trening / Training**
- Trening solo / Solo training: wysoko / high
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: średnio / medium
- Zawody / Competition: nisko / low
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: średnio / medium
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: średnio / medium
- Sprzęt / Equipment: wysoko / high

Status zawodów (meta): **PL** Praktyka tradycyjna | **EN** Traditional practice
Broń (meta): **PL** Broń treningowa | **EN** Training weapon

#### Źródła (tytuły na stronie)
- Gatka — Wikipedia contributors, CC BY-SA 4.0
- Sikhism — Encyclopaedia Britannica


### kalaripayattu — Kalaripayattu

**PL:** Kalaripayattu
**EN:** Kalaripayattu

Rodzina: **PL** Mieszane | **EN** Mixed
Zestaw: `golden`
Źródła się nie zgadzają: tak

#### Streszczenie
**PL:** Kalaripayattu to sztuka walki z Kerali: ćwiczy się ciało, formy oraz broń treningową. Zakres broni zależy od tradycji i szkoły; często używa się broni drewnianej. Nie jest to sport olimpijski.
**EN:** Kalaripayattu is a fighting art from Kerala: you train the body, forms and training weapons. Which weapons you use depends on the tradition and the school; wooden weapons are common. It is not an Olympic sport.

#### Pochodzenie
**PL:** Kerala, Indie
**EN:** Kerala, India

#### Okres
**PL:** Tradycja keralijska
**EN:** A Kerala tradition

#### Region

Azja Południowa

#### Typy
**PL:** Sztuka walki
**EN:** Martial art

**PL:** Tradycyjne
**EN:** Traditional

**PL:** Z bronią
**EN:** Weapon-based

#### Historia
**PL:** Tradycja jest południowoindyjska. Opowieści o bardzo dawnym pochodzeniu należą do szkół i nie wszystkie da się sprawdzić tak samo jak współczesny regulamin, dlatego nie podaję jednej starożytnej daty jako faktu.
**EN:** The tradition is South Indian. Stories of a very ancient origin belong to the schools, and not all of them can be checked the way a modern rulebook can, which is why I don't give a single ancient date as fact.

#### Jak się walczy
**PL:** Rozgrzewka, kopnięcia, formy i praca z bronią treningową. W części tradycji pojawia się także praca z ciałem i olejowanie.
**EN:** Warm-up, kicks, forms and work with a training weapon. In part of the tradition there is also body work and oiling.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: średnio / medium
- Pięści / Punches: nisko / low
- Kopnięcia / Kicks: wysoko / high
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: średnio / medium
- Klincz / Clinch: nisko / low
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: nisko / low
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: wysoko / high

**Trening / Training**
- Trening solo / Solo training: wysoko / high
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: średnio / medium
- Zawody / Competition: nisko / low
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: wysoko / high
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: średnio / medium
- Sprzęt / Equipment: średnio / medium

Status zawodów (meta): **PL** Praktyka tradycyjna | **EN** Traditional practice
Broń (meta): **PL** Broń treningowa | **EN** Training weapon

#### Źródła (tytuły na stronie)
- Kalaripayattu — Wikipedia contributors, CC BY-SA 4.0
- Kerala — Encyclopaedia Britannica


### dambe — Dambe

**PL:** Dambe
**EN:** Dambe

Rodzina: **PL** Uderzenia | **EN** Striking
Zestaw: `golden`

#### Streszczenie
**PL:** Dambe to styl walki wywodzący się z tradycji ludu Hausa. Tradycyjnie jedna ręka jest owijana w charakterystyczny sposób, a w walce pojawiają się też kopnięcia. To coś innego niż boks w rękawicach.
**EN:** Dambe is a fighting style that comes from Hausa tradition. Traditionally one hand is wrapped in a distinctive way, and kicks also appear in the fight. It is something different from gloved boxing.

#### Pochodzenie
**PL:** Lud Hausa, Afryka Zachodnia
**EN:** The Hausa people, West Africa

#### Okres
**PL:** Tradycja walki pięścią i kopnięciem
**EN:** A fist-and-kick fighting tradition

#### Region

Afryka Zachodnia

#### Typy
**PL:** Sport walki
**EN:** Combat sport

**PL:** Tradycyjne
**EN:** Traditional

#### Historia
**PL:** Dambe wiąże się z tradycją Hausa, historycznie także z określonymi grupami zawodowymi i pokazami. Współczesne wydarzenia mogą zmieniać zabezpieczenia, sposób sędziowania i inne szczegóły, więc nie każdy współczesny pojedynek wygląda identycznie jak tradycyjne starcie.
**EN:** Dambe is tied to Hausa tradition, historically also to particular occupational groups and to shows. Modern events can change protection, judging and other details, so not every modern bout looks identical to a traditional fight.

#### Jak się walczy
**PL:** Walczy się z owiniętą pięścią, w gardzie, z kopnięciami. Kontakt jest częścią tradycyjnego starcia.
**EN:** You fight with a wrapped fist, in a guard, with kicks. Contact is part of the traditional bout.

#### Profil treningu (słowa na stronie szczegółu)

**Uderzenia / Striking**
- Uderzenia / Striking: wysoko / high
- Pięści / Punches: wysoko / high
- Kopnięcia / Kicks: średnio / medium
- Kolana / Knees: nisko / low
- Łokcie / Elbows: nisko / low

**Chwyt / Grappling**
- Chwyt / Grappling: nisko / low
- Klincz / Clinch: nisko / low
- Rzuty / Throws: nisko / low
- Obalenia / Takedowns: nisko / low
- Parter / Ground fighting: nisko / low
- Poddania / Submissions: nisko / low

**Broń / Weapons**
- Broń / Weapons: nisko / low

**Trening / Training**
- Trening solo / Solo training: średnio / medium
- Praca z partnerem / Partner work: wysoko / high
- Kontakt / Contact: wysoko / high
- Zawody / Competition: średnio / medium
- Tradycja / Tradition: wysoko / high
- Złożoność techniczna / Technical complexity: średnio / medium
- Obciążenie fizyczne / Athletic demand: wysoko / high
- Wytrzymałość / Endurance: średnio / medium
- Eksplozywność / Explosiveness: wysoko / high
- Sprzęt / Equipment: nisko / low

Status zawodów (meta): **PL** Praktyka tradycyjna | **EN** Traditional practice
Broń (meta): **PL** Bez broni | **EN** No weapon

#### Źródła (tytuły na stronie)
- Dambe — Wikipedia contributors, CC BY-SA 4.0
- Hausa — Encyclopaedia Britannica


---
## 5. Quizopasowanie — pytania (`active=True`)

### [scale]
**PL:** Jak bardzo chcesz uderzać?
**EN:** How much do you want to strike?


### [scale]
**PL:** Jak bardzo chcesz chwytać i trzymać?
**EN:** How much do you want to grapple and hold?


### [scale]
**PL:** Jak bardzo chcesz walczyć w parterze?
**EN:** How much do you want to fight on the ground?


### [scale]
**PL:** Jak bardzo chcesz mieć broń na treningu?
**EN:** How much do you want a weapon in training?


### [scale]
**PL:** Jak bardzo chcesz kopać?
**EN:** How much do you want to kick?


### [scale]
**PL:** Jak mocny ma być kontakt?
**EN:** How hard should the contact be?


### [scale]
**PL:** Jak bardzo chcesz startować w zawodach?
**EN:** How much do you want to compete?


### [scale]
**PL:** Jak ważne są dla Ciebie formy i zwyczaje w sali?
**EN:** How much do forms and hall customs matter to you?


### [ab]
**PL:** Wolisz ćwiczyć sam czy z partnerem?
**EN:** Would you rather train alone, or with a partner?

- **PL:** Sam, forma albo worek.
  **EN:** Alone, with a form or a bag.
- **PL:** Z partnerem, który się rusza.
  **EN:** With a partner who moves.

### [ab]
**PL:** Wolisz zostać daleko czy wejść blisko?
**EN:** Would you rather stay far, or step in close?

- **PL:** Z daleka, niech noga robi robotę.
  **EN:** At a distance, let the leg do the work.
- **PL:** Z bliska, klincz albo chwyt.
  **EN:** Up close, a clinch or a grip.

### [situation]
**PL:** Na treningu dochodzi do zwarcia. Co ma być dalej?
**EN:** In training it comes to close range. What should happen next?

- **PL:** Rzut.
  **EN:** A throw.
- **PL:** Schodzicie do parteru i szukacie poddania.
  **EN:** You go to the ground and look for a submission.
- **PL:** Uderzenie i odskok.
  **EN:** A strike and a step out.

### [multi]
**PL:** Zaznacz, co ma być w Twoim tygodniu treningowym. Możesz wybrać kilka rzeczy naraz, a jeśli nic z tego Cię nie rusza, zostaw puste.
**EN:** Tick what should be in your training week. You can pick several, or leave it blank if none of it matters to you.

- **PL:** Kolana i łokcie.
  **EN:** Knees and elbows.
- **PL:** Zbroja albo maska.
  **EN:** Armour or a mask.
- **PL:** Rękawice.
  **EN:** Gloves.
- **PL:** Wytrzymałość, długie rundy.
  **EN:** Endurance, long rounds.
- **PL:** Szybkie, mocne wejście.
  **EN:** An explosive entry.
- **PL:** Nic z tego.
  **EN:** None of these.

---
## 6. Badania (Study) — widoczne przy porównaniu

---
## 7. Szablony tekstów dopasowania i porównania (`dimensions.py`)

### Poziomy profilu
**PL:** nisko
**EN:** low

**PL:** średnio
**EN:** medium

**PL:** wysoko
**EN:** high

### REASON_COPY (plus/minus na liście dopasowania)

**athletic_demand** — plus:
**PL:** Obciążenie ciała jest tu mniej więcej takie, jakiego szukasz.
**EN:** The physical demand is about what you're after.

minus (styl wyżej):
**PL:** Ciało jest tu obciążane mocniej, niż chcesz.
**EN:** The body is loaded harder here than you want.

minus (użytkownik wyżej):
**PL:** Ciało jest tu obciążane lżej, niż chcesz.
**EN:** The body is loaded lighter here than you want.

**clinch** — plus:
**PL:** Walka w zwarciu jest tu mniej więcej tak ważna, jak chcesz.
**EN:** Close-range work matters here about as much as you want.

minus (styl wyżej):
**PL:** Zwarcia jest tu więcej, niż szukasz.
**EN:** There's more close-range work here than you're after.

minus (użytkownik wyżej):
**PL:** Zwarcia jest tu mniej, niż szukasz.
**EN:** There's less close-range work here than you're after.

**competition_level** — plus:
**PL:** Zawodów jest tu mniej więcej tyle, ile chcesz.
**EN:** There's about as much competition here as you want.

minus (styl wyżej):
**PL:** Zawody są tu ważniejsze, niż szukasz.
**EN:** Competition matters more here than you're after.

minus (użytkownik wyżej):
**PL:** Zawody są tu mniej ważne, niż szukasz.
**EN:** Competition matters less here than you're after.

**contact_level** — plus:
**PL:** Poziom kontaktu pasuje do tego, czego szukasz.
**EN:** The amount of contact fits what you're after.

minus (styl wyżej):
**PL:** Kontakt jest mocniejszy, niż chcesz.
**EN:** The contact is harder than you want.

minus (użytkownik wyżej):
**PL:** Kontakt jest lżejszy, niż chcesz.
**EN:** The contact is lighter than you want.

**elbows** — plus:
**PL:** Łokcie są tu mniej więcej tak ważne, jak chcesz.
**EN:** Elbows matter here about as much as you want.

minus (styl wyżej):
**PL:** Łokcie liczą się tu bardziej, niż szukasz.
**EN:** Elbows matter more here than you're after.

minus (użytkownik wyżej):
**PL:** Łokcie liczą się tu mniej, niż szukasz.
**EN:** Elbows matter less here than you're after.

**endurance_demand** — plus:
**PL:** Wytrzymałość jest tu mniej więcej tak ważna, jak chcesz.
**EN:** Endurance matters here about as much as you want.

minus (styl wyżej):
**PL:** Wytrzymałości trzeba tu więcej, niż szukasz.
**EN:** It takes more endurance here than you're after.

minus (użytkownik wyżej):
**PL:** Wytrzymałości trzeba tu mniej, niż szukasz.
**EN:** It takes less endurance here than you're after.

**equipment_required** — plus:
**PL:** Sprzętu jest tu mniej więcej tyle, ile chcesz.
**EN:** There's about as much kit here as you want.

minus (styl wyżej):
**PL:** Sprzętu jest tu więcej, niż potrzebujesz.
**EN:** There's more kit here than you need.

minus (użytkownik wyżej):
**PL:** Sprzętu jest tu mniej, niż potrzebujesz.
**EN:** There's less kit here than you need.

**explosiveness** — plus:
**PL:** Tempo i zryw pasują do tego, czego szukasz.
**EN:** The pace and the burst fit what you're after.

minus (styl wyżej):
**PL:** Jest tu więcej zrywu, niż chcesz.
**EN:** There's more burst here than you want.

minus (użytkownik wyżej):
**PL:** Jest tu mniej zrywu, niż chcesz.
**EN:** There's less burst here than you want.

**grappling** — plus:
**PL:** Chcesz dużo chwytów i tutaj jest ich dużo.
**EN:** You want a lot of grappling, and there's a lot of it here.

minus (styl wyżej):
**PL:** Chwytów jest tu więcej, niż szukasz.
**EN:** There's more grappling here than you're after.

minus (użytkownik wyżej):
**PL:** Chwytów jest tu mniej, niż szukasz.
**EN:** There's less grappling here than you're after.

**ground_fighting** — plus:
**PL:** Parteru jest tu mniej więcej tyle, ile chcesz.
**EN:** There's about as much ground work here as you want.

minus (styl wyżej):
**PL:** Parteru jest tu więcej, niż szukasz.
**EN:** There's more ground work here than you're after.

minus (użytkownik wyżej):
**PL:** Parteru jest tu mniej, niż szukasz.
**EN:** There's less ground work here than you're after.

**kicks** — plus:
**PL:** Kopnięcia są tu mniej więcej tak częste, jak chcesz.
**EN:** Kicks are about as common here as you want.

minus (styl wyżej):
**PL:** Kopnięć jest tu więcej, niż szukasz.
**EN:** There are more kicks here than you're after.

minus (użytkownik wyżej):
**PL:** Kopnięć jest tu mniej, niż szukasz.
**EN:** There are fewer kicks here than you're after.

**knees** — plus:
**PL:** Kolana są tu mniej więcej tak ważne, jak chcesz.
**EN:** Knees matter here about as much as you want.

minus (styl wyżej):
**PL:** Kolana liczą się tu bardziej, niż szukasz.
**EN:** Knees matter more here than you're after.

minus (użytkownik wyżej):
**PL:** Kolana liczą się tu mniej, niż szukasz.
**EN:** Knees matter less here than you're after.

**partner_training** — plus:
**PL:** Praca z partnerem jest tu mniej więcej tak ważna, jak chcesz.
**EN:** Partner work matters here about as much as you want.

minus (styl wyżej):
**PL:** Pracy z partnerem jest tu więcej, niż szukasz.
**EN:** There's more partner work here than you're after.

minus (użytkownik wyżej):
**PL:** Pracy z partnerem jest tu mniej, niż szukasz.
**EN:** There's less partner work here than you're after.

**punches** — plus:
**PL:** Praca pięścią jest tu mniej więcej tak ważna, jak chcesz.
**EN:** Fist work matters here about as much as you want.

minus (styl wyżej):
**PL:** Pięści liczą się tu bardziej, niż szukasz.
**EN:** Fists matter more here than you're after.

minus (użytkownik wyżej):
**PL:** Pięści liczą się tu mniej, niż szukasz.
**EN:** Fists matter less here than you're after.

**solo_training** — plus:
**PL:** Jest tu miejsce na pracę solo, której szukasz.
**EN:** There's room here for the solo work you're after.

minus (styl wyżej):
**PL:** Pracy solo jest tu więcej, niż potrzebujesz.
**EN:** There's more solo work here than you need.

minus (użytkownik wyżej):
**PL:** Pracy solo jest tu mniej, niż szukasz.
**EN:** There's less solo work here than you're after.

**striking** — plus:
**PL:** Chcesz dużo uderzeń i tutaj jest ich dużo.
**EN:** You want a lot of striking, and there's a lot of it here.

minus (styl wyżej):
**PL:** Uderzeń jest tu więcej, niż szukasz.
**EN:** There's more striking here than you're after.

minus (użytkownik wyżej):
**PL:** Uderzeń jest tu mniej, niż szukasz.
**EN:** There's less striking here than you're after.

**submissions** — plus:
**PL:** Szukanie poddania pasuje do tego treningu mniej więcej tak, jak chcesz.
**EN:** Going for a submission fits this training about as much as you want.

minus (styl wyżej):
**PL:** Poddania liczą się tu bardziej, niż szukasz.
**EN:** Submissions matter more here than you're after.

minus (użytkownik wyżej):
**PL:** Poddania liczą się tu mniej, niż szukasz.
**EN:** Submissions matter less here than you're after.

**takedowns** — plus:
**PL:** Obaleń jest tu mniej więcej tyle, ile chcesz.
**EN:** There are about as many takedowns here as you want.

minus (styl wyżej):
**PL:** Obaleń jest tu więcej, niż szukasz.
**EN:** There are more takedowns here than you're after.

minus (użytkownik wyżej):
**PL:** Obaleń jest tu mniej, niż szukasz.
**EN:** There are fewer takedowns here than you're after.

**technical_complexity** — plus:
**PL:** Złożoność techniczna pasuje do tego, czego szukasz.
**EN:** The technical load fits what you're after.

minus (styl wyżej):
**PL:** Techniki jest tu więcej, niż szukasz.
**EN:** There's more technique here than you're after.

minus (użytkownik wyżej):
**PL:** Techniki jest tu mniej, niż szukasz.
**EN:** There's less technique here than you're after.

**throws** — plus:
**PL:** Rzuty są tu mniej więcej tak ważne, jak chcesz.
**EN:** Throws matter here about as much as you want.

minus (styl wyżej):
**PL:** Rzutów jest tu więcej, niż szukasz.
**EN:** There are more throws here than you're after.

minus (użytkownik wyżej):
**PL:** Rzutów jest tu mniej, niż szukasz.
**EN:** There are fewer throws here than you're after.

**tradition_level** — plus:
**PL:** Zwyczajów i tradycji w sali jest tu mniej więcej tyle, ile chcesz.
**EN:** There's about as much hall custom and tradition here as you want.

minus (styl wyżej):
**PL:** Zwyczajów i tradycji w sali jest tu więcej, niż szukasz.
**EN:** There's more hall custom and tradition here than you're after.

minus (użytkownik wyżej):
**PL:** Zwyczajów i tradycji w sali jest tu mniej, niż szukasz.
**EN:** There's less hall custom and tradition here than you're after.

**weapons** — plus:
**PL:** Broń na tym treningu jest mniej więcej tak ważna, jak chcesz.
**EN:** Weapons matter in this training about as much as you want.

minus (styl wyżej):
**PL:** Broń jest tu ważniejsza, niż szukasz.
**EN:** Weapons matter more here than you're after.

minus (użytkownik wyżej):
**PL:** Broń jest tu mniej ważna, niż szukasz.
**EN:** Weapons matter less here than you're after.

### LOW_REASON_COPY

**athletic_demand**
**PL:** Obciążenia fizycznego jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** The physical demand is low here — and that's what you want.

**clinch**
**PL:** Zwarcia jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little close-range work here — and that's what you want.

**competition_level**
**PL:** Zawodów jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little competition here — and that's what you want.

**contact_level**
**PL:** Kontaktu jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little contact here — and that's what you want.

**elbows**
**PL:** Łokcie prawie tu nie mają znaczenia — i dobrze, bo właśnie tego szukasz.
**EN:** Elbows barely matter here — and that's what you want.

**endurance_demand**
**PL:** Nie trzeba jej tu wiele — i dobrze, bo właśnie tego szukasz.
**EN:** You don't need much endurance here — and that's what you want.

**equipment_required**
**PL:** Sprzętu jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little kit here — and that's what you want.

**explosiveness**
**PL:** Zrywu jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little burst here — and that's what you want.

**grappling**
**PL:** Chwytów jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little grappling here — and that's what you want.

**ground_fighting**
**PL:** Parteru jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little ground work here — and that's what you want.

**kicks**
**PL:** Kopnięć jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There are few kicks here — and that's what you want.

**knees**
**PL:** Kolana prawie tu nie mają znaczenia — i dobrze, bo właśnie tego szukasz.
**EN:** Knees barely matter here — and that's what you want.

**partner_training**
**PL:** Pracy z partnerem jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little partner work here — and that's what you want.

**punches**
**PL:** Pięści prawie tu nie mają znaczenia — i dobrze, bo właśnie tego szukasz.
**EN:** Fists barely matter here — and that's what you want.

**solo_training**
**PL:** Pracy solo jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little solo work here — and that's what you want.

**striking**
**PL:** Uderzeń jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little striking here — and that's what you want.

**submissions**
**PL:** Poddania prawie tu nie mają znaczenia — i dobrze, bo właśnie tego szukasz.
**EN:** Submissions barely matter here — and that's what you want.

**takedowns**
**PL:** Obaleń jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There are few takedowns here — and that's what you want.

**technical_complexity**
**PL:** Technicznie jest tu prościej — i dobrze, bo właśnie tego szukasz.
**EN:** Technically it's simpler here — and that's what you want.

**throws**
**PL:** Rzutów jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There are few throws here — and that's what you want.

**tradition_level**
**PL:** Zwyczajów i tradycji w sali jest tu mało — i dobrze, bo właśnie tego szukasz.
**EN:** There's little hall custom and tradition here — and that's what you want.

**weapons**
**PL:** Broni jest tu prawie nie ma — i dobrze, bo właśnie tego szukasz.
**EN:** There's almost no weapon here — and that's what you want.

### DIFF_COPY (porównanie)

**athletic_demand**
**PL:** {higher} bardziej obciąża ciało niż {lower}.
**EN:** {higher} loads the body more than {lower}.

**clinch**
**PL:** {higher} spędza więcej czasu w zwarciu niż {lower}.
**EN:** {higher} spends more time at close range than {lower}.

**competition_level**
**PL:** {higher} przykłada większą wagę do zawodów niż {lower}.
**EN:** {higher} puts more weight on competition than {lower}.

**contact_level**
**PL:** {higher} trenuje z mocniejszym kontaktem niż {lower}.
**EN:** {higher} trains with harder contact than {lower}.

**elbows**
**PL:** {higher} częściej używa łokci niż {lower}.
**EN:** {higher} uses elbows more often than {lower}.

**endurance_demand**
**PL:** {higher} wymaga większej wytrzymałości niż {lower}.
**EN:** {higher} asks more of your endurance than {lower}.

**equipment_required**
**PL:** {higher} wymaga więcej sprzętu niż {lower}.
**EN:** {higher} needs more kit than {lower}.

**explosiveness**
**PL:** {higher} ma więcej zrywu niż {lower}.
**EN:** {higher} is more explosive than {lower}.

**grappling**
**PL:** {higher} ma więcej chwytów niż {lower}.
**EN:** {higher} has more grappling than {lower}.

**ground_fighting**
**PL:** {higher} dłużej zostaje w parterze niż {lower}.
**EN:** {higher} stays on the ground longer than {lower}.

**kicks**
**PL:** {higher} więcej kopie niż {lower}.
**EN:** {higher} kicks more than {lower}.

**knees**
**PL:** {higher} częściej używa kolan niż {lower}.
**EN:** {higher} uses knees more often than {lower}.

**partner_training**
**PL:** {higher} bardziej potrzebuje partnera niż {lower}.
**EN:** {higher} needs a partner more than {lower}.

**punches**
**PL:** {higher} więcej pracuje pięściami niż {lower}.
**EN:** {higher} uses the fists more than {lower}.

**solo_training**
**PL:** {higher} zostawia więcej miejsca na pracę solo niż {lower}.
**EN:** {higher} leaves more room for solo practice than {lower}.

**striking**
**PL:** {higher} ma więcej uderzeń niż {lower}.
**EN:** {higher} has more striking than {lower}.

**submissions**
**PL:** {higher} częściej szuka poddania niż {lower}.
**EN:** {higher} looks for a submission more often than {lower}.

**takedowns**
**PL:** {higher} częściej próbuje obalić rywala niż {lower}.
**EN:** {higher} goes for takedowns more often than {lower}.

**technical_complexity**
**PL:** {higher} ma bardziej rozbudowany arsenał technik niż {lower}.
**EN:** {higher} has a broader technical arsenal than {lower}.

**throws**
**PL:** {higher} mocniej opiera się na rzutach niż {lower}.
**EN:** {higher} leans on throws more than {lower}.

**tradition_level**
**PL:** {higher} przykłada większą wagę do tradycji sali niż {lower}.
**EN:** {higher} puts more weight on the hall's traditions than {lower}.

**weapons**
**PL:** {higher} wyraźniej stawia na broń niż {lower}.
**EN:** {higher} puts more weight on weapons than {lower}.

---
## Załącznik: SEO (niewidoczne w treści strony)

Tytuł karty, `meta description`, Open Graph — wyszukiwarki i podgląd linku, nie tekst na home.

### base.html — domyślny <head> (gdy strona nie nadpisuje meta)

**PL:** wiciędze
**EN:** wiciędze

**PL:** Katalog sportów i sztuk walki, sprawdzenie, czego szukasz na treningu, porównywarka i trochę beki.
**EN:** A catalog of combat sports and martial arts, a check of what you want from training, a comparison tool and a bit of a laugh.

### list.html — block meta_description

**PL:** Obczaj różne sporty i sztuki walki — możesz je też porównywać.
**EN:** Check out all kinds of combat sports and martial arts — you can compare them too.

### list.html — block title_i18n

**PL:** Katalog | wiciędze
**EN:** Catalog | wiciędze

### detail.html — block meta_description

**PL:** {{ style.summary_pl }}
**EN:** {{ style.summary_en }}

### detail.html — block title_i18n

**PL:** {{ style.name_pl }} | wiciędze
**EN:** {{ style.name_en }} | wiciędze

### test.html — block title_i18n

**PL:** Quizopasowanie | wiciędze
**EN:** Quizmatch | wiciędze

### match.html — block title_i18n

**PL:** Do poczytania | wiciędze
**EN:** To read | wiciędze

### compare_form.html — block meta_description

**PL:** Dwa style z zestawu głównego, jeden obok drugiego.
**EN:** Two core styles, one next to the other.

### compare_form.html — block title_i18n

**PL:** Porównaj | wiciędze
**EN:** Compare | wiciędze

### compare.html — block meta_description

**PL:** {{ left.name_pl }} i {{ right.name_pl }}, obok siebie.
**EN:** {{ left.name_en }} and {{ right.name_en }}, side by side.

### compare.html — block title_i18n

**PL:** {{ left.name_pl }} / {{ right.name_pl }} | wiciędze
**EN:** {{ left.name_en }} / {{ right.name_en }} | wiciędze

### empty.html — block title_i18n

**PL:** Brak pytań | wiciędze
**EN:** No questions | wiciędze

### 404.html — block title_i18n

**PL:** Nie ma takiej strony | wiciędze
**EN:** This page is not here | wiciędze
