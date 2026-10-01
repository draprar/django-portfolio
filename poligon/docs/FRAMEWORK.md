# Ćwiczba level framework

A practice level is a competency profile, not a difficulty number typed into JSON. Screen names stay in `poligon/levels.py`. The profile, the closed scenario list, the task-type taxonomy, and the named versions of placement, writing feedback, and the review schedule live in `poligon/framework.py`.

English is the language being learned. Polish is the support layer: instructions, explanations, and the interface. Answer choices stay in English.

## Levels

| Level | The learner can |
|---|---|
| 1 | Understand a basic message: a number, a direction, or a simple order. |
| 2 | Take part in a simple duty situation. |
| 3 | Cope when the next turn is not fully predictable. |
| 4 | Follow a longer instruction, a report, and a reason. |
| 5 | Work through a short report: situation, effect, action, backup. |

Each level states, in both languages: the communicative goal, how long a turn is, how fast the language is, how much ambiguity is allowed, the minimum competency for listening, speaking, reading, and writing, and which scenario ids are allowed. Higher levels keep the earlier scenarios and add harder ones.

Reading at level 3, as the reference competency: understand a short operational note, find the main fact, follow the order of events, recognise cause and effect, cope with some unknown words, and separate an important detail from a side fact.

## Scenarios

`orders`, `time`, `numbers`, `checkpoint`, `logistics`, `equipment`, `weather`, `vehicle`, `briefing`, `radio`, `patrol`, `map`, `medical`, `handover`, `reporting`.

## Task types

Live in the app today: `mcq`, `listening`, `speaking`, `writing`.

Reserved so content can name them before a view can score them: `true_false`, `sequence`, `main_idea`, `detail`, `inference`, `short_answer`.

## Named versions

These names are stable. Changing the rule means a new name, so an old result can still be read.

- `placement_v1` — 15 questions, 3 per level. Bands: 0–3 → 1, 4–6 → 2, 7–9 → 3, 10–12 → 4, 13–15 → 5. The result is a suggestion, not a certification.
- `writing_eval_v1` — the current length-and-shape heuristic. It does not check whether the answer did the task.
- `writing_eval_v2` — task, grammar, vocabulary, clarity, structure, each 0–4, shown as Strong, Developing, or Needs work.
- `srs_v1` — grade below 3 is due in 20 minutes; a pass waits 1 day, then 3 days, then interval times ease. Not textbook SM-2.

## Glossary

`poligon/data/glossary.json` is the short list of terms the live exercises already use. One English term has one Polish gloss and one context. New exercises should reuse these glosses instead of inventing a second translation.

## Catalog today

217 exercises and 1173 vocabulary cards are in the JSON catalog. 32 exercises are on the live queue. Levels in the app are 1–5. There is no level 0.
