# Ingest for Poligon

Public training content enters through JSON files listed in `poligon/data/manifest.json`. `seed_poligon` loads them with `update_or_create` and does not delete learner submissions.

## What may be seeded

- Original exercises in `poligon/data/exercises/`. The shipped catalog keeps only military-relevant items (205 exercises; 5 active per level and skill). Listening, speaking, and writing prompts are written for this project. Reading on levels 1–5 may use a shortened English Wikipedia or Simple English summary when `wiki_curriculum.json` supplies a title; the question and choices on those items are original and the card carries CC BY-SA attribution. Level 0 reading is original. Run `python poligon/data/prune_military_catalog.py` after regenerating JSON to drop civilian filler.
- Vocabulary is 1173 cards after the military prune. `vocabulary/original.json` and `vocabulary/wiktionary.json` stay on level 2. Extra level-2 cards and the other levels live in `vocabulary/level-*.json`. The English definition comes from the public Wiktionary REST API, stored with the page URL, the retrieval date, and `CC BY-SA 4.0`. Polish glosses are original. An example sentence from Tatoeba is added only when that sentence has a CC BY license.

`build_catalog.py`, `build_levels.py`, `build_max_catalog.py`, `fetch_tatoeba.py`, and `fetch_wikipedia.py` are offline builders. Production, tests, and CI do not call them and do not use the network to fill content. Builder caches stay out of git.

## Staging metadata

Keep these fields before a row becomes public vocabulary:

```text
content_source      original | wiktionary | wikipedia | tatoeba | wikidata
source_url
source_license
retrieved_at
attribution_en
attribution_pl
```

Only rows with a compatible license and a checked source are promoted. `rights_verified` for the current Wiktionary set is the presence of `source_url`, `source_license`, and `retrieved_at` together.

## Rule

Reference standards stay in `sources_registry.json`, which is an internal record and is not served to learners. They are not copied into exercises. If a source has unclear licensing, it stays in the provenance notes and is not promoted into public training content.
