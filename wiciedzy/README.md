# wiciędze (app `wiciedzy`, label `walczak`)

## Source of truth

- Catalog data: `data/styles.py`, `data/prose.py`, `data/instruments.py`
- Editorial mirror: `katalog-opisy.md`, `quizopasowanie.md`
- Templates under `templates/wiciedzy/`

## Generated artifacts (do not hand-edit)

Regenerate with:

```bash
python manage.py import_wiciedzy
python manage.py export_wiciedzy_texts
python manage.py export_wiciedzy_texts --polish-only --plain -o wiciedzy/teksty-pl.txt
```

Files:

- `teksty-eksport.md` — PL/EN mirror of live UI + catalog
- `teksty-audyt-eksport.md` — same pipeline with audit-oriented header (when built via `build_audyt_prompt.py`)
- `teksty-pl.txt` — Polish plain extract

Legacy: `teksty.md` (superseded by the exports above).

## Validation

```bash
python manage.py validate_wiciedzy_content
```

Exits with code 1 on ERROR (catalog/relation integrity). Warnings include discovery-only second sources.
