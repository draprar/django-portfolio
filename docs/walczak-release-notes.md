# Walczak — notatki release

Data: 2026-10-01.

Produkt zostaje tym, czym był: katalog, lista do czytania, porównanie, żart i szkic. Ta runda domyka słownik i rzeczy widoczne dla indeksu. Nie dodaje ścieżek.

## Zmienione

- Spis mówi o stylach, nie o dyscyplinach.
- Angielskie „Poznaj” to „Browse”, nie „Discover”.
- Na liście do czytania zestaw rzadszy nazywa się „Mniej oczywiste”, tak jak osobna strona.
- Pusty tag mówi, że żaden styl go nie ma. Pusta rodzina dalej mówi o rodzinie.
- Start dopowiada, że szkic jest w menu, liczy pięć liczb i nie wybiera stylu.
- Opis porównania to dwie nazwy, nie skrót jednej karty.
- `meta description` i `og:description` mają parę PL/EN. Przełącznik języka podmienia też `content` w `meta`.
- Publiczne strony mają `og:title`, `og:type` i `og:url`. Po zmianie języka tytuł Open Graph bierze się z tytułu dokumentu.
- Jest `/walczak/sitemap.xml`: start, spis, mniej oczywiste, formularz porównania i aktywne karty.
- API katalogu może być cache’owane przez 300 sekund. Losowy fakt ma `Cache-Control: no-store`.

## Naprawione

- Pusty filtr tagu nie obwiniał rodziny.
- Opis strony zostawał po polsku, gdy czytelnik przełączył angielski. Dotyczy elementów `meta` z `data-pl` i `data-en`. Reszta serwisu takich meta nie ma.

## Ulepszone

- Słownik PL/EN jest zapisany w `docs/walczak-copy-style-guide.md`.
- Plan produktu, bramka i te notatki opisują ten sam kod.

## Poza zakresem

- Nowe style i „uzupełnianie” dziesięciu kart, których drugie źródło tylko wskazuje temat. Zostają jako WARNING.
- Badania psychologiczne przy porównaniu. Brak jest jawny i zamierzony.
- Statusy DRAFT / APPROVED w bazie. Publikacja to `active` plus pliki w `walczak/data/`.
- Zdarzenia analityczne. Śledzenie wizyt w portfolio jest wyłączone.
- `robots.txt` dla całego serwisu i hreflang. Ekrany sesji mają `noindex`.
- Procent dopasowania, kluby, mapy, ceny, łączenie szkicu ze stylem.
- Czytnik ekranu, Firefox, Safari, iOS i polowe Core Web Vitals. Nie były sprawdzane w tej rundzie.
