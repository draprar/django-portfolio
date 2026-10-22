# AFC Rugby — raport wdrożenia (lokalnie)

Gałąź: `feature/afc-rugby-refresh` w repozytorium `django-portfolio` (kanoniczna kopia; równoległy folder `django-portfolio-rugby` można usunąć).

## Zrobione

- Odświeżona `/rugby/`: hero, rugby w pigułce + boisko + punktacja, mapa (lokalny SVG Natural Earth), AFC w skrócie, ślady, oś (7 punktów + pożegnanie), 3 relacje z `rugby/data/accounts.py`.
- Widok nie odpytuje `Post`; model i admin nietknięte.
- Lightbox (5 obrazów), YouTube osobno; skan encyklopedii z zacemnionym kontaktem (`rugby/private/scans/pzr_original.png`).
- Testy: `pytest rugby/tests/test_views.py` — 9 passed.

## Linki klubów

- Orkan, Legia: profil PZR (domeny 403/SSL).
- Pozostałe: zweryfikowane domeny klubów.

## Otwarte (właściciel)

- Prawa do fotografii / wizerunku na zdjęciu grupowym i skanach — wymaga potwierdzenia.
- Folder worktree `django-portfolio-rugby` można usunąć ręcznie (permission denied przy `git worktree remove`).

## Deploy

- Brak migracji modeli; po merge: standardowy deploy + `collectstatic`.
- Rollback: nie merge’ować gałęzi lub revert PR.

## Produkcja

Nie łączono z produkcyjną bazą; brak push/deploy w tej sesji.
