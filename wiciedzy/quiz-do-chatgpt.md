# Quizopasowanie — stan po wdrożeniu

ChatGPT: proszę o ponowną analizę tego quizu i o konkretne propozycje rozszerzenia.

To jest aktualny kod, nie stary brief. Analizuj ten mechanizm i te odpowiedzi. Nie wymyślaj osobowości, skuteczności, „typu człowieka” ani „najlepszego stylu dla Ciebie”. Nie dodawaj osi „dystans”. Odległość służy tylko do ułożenia listy do poczytania. Użytkownik jej nie widzi.

Katalog: 46 aktywnych stylów. Marka w UI: małe `wiciędze`.

---

## 1. Co użytkownik widzi

14 pytań, jedno pod drugim. Pytania 1–13 są wymagane. Pytanie 14 (checkboxy) może zostać puste.

Brak odpowiedzi na skalę albo na pytanie jednokrotnego wyboru = brak listy, komunikat: „Zaznacz każdą skalę i każdy wymagany wybór.”

Wynik nazywa się „Do poczytania”. Nagłówek: pięć stylów, zaczynamy od najlepszego dopasowania **w tym zestawie**. Pod spodem: porównanie opiera się na preferencjach i ogólnym profilu karty, nie opisuje każdej szkoły.

Przy stylu:

- ewentualnie „To nazwa zbiorcza…” (parasol: karate, wushu, arnis, jujutsu, silat, taijiquan),
- ewentualnie etykieta „Mniej oczywiste” (zestaw poboczny `golden`, nie ocena jakości),
- nazwa ze linkiem do karty,
- do 3 zdań zgodności,
- do 2 zdań różnicy (wyciszone),
- „Blisko tego jest {nazwa}.” tylko wtedy, gdy drugi styl spadł z listy przez relację w bazie.

Liczba odległości, procent i punkty nie są pokazywane.

---

## 2. Mechanizm

Profile stylów to liczby całkowite 0–5 na osiach treningu. Opisują praktykę, nie skuteczność.

Do rankingu wchodzą style `active=True` i `matcher_enabled=True`, które mają profil.

### 2.1. Skala 1–5 → liczba 0–5

Wzór: `(wybór − 1) / 4 × 5`.

| Klik | Wartość |
|---|---|
| 1 | 0 |
| 2 | 1,25 |
| 3 | 2,5 |
| 4 | 3,75 |
| 5 | 5 |

### 2.2. Waga opcji → liczba 0–5

Wzór: `ogranicz(0, 5, 2,5 + waga × 1,25)`.

| Waga w danych | Wartość na osi |
|---|---|
| −2 | 0 |
| −1 | 1,25 |
| +1 | 3,75 |
| +2 | 5 |

W tym quizie nie ma wagi 0 ani −1. −1 zostało świadomie usunięte.

### 2.3. Wektor użytkownika

Oś trafia do wektora tylko wtedy, gdy jakieś pytanie ją ustawiło.

Ta sama oś z dwóch pytań jest **uśredniana**, nie sumowana i nie nadpisywana. To ważne:

- `striking` ustawiają pytanie 1 i (jeśli wybrany cios) pytanie 13.
- `kicks` ustawiają pytanie 5 i zawsze pytanie 12.
- `ground_fighting` ustawiają pytanie 3 i (jeśli wybrany parter) pytanie 13.

Przykład: skala uderzeń = 5 (wartość 5) i „Uderzenie z bliska” (`striking +1` → 3,75) daje striking = (5 + 3,75) / 2 = **4,375**.

Przykład: skala kopnięć = 5 (wartość 5) i „Z bliska” (`kicks −2` → 0) daje kicks = (5 + 0) / 2 = **2,5**.

Pytanie 14: jeśli wśród zaznaczeń jest opcja bez wag („Nic z powyższych”), **całe pytanie 14 jest ignorowane**, także gdy JS jest wyłączony i użytkownik zaznaczył rękawice oraz „nic”. Puste pytanie 14 nic nie dodaje. Innych pytań to nie zeruje.

### 2.4. Odległość

Dla stylu bierzemy tylko osie, które są i u użytkownika, i w profilu.

`odległość = średnia |użytkownik − styl|` na tych osiach.

Mniejsza odległość = wyżej. Remis: alfabetycznie po slugu.

Oś, której użytkownik nie ustawił, **nie wchodzi** do średniej. Nie ma kary za brak odpowiedzi na checkboxach.

### 2.5. Lista 5

1. Idziemy po posortowanej liście. Bierzemy styl, dopóki w jego rodzinie (`family`) nie ma już 2 sztuk i dopóki nie ma 5 stylów. To lista tymczasowa.
2. W tej piątce: jeśli dwa style mają relację w bazie (kierunek obojętny), niższy spada z listy i ląduje przy wyższym jako „Blisko tego jest”.
3. Jeśli po tym jest mniej niż 5, dobieramy kolejne style z pełnego rankingu. Pomijamy: już użyte, rodzinę która ma już 2, oraz styl spokrewniony z kimkolwiek, kto został na liście. Dobierany styl **nie** dostaje drugiego „blisko”.

### 2.6. Zdania przy stylu

Dla każdej wspólnej osi, `diff = |użytkownik − styl|`:

| Warunek | Zdanie |
|---|---|
| `diff ≤ 1` i obie strony ≥ 3 | zgodność, wersja „mniej więcej tyle, ile chcesz” |
| `diff ≤ 1` i użytkownik ≤ 1,5 i styl ≤ 1 | zgodność, wersja „mało — i dobrze” |
| `diff ≥ 2,5` i styl wyżej | różnica: jest tego więcej, niż szukasz |
| `diff ≥ 2,5` i użytkownik wyżej | różnica: jest tego mniej, niż szukasz |
| reszta (diff od 1 do 2,5, albo środek skali przy małej różnicy) | nic |

Zgodności sortowane od najmniejszej różnicy, max 3. Różnice od największej różnicy, max 2.

Przy wartości 3 po obu stronach zdanie **nie** mówi „sporo”, „dużo” ani „a lot”.

Zdania opisują relację użytkownik ↔ styl. Nie oceniają człowieka.

---

## 3. Osie

Quiz może ustawić te osie. Reszta profilu (przede wszystkim `punches`) istnieje na kartach, ale **żadne pytanie jej nie rusza**, więc nie wpływa na odległość.

| Oś | Skąd |
|---|---|
| striking | P1, oraz P13 „uderzenie” |
| grappling | P2 |
| ground_fighting | P3, oraz P13 „parter i poddanie” |
| weapons | P4 |
| kicks | P5 i P12 |
| contact_level | P6 |
| competition_level | P7 |
| tradition_level | P8 |
| technical_complexity | P9 |
| athletic_demand | P10 |
| solo_training, partner_training | P11 |
| clinch | P12 |
| throws | tylko P13 „rzut” |
| takedowns | tylko P13 „obalenie” |
| submissions | tylko P13 „parter i poddanie” |
| knees, elbows, equipment_required, endurance_demand, explosiveness | P14, każda osobno |

`athletic_demand` jest w quizie, bo w profilach ma rozrzut 2–5 (iaido, kyudo, taiji = 2; muay thai, MMA, zapasy, sumo, lethwei, pankration = 5).

---

## 4. Pytania i odpowiedzi

Kotwice skali, jeśli nie napisano inaczej: **1 = wcale, 5 = bardzo.**

### P1. Skala. Oś `striking`. Wymagane.

PL: Jak bardzo chcesz pracować uderzeniami (oś striking)?

EN: How much do you want striking work (the striking axis)?

### P2. Skala. Oś `grappling`. Wymagane.

PL: Jak bardzo chcesz pracować w chwycie (oś grappling)?

EN: How much do you want grappling work (the grappling axis)?

### P3. Skala. Oś `ground_fighting`. Wymagane.

PL: Jak bardzo chcesz walczyć w parterze?

EN: How much do you want to fight on the ground?

### P4. Skala. Oś `weapons`. Wymagane.

PL: Jak bardzo chcesz mieć broń na treningu?

EN: How much do you want a weapon in training?

### P5. Skala. Oś `kicks`. Wymagane.

PL: Jak bardzo chcesz kopać?

EN: How much do you want to kick?

### P6. Skala. Oś `contact_level`. Wymagane.

PL: Jak mocny ma być kontakt na treningu z partnerem?

EN: How hard should partner contact be in training?

Kotwice: 1 = bardzo lekki / very light, 5 = bardzo mocny / very hard.

### P7. Skala. Oś `competition_level`. Wymagane.

PL: Jak bardzo chcesz startować w zawodach?

EN: How much do you want to compete?

### P8. Skala. Oś `tradition_level`. Wymagane.

Jedna oś: tradycja i zwyczaj sali razem, nie dwa tematy.

PL: Jak ważna jest dla Ciebie tradycja i zwyczaje w sali?

EN: How much do hall custom and tradition matter to you?

### P9. Skala. Oś `technical_complexity`. Wymagane. Nowe.

PL: Jak bardzo chcesz złożonej technicznie pracy?

EN: How much technical complexity do you want?

Kotwice: 1 = bardzo prosto / very simple, 5 = bardzo złożone / very complex.

Termin wszędzie: „złożoność techniczna” / „technical complexity”. Nie „technical load”.

### P10. Skala. Oś `athletic_demand`. Wymagane. Nowe.

PL: Jak wymagający fizycznie ma być trening?

EN: How physically demanding do you want training to be?

Kotwice: 1 = bardzo lekki / very light, 5 = bardzo wymagający / very demanding.

### P11. Jedna odpowiedź z trzech. Wymagane.

PL: Wolisz ćwiczyć głównie sam, głównie z partnerem, czy mieszać oba?

EN: Would you rather train mostly alone, mostly with a partner, or a mix of both?

| Opcja PL | Opcja EN | Wagi | Wartości |
|---|---|---|---|
| Głównie sam — technika albo worek. | Mostly alone — technique or a bag. | solo +2, partner −2 | solo 5, partner 0 |
| Mieszanka solo i z partnerem. | A mix of solo and partner work. | solo +1, partner +1 | solo 3,75, partner 3,75 |
| Głównie z partnerem, który się rusza. | Mostly with a partner who moves. | solo −2, partner +2 | solo 0, partner 5 |

### P12. Jedna odpowiedź z trzech. Wymagane.

To zasięg kontra bliskość. Nie ma osobnej osi distance. Kopnięcia i klincz są w pytaniu nazwane wprost.

PL: Wolisz zostać z daleka, wejść blisko, czy trzymać mieszankę?

EN: Would you rather stay at range, step in close, or keep a mix?

| Opcja PL | Opcja EN | Wagi | Wartości |
|---|---|---|---|
| Z daleka — niech noga robi robotę. | At range — let the leg do the work. | kicks +2, clinch −2 | kicks 5, clinch 0 |
| Z bliska — klincz albo chwyt. | Up close — a clinch or a grip. | clinch +2, kicks −2 | clinch 5, kicks 0 |
| Mieszanka — kopnięcia i klincz po równo. | A mix — kicks and clinch matter about equally. | kicks +1, clinch +1 | kicks 3,75, clinch 3,75 |

`kicks` z tej odpowiedzi uśrednia się ze skalą P5.

### P13. Jedna odpowiedź z czterech. Wymagane.

PL: Co wolisz, gdy trening schodzi do bliskiej pracy?

EN: What do you prefer when training moves into close work?

Jedna opcja ustawia tylko to, co jest w zdaniu.

| Opcja PL | Opcja EN | Wagi | Wartości | Czego nie rusza |
|---|---|---|---|---|
| Rzut. | A throw. | throws +2 | throws 5 | takedowns |
| Obalenie. | A takedown. | takedowns +2 | takedowns 5 | throws |
| Schodzisz do parteru i szukasz poddania. | Ground work and a submission. | submissions +2, ground_fighting +2 | obie 5 | — |
| Uderzenie z bliska. | A strike at close range. | striking +1 | striking 3,75 | punches |

`ground_fighting` uśrednia się ze skalą P3. `striking` uśrednia się ze skalą P1.

### P14. Checkboxy. Niewymagane. Kilka naraz.

PL: Zaznacz, co ma być w Twoim tygodniu treningowym. Możesz wybrać kilka rzeczy naraz; jeśli nic z tego nie ma dla Ciebie znaczenia, zaznacz wyłącznie ostatnią opcję.

EN: Tick what should be in your training week. You can pick several; if none of it matters to you, tick only the last option.

| Opcja PL | Opcja EN | Wagi | Wartość |
|---|---|---|---|
| Kolana. | Knees. | knees +2 | 5 |
| Łokcie. | Elbows. | elbows +2 | 5 |
| Zbroja albo maska. | Armour or a mask. | equipment_required +2 | 5 |
| Rękawice. | Gloves. | equipment_required +1 | 3,75 |
| Wytrzymałość, długie rundy. | Endurance, long rounds. | endurance_demand +2 | 5 |
| Eksplozywne wejście. | An explosive entry. | explosiveness +2 | 5 |
| Nic z powyższych. | None of these. | brak | pytanie odpada |

„Zbroja albo maska” i „Rękawice” to dwa poziomy tej samej osi sprzętu, nie dwa różne światy. Zaznaczenie obu uśrednia sprzęt: (5 + 3,75) / 2 = 4,375.

JS: „Nic z powyższych” odznacza resztę; inne odznacza „nic”. Klawiatura działa na zwykłych checkboxach. Bez JS serwer i tak wyrzuca wagi całego pytania, gdy „nic” jest w zestawie.

---

## 5. Co się zmieniło

Było 12 pytań. Jest 14. Doszły P9 (złożoność) i P10 (fizyka).

| Było | Jest |
|---|---|
| Solo albo partner, dwie opcje | Trzy: sam / mieszanka / partner |
| „Daleko czy blisko”, blisko dawało kicks −1 | Zasięg / blisko / mieszanka, wagi symetryczne ±2, mieszanka +1/+1 |
| Jedna opcja „rzut albo obalenie” = throws +2 i takedowns +2 | Rzut i obalenie osobno. Cios z bliska to striking +1, nie punches +2 |
| Jeden checkbox „kolana i łokcie” | Dwa checkboxy. „Nic” jest wyłączne |
| Każda skala: „wcale / bardzo” | Kontakt, złożoność i fizyka mają własne kotwice |
| Zgodność przy 3 potrafiła brzmieć „sporo / a lot” | „Mniej więcej tyle, ile chcesz” |
| Miejscami „niż potrzebujesz” | „niż szukasz”, tam gdzie to tylko preferencja |

Silnik bez zmian: wzory skali i wag, średnia na wspólnych osiach, remis slugiem, limit 5, cap rodziny 2, zwijanie relacji, progi zdań, max 3+2 zdania.

---

## 6. Czego nie ruszać w propozycjach

- Nie dodawać osobowości, IPIP, archetypów humoru ani „jesteś typem, który…”.
- Nie pisać, że styl jest skuteczny albo najlepszy.
- Nie pokazywać liczby odległości na karcie wyniku.
- Nie dokładać osi distance.
- Jedna odpowiedź nie może cicho ustawiać osi, której zdanie nie nazywa.
- Rzut ≠ obalenie. Cios ≠ pięści. Kolana ≠ łokcie. Blisko ≠ kicks −1.
- Cap 2, limit 5 i „Blisko tego jest” zostają.
- 46 stylów zostaje. Małe `wiciędze` zostaje.

Propozycje rozszerzenia: nowe pytanie, przeredagowanie istniejącego, albo luka (oś na profilu, której quiz nie tyka — dziś to głównie `punches`). Przy każdej: co użytkownik czyta, jaką oś rusza, jaką wagę, i czy nie zdubluje osi, która już jest uśredniana.
