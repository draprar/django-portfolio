# Content policy for Ćwiczba

Ćwiczba is an unofficial self-study trainer inside this portfolio. It is not an official proficiency assessment and it does not ship restricted test material. The public description does not present it as a STANAG or NATO product.

1. **Original first.** Exercise texts, prompts, answer choices, explanations, and audio scripts are written for this project.
2. **Reference, don't mirror.** Public standards can inform the competency target. Verbatim descriptors or test items from restricted publications do not go into the public data set.
3. **No official branding.** Ćwiczba does not ship official logos or other brand assets.
4. **Third-party audio must be licensed.** Browser speech synthesis is only a stand-in.
5. **Open-data imports stay traceable.** The catalog on disk is 237 practice exercises and 1173 vocabulary cards. The live queue is every practice exercise with `publication_status=published` (32 older items marked `legacy`, plus 20 reviewed items, one for each level and skill). `active_slugs.json` remains only so older migrations can find that first queue. Wiktionary English definitions keep the source URL, retrieval date, `CC BY-SA 4.0`, and an on-card attribution. A Tatoeba example is stored only when the API returns a CC BY license, sentence id, and author. A reading item may use one shortened English Wikipedia or Simple English summary (about 500 characters) with the page URL and `CC BY-SA 4.0`; the question and choices stay original. Polish glosses on vocabulary cards are original. Wikidata is not part of the catalog. Offline builder caches (`_wiktionary_cache*.json`, `_wikipedia_cache.json`, `_tatoeba_cache.json`) are local only. Template drills and topic-only questions stay in the database and off the live queue. What a level means — goal, length, speed, ambiguity, and the four skill competencies — is `poligon/framework.py`, described in `poligon/docs/FRAMEWORK.md`. A level number in JSON is not that profile. Shared terms use `poligon/data/glossary.json`. Whether an exercise is on the live queue is `publication_status` in the exercise file (`published`). `active` in the database is set from that status by `seed_poligon`. `poligon/data/active_slugs.json` is the list the older migration still reads; it is not a second editorial decision. `python manage.py validate_poligon_content` checks the files and prints coverage. Items already on the queue are `quality_status=legacy` until they grow a learning objective, a scenario, and a review.
6. **The rubric is not a certificate.** New speaking and writing answers use `writing_eval_v2`: five scores from 0 to 4, shown as Strong, Developing, or Needs work. Older saved rows stay on `writing_eval_v1`. Neither one is an official result.
7. **A practice level is not an official result.** Levels 1–5 in the app are working names for this trainer (survival, functional, operational, advanced, full proficiency). They are not a STANAG score and they do not quote official descriptors.

## Checklist for a new closed item

Before a multiple-choice or listening item joins the live queue:

- One fact carries the question. A distractor is another detail from the same text, not a random topic.
- The options are about the same length and the same kind of thing (all times, or all actions).
- Polish around the task does not give the answer away. The choices stay in English.
- The page does not name STANAG.

## Voice

The interface is Polish and addresses one person with **Ty**. English is available from the header, but Polish is what a visitor arriving from `/wybierz/` gets first. The register is simple and professional: short sentences, no slang, no jokes about empty screens. Auth in LingwoŁamki (`Zaloguj`, `Wróć`) is the model, not the warmer exercise copy.

1. **Polish interface, English material.** Everything around the exercise is Polish. The exercise itself — prompt, passage, answer choices, listening script — stays English, because that is what is being learned. A Polish translation of a task is offered behind "pokaż po polsku" for speaking and writing, where it cannot give the answer away. Answer choices are never translated.
2. **Buttons are verbs or the name of the action.** `Ćwicz`, `Sprawdź`, `Zaloguj`, `Następne ćwiczenie`. Not first-person slang (`Wchodzę`, `Zakładam`, `Dawaj następne`).
3. **Praise is short, then the next action.** `Dobrze.` — not `Dobrze. Lecimy dalej.`
4. **Empty and error states state the fact and the next step.** `Brak ćwiczeń na tym poziomie` plus a link to change the level. No metaphors (`cisza`, `pusto`).
5. **Avoid a default masculine form** where an impersonal one works: `Wybrana odpowiedź`, `Twoja odpowiedź`, `Pamiętam`, `Zalogowano jako`.
6. **No product jargon.** No "study signal", no "provenance", no "heuristic" in the instructions. The result page explains in one sentence what the number is.
7. **Say the limits plainly.** Listening uses browser speech: the page says it is not a recorded voice. Speaking grades the typed text, not the recording: the page says that too, next to the recorder.
8. **One instruction mapping, one catalog.** Exercise instructions come from a small set of strings shared across the catalog, kept in `poligon/data/revoice_instructions.py`. Re-voicing runs from there instead of editing each item by hand. Instruction strings are a separate pass from interface copy.
9. **"Why" lines are derived, never invented.** `poligon/data/add_explanations.py` fills the explanation shown after a wrong choice only where it follows from the item: single-word questions name the word and gloss the alternatives, and gist questions explain that the topic is what counts. The 40 level-2 comprehension items need an explanation written by hand and stay empty until then.
