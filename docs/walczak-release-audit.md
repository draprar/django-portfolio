# Walczak — audyt release candidate

Data: 2026-09-30.

## Werdykt

**READY FOR USER TESTING**

P0: 0. P1: 0.

Werdykt dotyczy obecnego produktu: katalog, lista do czytania, porównanie, żart i szkic osobowości. Automatyczny skan i jeden przebieg laboratorium nie są dowodem zgodności z WCAG ani z celami polowymi Core Web Vitals.

## 1. Zakres

Zamknięty został istniejący Walczak. W tym przebiegu doszły tylko poprawki P0/P1: czyszczenie sesji po niepełnym teście, żarcie i szkicu; zdanie o pięciu stylach i 22 osiach; opis szkicu zgodny z pozycjami odwróconymi; słownik Discover / Less obvious; tytuły i legendy PL/EN; `fieldset`; fokus na błędzie; jeden `h1` przy remisie; dwujęzyczne 404 Walczaka; zdjęcie `catalog_set` z publicznego API; twardy test sortowania; podkreślenie linków w tekście karty i źródeł.

Poza zakresem zostały kluby, mapy, ceny, plany, wiek, kontuzje, ranking skuteczności, łączenie osobowości ze stylem, „jaki jesteś wojownikiem”, dokładniejszy procent i badania „z grubsza”.

## 2. Definition of Done

| Kryterium | Wynik | Dowód |
| --- | --- | --- |
| Poznaj, Jaki trening, Porównaj, Żart i Szkic da się przejść | PASS | Przeglądarka na `127.0.0.1:8765`: spis, kompletny test, odświeżenie listy, porównanie boks/judo, pusty quiz, szkic |
| Brak `score` i `band` w HTML, sesji, aria, data attributes i JSON strony | PASS | Lista „Do poczytania” bez dopasowania do `score`, `band` i `%`; `test_preference_rank_is_stable_and_skips_a_style_without_a_profile` |
| Niekompletny test nie otwiera listy | PASS | `test_incomplete_preference_does_not_open_a_list`; wejście na `/walczak/dopasowanie/` bez sesji wraca do `/walczak/test/` |
| Gość dostaje listę do czytania | PASS | Zdanie o pięciu stylach i 22 osiach na stronie i w teście |
| Te same odpowiedzi dają tę samą listę | PASS | `test_preference_rank_is_stable_and_skips_a_style_without_a_profile`; `test_equal_distance_breaks_the_tie_by_slug` |
| Nieudany nowy test nie zostawia poprzedniej listy | PASS | Niepełny POST czyści `walczak_preference`, `walczak_result` albo `walczak_ipip` |
| Katalog 30 + 10, progi bez zmian | PASS | `test_import_is_stable_and_validation_passes`; spis ma 40 kart (`h2`) |
| `discovery_only` nie udaje drugiego pełnego oparcia | PASS | Walidator: WARNING, exit 0; karta krav-maga: „Opis jest cieńszy: drugie źródło tylko wskazuje temat.” |
| Pusty quiz i remis są jawne; remis nie wybiera jednego archetypu | PASS | Pusty quiz zostaje na formularzu z „Zaznacz odpowiedzi.”; `test_tied_quiz_shows_both_archetypes` liczy jeden `<h1` |
| Szkic 1–5, bez norm i bez wpływu na style | PASS | Zdanie o krótkim kwestionariuszu; `test_personality_score_does_not_change_the_preference_rank`; `test_reverse_ipip_item_flips_the_point` |
| Ten sam słownik PL/EN, `lang` podąża za przełącznikiem | PASS | Title z `data-pl` / `data-en`; menu „Discover”; etykieta „Less obvious” |
| Brak znanych P0/P1 a11y na głównych ścieżkach | PASS | axe-core 4.10.3: 0 naruszeń po poprawce podkreślenia. To nie jest orzeczenie WCAG |
| Security: check, check --deploy, CSRF, cookies, brak tracebacka | PASS | Oba checki: „no issues (2 silenced)”. HTML `Cache-Control: no-store` |
| LCP, INP, CLS w laboratorium, z warunkami | PASS częściowy | LCP i CLS zmierzone. INP niezweryfikowany. Cele polowe 2,5 s / 200 ms / 0,1 nie są wynikiem tego przebiegu |
| Publiczny katalog: title, opis, canonical. Sesja: noindex. Bez hreflang | PASS | Spis, karta, porównanie indeksowalne. Test, lista, quiz, szkic: `noindex` |
| Smoke 320, 360, 390, 768, desktop; brak 404 assetów na głównych ścieżkach | PASS w Chromium | Poziomy overflow 0. Timing zasobów spisu: 0 odpowiedzi ≥ 400 |

## 3. P0

Brak otwartych.

Zamknięty w tym przebiegu: niepełny POST testu, quizu albo szkicu zostawiał poprzedni zapis sesji, a GET wyniku pokazywał starą listę. Widoki kasują odpowiedni klucz przed ponownym renderem.

## 4. P1

Brak otwartych.

Zamknięte w tym przebiegu:

- Kopia listy mówi o pięciu stylach ułożonych według zgodności i o 22 osiach profilu.
- Szkic mówi, że liczba jest wynikiem krótkiego kwestionariusza w skali 1–5. Odwrócenie pozycji (`6 - raw`) zostaje w liczeniu.
- Słownik EN: Discover, Less obvious. Pusta rodzina prowadzi do „Poznaj / Discover”.
- Tytuły i legendy grup mają `data-pl` / `data-en`. Pytania są w `fieldset` / `legend`. Kotwice 1 i 5 są w nazwie dostępnej radia.
- Po błędzie fokus ląduje na `[data-walczak-error]`. Pusty quiz: fokus na `.walczak-message`.
- Remis żartu ma jeden `h1`.
- Ścieżka `/walczak/…` bez widoku renderuje dwujęzyczną stronę Walczaka, gdy działa handler 404.
- Publiczne API listy i szczegółu nie oddaje `catalog_set`.
- Sortowanie zostaje `(distance, slug)`.
- Linki źródeł i linki w tekście karty były odróżnione samym kolorem (`#c4922a` przy tekście `#e0e0e0`, kontrast 2,12:1). axe-core zgłosił `link-in-text-block` (impact: serious) na karcie krav-maga. Dostały podkreślenie. Ponowny skan tej karty: 0 naruszeń.

## 5. P2

Zostają. Nie psują przejścia głównych ścieżek.

- Opis `meta` zostaje po polsku, gdy przełącznik ustawia angielski. `lang.js` podmienia węzły z `data-pl` i `data-en`. Atrybutu `content` nie rusza. Indeksujący widzą polski opis. Hreflang nie jest dodany.
- Projekt nie ma sitemap. Publiczne strony mają title, opis i canonical.
- Przy `DEBUG=True` nieznany adres `/walczak/…` pokazuje techniczne 404 Django. Handler dwujęzyczny jest podpięty i pokryty testem; w produkcji `DEBUG` jest wyłączone.
- JSON publicznego API w tym przebiegu nie wysłał `Cache-Control`. HTML ma `no-store`.
- Część źródeł encyklopedycznych ma puste pole licencji. Wikipedia na karcie krav-maga pokazuje CC BY-SA 4.0.
- Słowo „stójka” zostaje w opisie karty tam, gdzie opisuje walkę na nogach. Oś preferencji uderzeń mówi „uderzenia”.
- Skip link ma regułę `.walczak-skip:focus { left: 0 }`, a cel `#walczak-main` istnieje. W osadzonej przeglądarce `:focus` nie zaskoczył przy programowym fokusie, więc wizualne wysunięcie linku nie zostało potwierdzone klawiszem. Klik ustawił hash `#walczak-main`.

## 6. Funkcjonalność

- Start: jeden `h1`, cztery wejścia w treści (Poznaj, Jaki trening, Porównaj, Żart) i Szkic w nawigacji.
- Spis: 40 kart, jeden `h1` „Poznaj”, rodziny i tagi.
- Test: 12 grup (`fieldset`), skala „1 , w ogóle” / „5 , bardzo”, multi może zostać puste.
- Kompletny POST otworzył `/walczak/dopasowanie/`. Odświeżenie zostało na tej liście: Aikido, Hapkido, Krav maga, Capoeira, Glíma. Glíma ma etykietę „Mniej znany”.
- Porównanie boks/judo: historia i typ, potem różnice, potem pary słowne. Zdanie o braku danych osobowości i badań jest na stronie. Różnica uderzeń jest zapisana jako „więcej uderzeń”.
- Quiz: 8 grup, stopka „To żart, nie diagnoza i nie rekomendacja treningu.” Pusty POST został na `/walczak/quiz/` z alertem.
- Szkic: 20 pozycji, kotwice „zdecydowanie nie” / „zdecydowanie tak”. Zapisana sesja pokazuje pięć liczb i zdanie o kwestionariuszu.

## 7. Dopasowanie

Klucz sortowania to `(distance, slug)`. Rodzina, relacja i zestaw golden nie losują kolejności. Limit czytania i limit rodziny zostają w algorytmie. Strona listy nie obiecuje procentu ani „pięciu najbliższych”. Stopka zostawia zdanie, że poziomy na kartach są oceną redakcji.

## 8. Treść i źródła

`python manage.py validate_walczak_content` zakończył się kodem 0. WARNING dla drugiego źródła `discovery_only`: krav-maga, hapkido, arnis, lethwei, bokh, laamb, glima, gatka, kalaripayattu, dambe. INFO: brak badań nie jest błędem. Progów 30/10 nie zmieniano.

URL-e źródeł nie były odpytywane jeden po drugim. 403 albo robots nie byłyby podstawą do uznania źródła za złe. Karta krav-maga w przeglądarce pokazuje Wikipedię i Britannicę oraz zdanie o cieńszym opisie.

Publiczne API, 40 rekordów listy, klucze: `slug`, `name_pl`, `name_en`, `family`, `region`. Szczegół boksu ma historię, praktykę, typy i źródła. Brak `catalog_set`, `joke_pl` i `quality`.

## 9. PL/EN

Dokument startuje z `lang="pl"`. Przełącznik pisze do `localStorage` (`site_lang`) i podmienia tekst elementów z parą `data-pl` / `data-en`. Tytuł jest w tym mechanizmie. Legenda ma atrybuty na wewnętrznym `span`, więc ukryte „Wymagane” zostaje przy zmianie języka.

## 10. WCAG

Narzędzie: axe-core 4.10.3, wstrzyknięte w osadzony Chromium, reguły domyślne, `resultTypes: violations`.

| Strona | Naruszenia |
| --- | --- |
| `/walczak/spis/` przy 360 px | 0 |
| `/walczak/` | 0 |
| `/walczak/test/` | 0 |
| `/walczak/dopasowanie/` | 0 |
| `/walczak/porownaj/boks/judo/` | 0 |
| `/walczak/quiz/` | 0 |
| `/walczak/spis/krav-maga/` przed podkreśleniem | `link-in-text-block`, serious, 2 węzły |
| `/walczak/spis/krav-maga/` po podkreśleniu | 0 |

Przegląd ręczny: jeden `h1` na sprawdzonych stronach; skip link wskazuje `#walczak-main`; grupy pytań są w `fieldset`; skala 1 i 5 ma tekst dla czytnika; błąd quizu bierze fokus; przy 320 px widoczne linki i przyciski spisu miały co najmniej 24×24 px; overflow poziomy 0 przy 320, 360, 390, 640, 768 i 1265 px. Szerokość 640 px jest przybliżeniem powiększenia 200% okna 1280 px. `prefers-reduced-motion` jest w CSS i nie był przełączany w systemie.

Niezgodności po poprawce: brak znanych na przebadanych stronach. Narrator niezweryfikowany. Ten raport nie orzeka zgodności z WCAG 2.2 AA.

## 11. Bezpieczeństwo

- `python manage.py check` → System check identified no issues (2 silenced).
- `python manage.py check --deploy` przy `DJANGO_DEBUG=false`, `DJANGO_TESTING=true`, hoście `example.com`, pochodzeniu CSRF `https://example.com` i sekrecie dłuższym niż 50 znaków → ten sam wynik.
- Przy `DEBUG=false` ustawienia włączają HTTPS, HSTS, `Secure` i `HttpOnly` na ciasteczkach sesji i CSRF, `SameSite=Lax`.
- Formularze mają token CSRF. Quiz ma test limitu częstości.
- HTML z middleware dostaje `Cache-Control: no-cache, no-store, must-revalidate, max-age=0`. Potwierdzone na `/walczak/`, `/walczak/spis/` i `/walczak/test/`.
- Traceback na ścieżce Walczaka przy włączonym DEBUG jest technicznym 404 Django. Handler produkcyjny jest osobno.

## 12. HTTP, SEO, wydajność

Canonical buduje się z schematu, hosta i ścieżki. Strony sesyjne mają `noindex`: test, dopasowanie, quiz, wynik, szkic, fakt, pusta rodzina. Porównanie pary i katalog zostają do indeksu. Hreflang nie jest dodany.

Warunki laboratorium: Windows 10, localhost `127.0.0.1:8765`, `runserver`, osadzony Chromium Cursora, bez dławienia sieci i CPU. Jeden przebieg. To nie jest 75. percentyl w polu.

| Strona | Szerokość CSS | TTFB | DCL | Load | LCP | CLS |
| --- | --- | --- | --- | --- | --- | --- |
| `/walczak/spis/` | 1265 | 22 ms | 82 ms | 88 ms | 1040 ms, element `P`, 37752 B | 0 |
| `/walczak/test/` | 1280 | 18 ms | 150 ms | 164 ms | 928 ms | 0 |
| `/walczak/` | desktop | 11 ms | — | — | nie złapany | 0 |

INP: brak wpisów event timing. Niezweryfikowany.

## 13. Przeglądarka i urządzenia

Silnik: osadzony Chromium. Chrome i Edge są w systemie; Edge nie był klikany osobno. Firefox, Safari i iOS nie są zainstalowane.

Szerokości spisu: 320, 360, 390, 640, 768 (układ 753 px z paskiem), 1265. Overflow 0. Konsola nie była nagrywana przez całą sesję. Timing zasobów spisu: 13 żądań, zero statusów ≥ 400.

## 14. Testy automatyczne

- `python -m ruff check walczak config/views.py config/test_views_urls.py` → All checks passed.
- `python -m mypy walczak` → Success: no issues found in 26 source files. Notatka `annotation-unchecked` na `walczak/tests/test_mvp.py:155`.
- `python -m pytest -q --tb=line` → 569 passed, 1 skipped, 13 warnings, 261,35 s, exit 0. Ten przebieg jest sprzed podkreślenia linków. Podkreślenie jest w CSS i zostało sprawdzone axe-core na karcie, liście dopasowania i pozostałych stronach z tabeli WCAG.
- Walidator treści: exit 0, same WARNING co wyżej.

## 15. Niezweryfikowane

- Narrator i inny czytnik ekranu.
- Firefox, Safari, iOS.
- Edge jako osobny przebieg.
- INP.
- Polowe LCP, INP i CLS.
- Wizualne wysunięcie skip linku po prawdziwym Tab, gdy okno ma fokus systemu.
- Ręczne otwarcie każdego URL-a źródła.
- Dwujęzyczne 404 w przeglądarce przy `DEBUG=False`. Pokrywa je `test_walczak_missing_path_uses_the_app_page`.

## 16. Co mogą pokazać dopiero obcy użytkownicy

Czy zdanie o 22 osiach jest zrozumiałe. Czy lista pięciu stylów brzmi jak lektura, a nie jak werdykt. Czy żart jest żartem. Czy szkic przy pozycjach odwróconych nie jest czytany jako „średnia zgody”. Czy angielski przełącznik wystarcza osobie, która nie czyta polskiego opisu w `meta`.

## 17. Pliki tego przebiegu

- `walczak/views.py`
- `walczak/preference.py`
- `walczak/serializers.py`
- `walczak/static/walczak/css/walczak.css`
- `walczak/tests/test_mvp.py`
- `walczak/tests/test_views.py`
- `walczak/templates/walczak/404.html`
- `walczak/templates/walczak/base.html`
- `walczak/templates/walczak/home.html`
- `walczak/templates/walczak/list.html`
- `walczak/templates/walczak/match.html`
- `walczak/templates/walczak/test.html`
- `walczak/templates/walczak/quiz.html`
- `walczak/templates/walczak/personality.html`
- `walczak/templates/walczak/result.html`
- `walczak/templates/walczak/empty.html`
- `walczak/templates/walczak/compare_form.html`
- `walczak/templates/walczak/compare.html`
- `walczak/templates/walczak/detail.html`
- `walczak/templates/walczak/golden.html`
- `walczak/templates/walczak/fact.html`
- `config/views.py`
- `config/test_views_urls.py`
- `docs/walczak-release-audit.md`

## 18. Komendy

```text
python manage.py validate_walczak_content
python -m mypy walczak
python -m ruff check walczak config/views.py config/test_views_urls.py
python manage.py check
python manage.py check --deploy
python -m pytest -q --tb=line
python manage.py runserver 127.0.0.1:8765 --noreload
```

`check --deploy` dostał `DJANGO_DEBUG=false`, `DJANGO_TESTING=true`, `DJANGO_ALLOWED_HOSTS=example.com`, `DJANGO_CSRF_TRUSTED_ORIGINS=https://example.com`, `CORS_ALLOWED_ORIGINS=https://example.com` i sekret dłuższy niż 50 znaków. Po komendzie środowisko lokalne wróciło do debug.
