# AFC Rugby v11 — raport po audycie

Gałąź: `feature/afc-rugby-refresh`. Data domknięcia v11: **2026-10-22**.

## Bramka grep (plik:linia)

| Wzorzec | Trafienia (stan przed v11) |
|--------|----------------------------|
| `<!DOCTYPE` w `base.html` | brak → dodano |
| `sr-only` w `rugby/` | `basics.html`, `about.html`, `map.js:187` → `visually-hidden` |
| `background-attachment` | `style.css:61` → usunięte |
| `.map-marker-label` + `display: none` | `style.css:1234` → usunięte |
| `.map-marker--both` | `style.css` (bez pierścienia) → styl `both` + legenda |
| `x1="62"` słupy | `pitch_svg.html:11` → `124` / `876` |
| `_infer_source_url`, `map_data_incomplete: True` | `views.py` → JSON + liczenie z danych |
| `keydown` Escape menu | tylko toggler → toggler + `#navbarCollapse` |

Potwierdzone bez zmian (zgodnie z planem): `#map-card` `position: fixed`, `clampScale` max 10, `scroll.js` tylko `.scrolled`, brak `data-aos` w szablonach, centrowanie markerów przez `margin`.

## Naprawione i potwierdzone (pytest + kod)

- DOCTYPE, `<main id="main-content">`, skip-link `#main-content`, `noscript` dla loadera, OG meta, Bootstrap `defer`, Font Awesome usunięty z `#topBtn` (SVG inline).
- `window.__rugbyLangReady`, loader na `rugby:lang` + flaga; ikony lightbox i top: `data-aria-*`.
- `visually-hidden`, lead mapy bez „repozytorium”, `map_data_incomplete` z `club-history.json`.
- Kanon danych: `rugby/data/club-history.json`; `places.py` ładuje JSON; usunięty `static/.../club-history.json`.
- Etykiety miast PL/EN, usunięte `display: none` na labelach; dwuetapowy tap skupiska (bez ustawiania `openCluster` w `click`).
- Słupy na linii końcowej, martwe `#phase-scrum` / `#phase-maul`; reset `.phase-mark` przy zmianie fazy.
- Escape w menu mobilnym na `collapse` i togglerze; scroll-spy bez świecenia AFC na hero/mapie.
- Mapa: leader lines przez `getScreenCTM().inverse()`, hover vs pin, styl `both`, cele 44px, projekcja przez `json_script`, `pzr_profile_url` w dymku.
- Punktacja: 5× `button.scoring-btn` + `pitch.js` (podgląd bez zmiany wyniku fazy; reset przy zmianie kroku).
- Scroll-spy: `aria-current="location"`; Kontakt do portfolio wyłączony z bieżącej sekcji.
- Stopka: usunięty `.rugby-footer-hub`; zdjęcie drużyny z `alt` PL/EN, wymiary, `loading="lazy"`.
- Sezony: `evidence_type` w `club-history.json`; sync starszych sezonów + PLR7 2022/23 (`/sezon/5/`); brak PLR7 2025/26–26/27.
- Media: `data-alt-*` na `<img>`, archiwum EN lead, pożegnanie w `blockquote.farewell-quote`.

## Testy Django (automatyczne)

`pytest rugby/tests/test_views.py` — **27 passed** (2026-10-22), m.in. `main-content`, 5 przycisków punktacji, brak `.rugby-footer-hub`.

## Do ręcznej weryfikacji w przeglądarce (desktop + telefon)

Scenariusze z promptu v11 — **nie** zastępują pytest:

1. Mapa: hover markera → dymek; przejście kursora na dymek; klik = pin; Zamknij / Esc = unpin; filtr ligi zamyka pin.
2. Skupisko: desktop — kreski tylko przy otwartym klastrze, bez „słupów”; mobile — pierwszy tap rozsuwa, drugi otwiera dymek.
3. Plansza: 5 przycisków punktacji (`aria-pressed`, Enter/Spacja); wynik fazy bez zmian; zmiana fazy czyści podgląd.
4. Nawigacja: jeden link z `aria-current="location"`; Kontakt nigdy nie jest bieżącą sekcją `/rugby/`.
5. Złota kreska pod `h2` w `#info` — symetryczny odstęp.

Niezweryfikowane wizualnie w tej sesji: loader ≤300 ms, parallax hero, kolor linków PZR w Computed.

## Luki i decyzje

- **Sezony / URL PZR:** patrz `docs/planning/afc-rugby-map-sources.md` (sezon po sezonie, `evidence_type`). Luki: Ekstraliga 2019/20 (`played_result` per mecz), PLR7 2025/26–26/27. Mapa **nie** jest kompletna.
- **Warszawa:** jeden marker `warszawa-ligi` (bez rozbicia na 3 — wachlarz nie testowany przy max zoom).
- **Kółko na mapie / brak obrońców na boisku:** bez zmian merytorycznych (plan autora).
- **Redakcja:** MTS, WMPD PUDiZ, Bors, Misiak, czerwiec 2008, „wybraliśmy” vs „odtworzyłem”, prawa do sześciu śladów, alt plakatów spotkanie/nabór — do decyzji autora.
- **Martwy CSS:** accordion / część timeline-image — grep pozostaje; pełne wyczyszczenie odłożone.

## Skany prywatne

Pliki w `rugby/private/scans/` nie trafiają do staticów ani wdrożenia; służą weryfikacji źródeł w Cursorze.
