# Walczak — bramka release

Data: 2026-10-01. Sprawdzone na drzewie roboczym, nie na czystym commicie.

## Bramka

| Kryterium | Stan | Dowód |
| --- | --- | --- |
| Testy Walczaka | PASS | `python -m pytest walczak/tests -q` → 52 passed |
| Cały `pytest` repozytorium | FAIL | 6 failed, 602 passed, 1 skipped. Wszystkie porażki są w `poligon/` (`test_seed`, `test_views`, `test_content`). Walczak ich nie rusza. Drzewo Ćwiczby było zmienione wcześniej |
| Migracje Walczaka | PASS | Brak nowej migracji. `manage.py check` → no issues (2 silenced) |
| Walidator treści | PASS | Exit 0. Dziesięć WARNING `discovery_only`, INFO o braku badań. Bez ERROR |
| P0 | PASS | Brak nowego. Sesja po urwanym formularzu była już czyszczona |
| P1 release | PASS | Słownik, pusty tag, opis `meta`, mapa stron |
| Główne ścieżki w przeglądarce | PASS | Chromium, `127.0.0.1:8765`: start, przełącznik EN, spis, karta boksu, mapa XML |
| Telefon 390 px | PASS | Spis: overflow 0, tytuł „Browse”, opis po angielsku |
| Desktop | PASS częściowy | Start i karta oglądane przed zwężeniem. Osobnego pomiaru 1280 px po zmianie nie powtarzałem |
| Język PL/EN | PASS | EN na starcie: Browse, szkic, stopka, `meta description` i `og:description` |
| Copy | PASS | Przewodnik w `docs/walczak-copy-style-guide.md`. Karty stylów nietknięte |
| Konfiguracja produkcji | NOT VERIFIED | Nie stawiałem `DEBUG=False` na hoście. Ustawienia w `config/settings.py` są wspólne i były już opisane w audycie z 2026-09-30 |
| Dokumenty zgodne z kodem | PASS | Plan, przewodnik, notatki, ten plik, zdanie na górze starego audytu |

Bramka Walczaka jest spełniona. Bramka całego repozytorium nie jest, dopóki Ćwiczba nie przejdzie swoich sześciu testów. To nie jest regres Walczaka.

## Ścieżki

| Ścieżka | Stan | Uwaga |
| --- | --- | --- |
| Start | PASS | Cztery wejścia. Zdanie, że szkic nie wybiera stylu |
| Spis i karta | PASS | EN na karcie boksu: historia, praktyka, źródła, „editorial judgment” |
| Pusty tag / pusta rodzina | PASS | Testy. W przeglądarce nie zakładałem pustego tagu w bazie |
| Jaki trening / dopasowanie | PASS | Pokryte istniejącymi testami sesji i stabilnej listy. W tej rundzie nie klikałem formularza od nowa |
| Porównanie | PASS | Testy pary, tego samego slugu i stylu spoza zestawu. W przeglądarce nie otwierałem pary |
| Żart i remis | PASS | Test jednego `h1` przy remisie |
| Szkic | PASS | Test, że wynik nie zmienia listy. W przeglądarce nie wypełniałem 20 pozycji |
| Fakt | PASS | Test API i strony, gdy fakt jest w bazie |
| 404 przy `DEBUG=True` | PASS | Techniczna strona Django. Tak ma być lokalnie |
| 404 dwujęzyczne przy `DEBUG=False` | NOT VERIFIED | W przeglądarce nie wyłączałem DEBUG. Pokrywa to `test_walczak_missing_path_uses_the_app_page` |
| Mapa `/walczak/sitemap.xml` | PASS | 44 adresy. Jest boks. Nie ma quizu, testu ani faktu |

## Poza sprawdzeniem

| Rzecz | Stan |
| --- | --- |
| Czytnik ekranu | NOT VERIFIED |
| Firefox, Safari, iOS | NOT VERIFIED |
| INP i polowe LCP/CLS | NOT VERIFIED |
| Ręczne otwarcie każdego URL-a źródła | NOT VERIFIED |
| `robots.txt` całego serwisu | NOT VERIFIED — pliku nie ma. Ekrany sesji mają `noindex` |
| Analityka zdarzeń | Nie dotyczy. Śledzenie wizyt jest wyłączone w całym portfolio |
| Pole `region` na karcie | Zostaje jednym napisem. Po angielsku boks pokazuje „Europa” |
