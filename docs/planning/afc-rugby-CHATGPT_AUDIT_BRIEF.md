# AFC Rugby Giżycko — brief do audytu (ChatGPT / zewnętrzny)

**Data:** 22 października 2026  
**Autor kontekstu:** Walery  
**Gałąź robocza:** `feature/afc-rugby-refresh`  
**URL:** `/rugby/` w portfolio Django (jedna długa strona, PL/EN, `localStorage` → `rugby_lang`)

Cel: wkleić ten plik do ChatGPT (lub innego audytora bez repo) **razem z PNG z sekcji 8A** (pełna strona). Opcjonalnie: pliki z tabeli must-have i `afc-rugby-final-audit.md`.

---

## 1. Czym jest strona

- Archiwum inicjatywy **AFC Rugby Giżycko** (rugby 7, 2008–2010) w hubie portfolio.
- Sekcje: hero, rugby w pigułce + **interaktywne boisko** (7 faz + 5 przycisków punktacji), **mapa klubów** (Ekstraliga + PLR7, ostatnie 10 lat, dane z PZR / `club-history.json`), AFC w skrócie, ślady (media + lightbox), oś czasu, wybrane relacje z archiwum, stopka ze zdjęciem drużyny (link do portfolio).
- **Nie** dodawaj nowych sekcji, CMS, dźwięku, animacji „marketingowych” ani fikcyjnych faktów.
- Mapa **nie jest kompletna** — tylko sezony z potwierdzonym źródłem; szczegóły w `docs/planning/afc-rugby-map-sources.md`.

### Co zmieniło się w v11 (2026-10-22) — ważne dla audytu wizualnego

- `<main id="main-content">`, skip-link, loader + `rugby:lang`, scroll-spy z `aria-current="location"` (bez „bieżącej” sekcji Kontakt do portfolio).
- Boisko: punktacja jako **5× `button.scoring-btn`** (podgląd w `pitch.js`, bez zmiany wyniku fazy).
- Mapa: hover vs **pin**; kreski do dymku przez `getScreenCTM().inverse()`; **markery SVG** (kółko + pierścień + diament AFC), legenda też SVG; skupiska rozsuwane tylko przy otwartym klastrze (nie „na starcie” w Bałtyku).
- **Cel kliknięcia (AIM):** cały przycisk markera ma `scale: 1/zoom` — kursor na kropce = trafienie w ten sam klub (wcześniej skala tylko na `.map-marker-dot`).
- Stopka: usunięty hub `.rugby-footer-hub`; zdjęcie z delikatnym scrimem (`opacity`, gradient).
- Dane: `evidence_type` w JSON; sync starszych sezonów + PLR7 2022/23 (`/sezon/5/`); brak PLR7 2025/26–26/27.

---

## 2. Co audytować

1. **UI/UX** — czytelność, odstępy (nagłówki, złota kreska pod `h2`, panele sekcji), mobile, **mapa** (markery, legenda, skupiska, dymek), boisko, lightbox, menu, stopka.
2. **Copy PL/EN** — spójność tonu archiwum, para `data-pl` / `data-en`, bez dopisywania wydarzeń.
3. **Dostępność** — skip-link, focus, `aria-*` na mapie (przyciski klubów), punktacja (`aria-pressed`), kontrast.
4. **Mapa i dane** — czy komunikat o niekompletności jest uczciwy; czy dymek klubu nie obiecuje więcej niż JSON; czy legenda „oba ligi” jest czytelna.
5. **Regresje vs wcześniejsza wersja** — jeśli masz stary zrzut (`rugby-app-fullpage-2026-10-21.png`) lub Wayback / GitHub Pages (linki w sekcji pożegnania), porównaj układ i copy.

---

## 3. Pliki repozytorium — co warto dać ChatGPT (kolejność)

### Must-have (treść + UI)

| Plik | Po co |
|------|--------|
| `rugby/templates/rugby/base.html` | szkielet, loader, OG, main |
| `rugby/templates/rugby/navbar.html` | nawigacja, PL/EN |
| `rugby/templates/rugby/hero.html` | hero |
| `rugby/templates/rugby/basics.html` | pigułka + boisko |
| `rugby/templates/rugby/partials/pitch_svg.html` | SVG boiska |
| `rugby/templates/rugby/places.html` | mapa (SVG markery, legenda) |
| `rugby/templates/rugby/info.html` | AFC w skrócie |
| `rugby/templates/rugby/media.html` | ślady |
| `rugby/templates/rugby/about.html` | historia + relacje |
| `rugby/templates/rugby/footer.html` | stopka / hub |
| `rugby/static/rugby/css/style.css` | wygląd całości (mapa, stopka) |
| `rugby/static/rugby/js/lang.js` | i18n |
| `rugby/static/rugby/js/map.js` | mapa, spiderfy, dymek, skala markerów |
| `rugby/static/rugby/js/pitch.js` | fazy boiska, punktacja |
| `rugby/static/rugby/js/scroll.js` | scroll-spy, navbar |
| `rugby/static/rugby/js/enhancements.js` | lightbox itd. |
| `rugby/views.py` | kontekst widoku, `map_data_incomplete` |
| `rugby/data/places.py` | loader mapy z JSON |
| `rugby/data/club-history.json` | kanon sezonów klubów |
| `rugby/tests/test_views.py` | oczekiwane zachowanie HTTP |

### Kontekst planowania (bez obowiązku wklejania całości)

| Plik | Po co |
|------|--------|
| `docs/planning/afc-rugby-map-sources.md` | źródła mapy, luki sezonów |
| `docs/planning/afc-rugby-final-audit.md` | domknięcie v11, pytest vs ręczne scenariusze |
| `docs/planning/afc-rugby-final-report.md` | szerszy raport wdrożenia (jeśli istnieje) |
| `rugby/data/sync_club_seasons.py` | skąd biorą się sezony w JSON |

### Nie wgrywaj do ChatGPT (prywatne / binarne)

- `rugby/private/scans/*` (skany PZR — tylko przy NDA)
- duże obrazy w `rugby/static/rugby/img/` (wystarczy PNG pełnej strony)

---

## 4. Wynik audytu (format odpowiedzi)

1. **Findings** — UI, copy, mapa, a11y, mobile; priorytet 🔴 / 🟡 / 🟢.
2. **Konkretne poprawki** — dla każdej: który blok HTML (`#info`, `#places`, …) i gotowy tekst PL + EN (jeśli dotyczy copy).
3. **Regresje vs stara wersja** — tabela: było / jest / rekomendacja (jeśli masz punkt odniesienia).
4. **Top 5 na najbliższy tydzień** (Walery wdraża w Django).
5. **Pytania do Walerego** — max 5, tylko decyzje produktowe.

Język odpowiedzi: **polski**.

---

## 5. Prompt startowy (skopiuj z briefem)

```
Przeczytaj brief „AFC Rugby Giżycko — brief do audytu” (2026-10-22) i załącznik: zrzut pełnej strony rugby-app-fullpage-2026-10-22.png. Opcjonalnie dołącz afc-rugby-final-audit.md i wybrane pliki z tabeli must-have. Zrób audyt UI/UX, copy PL/EN i mapy (markery SVG, dymek, niekompletność danych). Nie proponuj nowych sekcji ani faktów spoza materiałów. Zwróć wynik w formacie z sekcji 4 briefu.
```

---

## 6. Załączniki dla ChatGPT

### A. Bieżąca aplikacja — pełna strona (zrzut) — **WYMAGANE**

Plik w repo (wygenerowany **2026-10-22**, desktop **1280×10185 px**, pełna wysokość scrolla, `/rugby/`):

`docs/planning/afc-rugby-audit-assets/rugby-app-fullpage-2026-10-22.png`

**Do uploadu w ChatGPT:** ten PNG + ten brief `.md`.

Opcjonalnie: dodatkowe kadry `#places` (mapa, pin + dymek), `#basics` (boisko + punktacja), `#info` (nagłówek + karty).

Archiwum porównawcze (poprzedni zrzut): `rugby-app-fullpage-2026-10-21.png` (ten sam folder).

### B. Poprzednia treść (opcjonalnie)

- Linki w sekcji pożegnania: **Wayback Machine**, **GitHub Pages**.
- Tekstowy zrzut starej strony: jeśli masz lokalnie `rugby-stan-strony-do-audytu.md`, dołącz; w repo może go nie być.

### C. Skany prywatne

Tylko przy świadomej decyzji i NDA — patrz sekcja 3.

---

## 7. Stan techniczny (skrót)

- **Testy:** `python -m pytest rugby/tests/test_views.py` — **27 passed** (2026-10-22).
- **Dane mapy:** `python -m rugby.data.sync_club_seasons` → `rugby/data/club-history.json`.
- **`map_data_incomplete`:** `true`, dopóki są sezony `w_toku` / luki w źródłach (patrz `afc-rugby-map-sources.md`).
- **Ręcznie w przeglądarce** (nie zastępuje pytest): mapa hover/pin/Esc; skupisko desktop vs mobile (double-tap); 5 przycisków punktacji; jeden `aria-current="location"`; stopka i kontrast zdjęcia — lista w `afc-rugby-final-audit.md` § „Do ręcznej weryfikacji”.

---

## 8. Luki znane (nie traktuj jako bugów bez kontekstu)

- Ekstraliga 2019/20 — brak pełnej tabeli końcowej w źródle (`played_result` per mecz).
- PLR7 2025/26–26/27 — brak publicznego źródła w sync.
- Warszawa — jeden marker `warszawa-ligi` (Skra/Legia/AZS AWF razem).
- Decyzje redakcyjne (MTS, WMPD, alt plakatów, sformułowania w timeline) — do autora; wymienione w `afc-rugby-final-audit.md`.
