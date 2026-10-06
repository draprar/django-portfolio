"""Emit RELATIONS block with WC-030/031 fixes."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
data = json.loads((ROOT / "_dump_wiciedzy.json").read_text(encoding="utf-8"))
rels = {(r["from"], r["to"]): r for r in data["relations"]}

rels.pop(("zapasy", "catch"), None)
rels.pop(("jujutsu", "bjj"), None)

j = rels[("jujutsu", "judo")]
j["kind"] = "historical_precursor"
j["note_pl"] = (
    "Starsze szkoły jujutsu były jednym z źródeł materiału, z którego Kano ułożył judo. "
    "Dzisiejsze judo sportowe nie jest tymi szkołami."
)
j["note_en"] = (
    "Older jujutsu schools were one source of the material from which Kano built judo. "
    "Today's sporting judo is not those schools."
)

h = rels[("hema", "szermierka")]
h["note_en"] = (
    "Sport fencing and HEMA are two different practices: fencing records touches with electrical kit, "
    "while HEMA reconstructs historical techniques from treatises."
)

catch_urls = [
    "https://en.wikipedia.org/wiki/Catch_wrestling",
    "https://www.britannica.com/sports/wrestling",
]
rels[("catch", "zapasy")] = {
    "from": "catch",
    "to": "zapasy",
    "kind": "subset",
    "note_pl": (
        "Catch wrestling należy do szerszej rodziny zapasów, ale nie jest stylem olimpijskim wolnym ani klasycznym. "
        "Poddanie może zakończyć walkę catch, podczas gdy w stylu wolnym i klasycznym decydują upadek, "
        "przewaga techniczna lub punkty."
    ),
    "note_en": (
        "Catch wrestling belongs to the broader wrestling family but is not Olympic freestyle or Greco-Roman. "
        "A submission can end a catch bout, while freestyle and Greco-Roman bouts end by fall, "
        "technical superiority or points."
    ),
    "source_urls": catch_urls,
}
rels[("zapasy", "catch")] = {
    "from": "zapasy",
    "to": "catch",
    "kind": "related",
    "note_pl": (
        "Catch wrestling to zapasy z poddaniami obok rzutu; nie jest stylem olimpijskim, "
        "ale siedzi w tej samej rodzinie co folkstyle i inne zapasy."
    ),
    "note_en": (
        "Catch wrestling is submission wrestling beside the throw; it is not an Olympic style, "
        "but it sits in the same family as folkstyle and other wrestling."
    ),
    "source_urls": catch_urls,
}

rows = sorted(rels.values(), key=lambda r: (r["from"], r["to"]))
lines = ["RELATIONS: list[dict] = ["]
for row in rows:
    urls = ", ".join(repr(u) for u in row["source_urls"])
    lines.extend(
        [
            "    {",
            f'        "from": {row["from"]!r},',
            f'        "to": {row["to"]!r},',
            f'        "kind": {row["kind"]!r},',
            f'        "note_pl": {row["note_pl"]!r},',
            f'        "note_en": {row["note_en"]!r},',
            f'        "source_urls": [{urls}],',
            "    },",
        ]
    )
lines.append("]")
(ROOT / "wiciedzy" / "data" / "_relations_fragment.py").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(len(rows), "relations")
