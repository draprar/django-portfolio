# AFC Rugby — źródła mapy klubów (okno 21.10.2016–21.10.2026)

Audyt zaktualizowany: **22 października 2026**. Okno ruchome: mecze i turnieje z datą w przedziale **2016-10-21 … 2026-10-21**. Każdy wpis sezonu w JSON ma pole `evidence_type` (`final_table`, `group_roster`, `played_result`, `snapshot`).

- **Kanon:** `rugby/data/club-history.json`
- **Sync z tabel PZR:** `python -m rugby.data.sync_club_seasons` (wymaga `pypdf` do przewodników PDF; nie nadpisuje klubów `historic`)
- **Runtime:** `rugby/data/places.py` — w dymku sezony tylko ze statusu `potwierdzony` lub `w_toku`

Mapa **nie jest kompletna** dla całego dziesięciolecia. `map_data_incomplete` pozostaje `true` m.in. przez Ekstraligę **2026/27** (`w_toku`, `evidence_type: snapshot` do 2026-10-21) oraz **brak PLR7 2025/26 i 2026/27** (nie wymyślać URL sezonu).

## Zakres rozgrywek

- **Ekstraliga Rugby** (rugby XV)
- **Męska Polska Liga Rugby 7 (PLR7)**
- Wyłączone: II liga, MP rugby 7, kobiety, młodzież, puchar, **Barbarians**, rezerwy („II” w nazwie w sync)

---

## Raport sezon po sezonie (stan po sync v11)

### Ekstraliga

| Sezon | Źródło (główne) | evidence_type | Status | Uwagi |
| --- | --- | --- | --- | --- |
| 2016/17 | [artykuł PZR 2302](https://polskie.rugby/artykul/2302/ekstraliga-rozgrywki-2016-2017) | `group_roster` | `potwierdzony` | 8 drużyn w grupach A/B — nie tabela końcowa |
| 2018 | [Kalendarz Fazy II](https://polskie.rugby/artykul/4359/ekstraliga-kalendarz-fazy-ii) | `snapshot` | `potwierdzony` | Tabele faz w treści artykułu |
| 2019 | [finał 2019](https://polskie.rugby/artykul/5118/ekstraliga-ogniwo-mistrzem-polski) + [tabela legacy](http://pzrugby.pl/tabele/Tabelawynikiterminarz,52) | `final_table` | `potwierdzony` | Supplemental: [5004](https://polskie.rugby/artykul/5004/ekstraliga-aktualna-tabela) (migawka, nie finał) |
| 2019/20 | [COVID / przerwanie](https://polskie.rugby/artykul/12002/od-pucharu-ajencji-wschodniej-do-ekstraligi) | — | brak wpisów | Tylko `played_result` z rozegranych meczów — **nie** w sync |
| 2020/21 | [PDF przewodnik](https://polskie.rugby/storage/files/Ekstraliga%202021.pdf) | `final_table` | `potwierdzony` | Parser PDF (`pypdf`) |
| 2021/22 | [PDF wiosna 2022](https://polskie.rugby/storage/files/Ekstraliga%20Rugby%20-%20Wiosna%202022.pdf) | `final_table` | `potwierdzony` | Parser PDF |
| 2022/23 | [sezon/1](https://polskie.rugby/sezon/1/ekstraliga-rugby-20222023) | `final_table` | `potwierdzony` | 10 club_id |
| 2023/24 | [sezon/9](https://polskie.rugby/sezon/9/ekstraliga-rugby-20232024) | `final_table` | `potwierdzony` | 8 club_id (9 drużyn w tabeli) |
| 2024/25 | [sezon/23](https://polskie.rugby/sezon/23/ekstraliga-rugby-20242025) | `final_table` | `potwierdzony` | 9 club_id |
| 2025/26 | [sezon/32](https://polskie.rugby/sezon/32/ekstraliga-rugby-20252026) | `final_table` | `potwierdzony` | 10 club_id |
| 2026/27 | [sezon/39](https://polskie.rugby/sezon/39/ekstraliga-rugby-20262027) | `snapshot` | `w_toku` | Tabela częściowa do **2026-10-21** (`as_of` w JSON) |

### PLR7 (mężczyźni)

| Sezon | Źródło | evidence_type | Status | Uwagi |
| --- | --- | --- | --- | --- |
| 2016–2019 | — | — | brak | Bez sztucznych lat |
| 2020 | [wznowienie](https://polskie.rugby/artykul/6259/weekend-z-rugby-19-20092020) | — | brak | Kontekst, nie tabela klubów |
| 2021 | [VIII turniej Poznań](https://polskie.rugby/artykul/7136/plr7-viii-turniej-w-poznaniu) | `snapshot` | `potwierdzony` | Klasyfikacja po 8 turniejach — nie pełny cykl |
| **2022/23** | [sezon/5](https://polskie.rugby/sezon/5/polska-liga-rugby-7-20222023) | `final_table` | `potwierdzony` | Supplemental: [8892 Poznań](https://polskie.rugby/artykul/8892/plr7-v-turniej-w-poznaniu) |
| 2023/24 | [sezon/12](https://polskie.rugby/sezon/12/polska-liga-rugby-7-20232024) | `final_table` | `potwierdzony` | ~15 club_id |
| 2024/25 | [sezon/27](https://polskie.rugby/sezon/27/polska-liga-rugby-7-20242025) | `final_table` | `potwierdzony` | 8 club_id |
| 2025/26 | — | — | **brak** | `/kategoria/59/` i regulamin MPS R7 **nie** są dowodem PLR7 |
| 2026/27 | — | — | **brak** | Jak wyżej |

---

## Mapa — spiderfy i dymek (v11)

- **Kreski:** `map.js` — `getScreenCTM().inverse()` na SVG `.map-leaders`; odświeżanie po zoom/pan/resize/spiderfy.
- **Próg skupiska:** 28 px (jeden próg dla klastra i rozsunięcia).
- **Dymek:** hover (chwilowy) vs **pin** (klik); `hideCard` nie zeruje pinu; zamknięcie / Esc / filtr ligi → `unpin`.
- **Giżycko (`historic`):** bez linii spiderfy.

## Geometria mapy

- Podkład: Natural Earth 50m → `rugby/static/rugby/img/map-europe.svg`
- Projekcja: Web Mercator (`rugby/views.py`, `rugby/static/rugby/js/map.js`)

## Marker historyczny

- **Giżycko (`gizycko`)** — `historic`, `seasons: []`, link `#afc-farewell`

## Indeks źródeł (pomocniczy, niepubliczny)

- `rugby/private/scans/afc_rugby_season_sources_2016_2026 (2).json` (i `.md`, `.csv`)

## Testy

```bash
python -m pytest rugby/tests/test_views.py
```

Ostatni przebieg: **27 passed** (2026-10-22).
