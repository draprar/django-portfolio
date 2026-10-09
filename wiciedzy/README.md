# wiciędze (app `wiciedzy`, label `walczak`)

## Source of truth

- Catalog data: `data/styles.py`, `data/prose.py`, `data/instruments.py`

### Quizopasowanie (`instruments.py`) and deploy

Preference questions live in the **database** after `import_wiciedzy`. Code-only changes are not enough for production.

- **Render / CI:** `migrate` then `import_wiciedzy` (see `render.yaml`, `.github/workflows/ci.yaml`).
- **Reorder, new copy, or new questions:** add a data migration that runs `import_wiciedzy` on deploy (pattern: `migrations/0009_preference_order_copy.py`). Import matches rows by scale `dimension` or choice `text_en`, then sets `sort_order`.
- Do not rely on a manual import on the server after merge; the PR should ship everything needed for migrate-only deploys.

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
