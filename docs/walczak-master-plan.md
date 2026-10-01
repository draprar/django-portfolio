# Walczak — plan produktu

Data: 2026-10-01.

Ten plan opisuje produkt, który już jest w repozytorium, i tę rundę dopięcia do release. Nie jest briefem na nową aplikację.

## 1. Executive summary

Walczak to katalog sportów i sztuk walki z trzema wejściami: czytanie kart, pytania o rodzaj treningu i porównanie dwóch stylów. Obok leżą żart (archetyp) i szkic osobowości (Mini-IPIP). Żadne z nich nie wybiera stylu i nie jest diagnozą.

Produkt był już przechodni: katalog 30 + 10, stabilna lista do czytania, czyszczenie sesji po niepełnym formularzu, publiczne API bez pól redakcyjnych. Ta runda nie dokłada funkcji. Prostuje słownik, puste filtry, opis strony przy zmianie języka i listę publicznych adresów. Reszta zostaje.

## 2. Current state

Potwierdzone w kodzie, nie w samym raporcie z 2026-09-30.

Ścieżki:

| Adres | Co robi |
| --- | --- |
| `/walczak/` | Start: Poznaj, Jaki trening, Porównaj, Żart. Szkic jest w menu. |
| `/walczak/spis/` | Katalog. Filtr rodziny i tagu. |
| `/walczak/spis/<slug>/` | Karta: skrót, historia, jak się walczy, profil słowami, relacje, fakty, źródła. |
| `/walczak/zlote/` | Zestaw mniej oczywistych. |
| `/walczak/test/` → `/walczak/dopasowanie/` | Pytania o trening. Wynik to lista do czytania, trzymana w sesji. |
| `/walczak/porownaj/` | Dwa style z zestawu głównego. |
| `/walczak/quiz/` → `/walczak/wynik/` | Żart. Remis pokazuje oba archetypy. |
| `/walczak/osobowosc/` | Szkic. Pięć liczb. Nie rusza listy stylów. |
| `/walczak/fakt/` | Jeden fakt, bez powtórki pięciu ostatnich w sesji. |
| `/walczak/api/…` | Odczyt stylów, tagów i faktu. Bez `catalog_set`, żartu i `quality`. |

Logika dopasowania jest w `walczak/preference.py`. Sortowanie to `(odległość, slug)`. Limit pięciu kart i co najwyżej dwie z jednej rodziny. Powiązane style schodzą obok siebie, nie dublują listy. Odległość nie jest pokazywana.

Treść siedzi w `walczak/data/styles.py` i `walczak/data/instruments.py`, wchodzi migracją i `import_walczak`. Walidator kończy się kodem 0. WARNING zostaje przy dziesięciu kartach, których drugie źródło tylko wskazuje temat. Badań (`Study`) nie ma. To jest stan zamierzony.

Analityka całego portfolio jest wyłączona (`analytics` to zaślepka). Walczak nie dostaje osobnych zdarzeń.

## 3. Product diagnosis

Walczak jest dla kogoś, kto chce przeczytać, czym styl jest, albo ułożyć krótką listę lektur pod rodzaj treningu, którego szuka. Nie jest dla kogoś, kto chce werdykt „twój styl” ani plan treningowy.

Pętla: start → katalog albo pytania → karta → ewentualnie porównanie albo inna karta. Żart i szkic są boczne. Prowadzą z powrotem do katalogu, nie do rankingu.

Działa: rozdział żartu od pytań o trening, jawny brak badań, parasol opisany jako parasol, źródła przy karcie, sesja nie trzyma starego wyniku po urwaniu formularza.

Niejasne przed tą rundą: angielskie „Discover” przy polskim „Poznaj”, „dyscyplina” obok „stylu”, „mniej znany” obok „mniej oczywistych”, pusty tag mówiący o rodzinie, opis `meta` zostający po polsku.

Największa wartość jest w kartach i w zdaniach, które odcinają nadmiar: „to nie jest kickboxing”, „ocena redakcji, nie pomiar siły”, „żart, nie diagnoza”.

Przed release trzeba było domknąć słownik, meta i pusty filtr. Nie trzeba było nowych rekordów, procentu dopasowania ani łączenia szkicu ze stylem.

## 4. Target product

Obietnica: przeczytasz, czym styl jest, i możesz zestawić go z tym, jak chcesz trenować. Nie dostaniesz wyroku.

Podstawowy przypadek: ktoś nie wie, czy bliżej mu do chwytu czy do uderzeń. Wchodzi w „Jaki trening”, dostaje pięć kart do czytania, otwiera jedną, porównuje z drugą.

Ścieżka główna:

1. Start mówi, co jest w środku, i że szkic niczego nie wybiera.
2. Katalog grupuje style rodziną i tagiem.
3. Karta jest do czytania: czym jest, czym nie jest, skąd to wiemy.
4. Pytania nie nazywają stylów.
5. Wynik jest listą, z plusem i minusem słowami, bez liczby.
6. Dalej jest link do karty, a obok — styl powiązany, jeśli algorytm go zdjął z listy.
7. Porównanie jest dla dwóch stylów z zestawu głównego. Mniej oczywiste czyta się osobno, bo cieniej opisane nie powinny udawać pary z boksem.
8. Żart kończy się archetypem i skojarzeniem, potem „sprawdź na serio” wraca do pytań o trening.
9. Szkic zostaje szkicem.

Role:

| Część | Rola |
| --- | --- |
| Katalog | Rzecz, do której wszystko wraca. |
| Pytania o trening | Układają listę lektur. |
| Porównanie | Dwa opisy obok siebie. |
| Żart | Charakter. Nie mierzy. |
| Szkic | Uczciwy Mini-IPIP. Nie mierzy stylu. |
| Fakty | Jeden szczegół, z etykietą, gdy to legenda. |
| Mniej oczywiste | Osobny zestaw. Nie lepszy. |

## 5. Product principles

Prawdziwiej niż ładniej. Krótszy tekst niż dłuższy. Lepsza ścieżka niż nowa funkcja. Czytelniej niż efektowniej.

Zachować: „Parasol, nie jeden regulamin.”, suche karty, żart obok, nie w środku, oceny słowami.

Nie dodawać: klubów, map, cen, wieku, kontuzji, rankingu skuteczności, „jakim jesteś wojownikiem”, procentu, gamifikacji, zaleceń treningowych.

## 6. Content strategy

Zakres zostaje: 30 w zestawie głównym, 10 mniej oczywistych. Próg walidatora tego pilnuje.

Kompletność karty to nie liczba rekordów. Karta jest kompletna, gdy ma skrót, historię, praktykę, profil, co najmniej dwa źródła i typ. Dziesięć kart ma słabsze drugie źródło. To jest REVIEW, nie powód, żeby dopisać kolejne style.

Duplikatów slugów walidator nie puszcza. Brak badań jest INFO, nie dziura.

Nie rozszerzać katalogu w tej rundzie. Matryca „kategoria × styl × typ pytania × trudność” pasowałaby do quizu wiedzy. Walczak nim nie jest. Nowe rekordy bez lepszego źródła pogorszyłyby zbiór.

Pipeline, który naprawdę działa, jest w git, nie w statusie w bazie:

1. Szkic tekstu w `walczak/data/`.
2. Przegląd przy zmianie: `docs/walczak-content-review.md` i `docs/walczak-content-sources.md`.
3. `import_walczak` albo migracja.
4. `validate_walczak_content` — ERROR blokuje, WARNING zostaje widoczne.
5. `active=True` jest publikacją. `active=False` ściąga kartę ze spisu, z dopasowania i z mapy stron.

Osobne stany DRAFT / APPROVED w modelu nie powstają. Byłyby drugim miejscem prawdy obok plików i recenzji, i rozjechałyby się z nimi.

## 7. Data architecture

`Style` jest kartą. `TrainingProfile` ma 22 osie 0–5 i służy tylko do odległości oraz słów na karcie. `StyleRelation` wymaga źródła. `Source.quality = discovery_only` nie liczy się jako drugie oparcie. `Fact.is_legend` odcina podanie od praktyki.

`Question` / `Choice` to stary quiz punktowy. Publiczny `/quiz/` czyta `HumorQuestion`. Stary model zostaje w bazie i w panelu, żeby migracji nie ruszać bez potrzeby. Nie wraca do interfejsu.

`PreferenceQuestion` nie wskazuje stylu. Wagi siedzą na opcjach. Szkic (`IPIPItem`) nie ma klucza obcego do `Style`.

API listy oddaje slug, nazwy, rodzinę i region. Szczegół oddaje opis, historię, praktykę, typy i źródła bez `quality`. Żart i zestaw redakcyjny nie wychodzą.

## 8. UX architecture

Po każdym ekranie ma być widać, co dalej.

| Ekran | Dalej |
| --- | --- |
| Start | Cztery wejścia. Zdanie o szkicu, żeby menu nie było zagadką. |
| Spis | Karta. Pusty filtr mówi, co jest puste, i link „Pokaż wszystkie”. |
| Karta | Źródła i relacje są linkami. |
| Pytania | Błąd zostaje przy formularzu i bierze fokus. Komplet otwiera listę. |
| Lista | Nazwa stylu prowadzi do karty. „Obok tego leży” też. |
| Porównanie | Formularz wraca, gdy para jest zła albo styl jest spoza zestawu głównego. |
| Żart | „Jeszcze raz” albo „Sprawdź na serio”. |
| Szkic | Zostaje na tej samej stronie z pięcioma liczbami. |
| 404 | Start albo Poznaj. |

Odświeżenie listy i wyniku czyta sesję. Wejście na wynik bez sesji wraca do formularza. Niepełny POST kasuje poprzedni klucz. Bezpośredni URL karty i porównania działa bez sesji. Porównanie tego samego slugu albo stylu spoza zestawu głównego nie otwiera pary.

## 9. Copy strategy

Zostawić zdania, które już brzmią jak Walczak. Zmieniać tylko tam, gdzie słownik się rozjeżdża albo tekst obiecuje nie to.

Zrobione w tej rundzie:

- „dyscyplin” na spisie → „stylów”.
- EN „Discover” → „Browse”.
- „Mniej znany” na liście → „Mniej oczywiste”.
- Pusty tag nie mówi o rodzinie.
- Opis porównania to nazwy dwóch stylów, nie skrót jednego.
- Start mówi, że szkic liczy pięć liczb i nie wybiera stylu.

Nie ruszane, bo są dobre: karty w `styles.py`, archetypy, powody dopasowania w `dimensions.py`, stopki o diagnozie, „Parasol, nie jeden regulamin.”, „Smak, nie wyrok.”

Zasady: `docs/walczak-copy-style-guide.md`.

## 10. Localization strategy

Dokument startuje z `lang="pl"`. Przełącznik woła `core/js/lang.js`, który podmienia węzły z `data-pl` i `data-en`, w tym `content` przy `meta`. Walczak ma `data-lang-plain`, więc treść z bazy nie jest wstawiana jako HTML.

`og:title` nie ma pary językowej w atrybucie, bo tytuł strony już ją ma. Po przełączeniu krótki skrypt w szablonie Walczaka przepisuje `og:title` z `document.title`. Robot bez JavaScriptu widzi polski tytuł, zgodny z domyślnym `lang`.

Hreflang nie jest dodany. Nie ma osobnych URL-i językowych. Jedna strona, dwa teksty.

Angielski nie jest kalką. „Poznaj” nie staje się „Discover”. „Sprawdź na serio” zostaje „Check for real”.

## 11. Quality strategy

Walidator treści: puste pola karty, próg 30/10, dwa źródła w zestawie głównym, URL, typ, profil przy włączonym dopasowaniu, źródło przy relacji i przy badaniu.

Testy zachowania, nie tylko „pytest przeszedł”: lista po rodzinie, pusta rodzina, pusty tag, nieaktywna karta, remis żartu, urwany quiz kasuje sesję, stabilna kolejność dopasowania, szkic nie zmienia listy, API bez pól redakcyjnych, mapa stron bez ekranów sesji, nagłówki cache API.

Lint: ruff. Typy: mypy na `walczak`.

Poza automatem, i tak oznaczone jako niezweryfikowane: czytnik ekranu, Firefox, Safari, iOS, polowe Core Web Vitals.

## 12. Production strategy

Walczak nie ma własnych ustawień. Jedzie na `config/settings.py`: przy `DEBUG=False` wymuszony `ALLOWED_HOSTS`, HTTPS, HSTS, ciasteczka `Secure` / `HttpOnly` / `SameSite=Lax`, CSP. HTML dostaje `Cache-Control: no-store` w middleware. Sekrety nie siedzą w repozytorium.

Baza: migracje `walczak` łącznie z importem katalogu. Nie ma osobnego seeda przy starcie produkcji ponad migrację.

Statyczne: `walczak/static/walczak/css/walczak.css` i wspólny `lang.js`.

Poczty Walczak nie wysyła.

Katalog publiczny w API może być cache’owany 300 sekund. Losowy fakt ma `no-store`, bo każde GET ma być innym faktem, o ile pula na to pozwala.

Backup i rollback są sprawą hosta portfolio, nie osobnym mechanizmem Walczaka. Rollback aplikacji to poprzedni deploy; rollback treści to poprzedni commit danych i migracja wstecz, jeśli została.

Monitoring: brak osobnego dla Walczaka. Analityka odwiedzin jest globalnie wyłączona i tak zostaje. Włączanie jej tylko tutaj rozjechałoby się z resztą serwisu.

## 13. Release strategy

Publiczne do indeksu: start, spis, karta, mniej oczywiste, formularz porównania, konkretna para. Mapa: `/walczak/sitemap.xml`.

Poza indeksem (`noindex`): test, dopasowanie, quiz, wynik, szkic, fakt, pusta ścieżka aplikacji. Wynik zależy od sesji albo od losowania. Nie ma z niego strony do zacytowania.

Osobny `robots.txt` dla całego portfolio nie powstaje w tej rundzie. Meta `noindex` na ekranach sesji jest granicą, którą Walczak kontroluje bez ruszania innych aplikacji.

Rate limit 10 POST na minutę z IP: pytania, żart, szkic, formularz porównania.

Release gate: testy Walczaka, ruff, mypy, walidator treści, brak nowego P0. Szczegóły w `docs/walczak-release-checklist.md`.

## 14. Detailed phases

### Faza 0 — audyt

Przeczytane: modele, widoki, URL-e, szablony, CSS, dane, walidator, testy, trzy istniejące dokumenty. Kod był zgodny z audytem z 2026-09-30 w sprawach sesji, API i progów katalogu. Rozjazd: audyt utrwalał „Discover” i „Mniej znany”, a docelowy słownik jest inny. Kod ma pierwszeństwo przed starym raportem; raport dostał zdanie odsyłające.

### Faza 1 — słownik i puste stany

Bez nowych funkcji. Teksty, które myliły, poprawione w szablonach. Karty stylów nietknięte.

### Faza 2 — język w meta i mapa stron

`lang.js` ustawia `content` na `meta`, jeśli element ma `data-pl` i `data-en`. Inne aplikacje nie mają takich meta, więc zmiana ich nie rusza. Walczak dokłada Open Graph i własną mapę XML.

### Faza 3 — cache API

Lista, szczegół i tagi: `public, max-age=300`. Fakt: `no-store`. HTML zostaje przy globalnym `no-store`.

### Faza 4 — dokumenty i bramka

Ten plan, przewodnik copy, notatki release, checklista. Testy nowych zachowań. Walidator. Lint i typy.

Czego faza 4 nie robi: nowych stylów, statusu redakcyjnego w modelu, zdarzeń analitycznych, `robots.txt` całego serwisu, hreflang.

## 15. Acceptance criteria

- Spis mówi „stylów”, nie „dyscyplin”. Angielskie wejście to „Browse”.
- Pusty tag nie wspomina rodziny. Pusta rodzina nadal mówi o rodzinie.
- Etykieta zestawu na liście do czytania to „Mniej oczywiste”.
- Start mówi, że szkic nie wybiera stylu.
- Opis `meta` ma parę PL/EN na stronach publicznych.
- `/walczak/sitemap.xml` zawiera karty aktywnych stylów i nie zawiera quizu, testu, dopasowania, faktu, szkicu ani wyniku.
- API listy nie oddaje `catalog_set`. Fakt nie jest cache’owany jak katalog.
- Istniejące testy dopasowania, żartu i sesji dalej przechodzą.
- Walidator treści kończy się kodem 0.
- Żart dalej jest podpisany jako żart. Szkic dalej nie rusza rankingu.
