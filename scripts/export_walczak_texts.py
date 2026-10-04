"""One-off export of all Walczak user-facing strings. Run: python scripts/export_walczak_texts.py"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from walczak.dimensions import DIMENSION_LABELS, DIFF_COPY, LOW_REASON_COPY, REASON_COPY, level_words
from walczak.display import COMPETITION_WORDS, GROUP_LABELS, WEAPON_WORDS
from walczak.models import (
    Archetype,
    Fact,
    PreferenceOption,
    PreferenceQuestion,
    Study,
    Style,
    StyleRelation,
    StyleType,
    Tag,
)

PAIR_RE = re.compile(
    r'data-pl="([^"]*)"\s+data-en="([^"]*)"|data-en="([^"]*)"\s+data-pl="([^"]*)"'
)


def pairs_from_templates() -> list[tuple[str, str, str]]:
    tpl_dir = ROOT / "walczak" / "templates" / "walczak"
    out: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()
    for path in sorted(tpl_dir.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        for m in PAIR_RE.finditer(text):
            if m.group(1) is not None:
                pl, en = m.group(1), m.group(2)
            else:
                en, pl = m.group(3), m.group(4)
            if "{{" in pl or "{{" in en:
                continue
            key = (pl, en)
            if key in seen:
                continue
            seen.add(key)
            out.append((path.name, pl, en))
    return out


def line(pl: str, en: str) -> str:
    return f"PL: {pl}\nEN: {en}\n"


def main() -> None:
    lines: list[str] = [
        "# Walczak — eksport tekstów",
        "",
        f"Wygenerowano z repo `{ROOT.name}`. Polski = domyślny na stronie.",
        "",
        "## Interfejs (szablony, pary PL/EN)",
        "",
    ]
    by_file: dict[str, list[tuple[str, str]]] = {}
    for fname, pl, en in pairs_from_templates():
        by_file.setdefault(fname, []).append((pl, en))
    for fname in sorted(by_file):
        lines.append(f"### {fname}")
        lines.append("")
        for pl, en in by_file[fname]:
            lines.append(line(pl, en))
        lines.append("")

    lines.append("## Etykiety profilu treningu (`dimensions.py`, `display.py`)")
    lines.append("")
    for key, (pl, en) in DIMENSION_LABELS.items():
        lines.append(line(pl, en))
    lines.append("### Poziomy")
    lines.append(line("nisko", "low"))
    lines.append(line("średnio", "medium"))
    lines.append(line("wysoko", "high"))
    lines.append("### Grupy")
    for pl, en in GROUP_LABELS.values():
        lines.append(line(pl, en))
    lines.append("### Zawody (meta)")
    for pl, en in COMPETITION_WORDS.values():
        lines.append(line(pl, en))
    lines.append("### Broń (meta)")
    for pl, en in WEAPON_WORDS.values():
        lines.append(line(pl, en))
    lines.append("")

    lines.append("## Szablony zdań (`dimensions.py`)")
    lines.append("")
    lines.append("### Porównywarka — różnice (DIFF_COPY, {higher}/{lower})")
    lines.append("")
    for pl, en in DIFF_COPY.values():
        lines.append(line(pl, en))
    lines.append("### Quizopasowanie — uzasadnienia (REASON_COPY, 3 warianty na oś)")
    lines.append("")
    for name, triple in REASON_COPY.items():
        lines.append(f"#### {name}")
        for pl, en in triple:
            lines.append(line(pl, en))
    lines.append("### Quizopasowanie — niskie wartości (LOW_REASON_COPY)")
    lines.append("")
    for pl, en in LOW_REASON_COPY.values():
        lines.append(line(pl, en))
    lines.append("")

    lines.append("## Rodziny stylów (model)")
    lines.append("")
    for code, pl in Style.FAMILY_CHOICES:
        lines.append(line(pl, Style.FAMILY_EN[code]))
    lines.append("")

    lines.append("## Quizopasowanie — pytania i opcje")
    lines.append("")
    for q in PreferenceQuestion.objects.prefetch_related("options").order_by("sort_order", "pk"):
        lines.append(f"### [{q.kind}] {q.text_pl}")
        lines.append(line(q.text_pl, q.text_en))
        for opt in q.options.all():
            lines.append(line(opt.text_pl, opt.text_en))
        lines.append("")

    lines.append("## Tagi")
    lines.append("")
    for t in Tag.objects.order_by("name_pl"):
        lines.append(line(t.name_pl, t.name_en))
    lines.append("")

    lines.append("## Typy stylu")
    lines.append("")
    for t in StyleType.objects.order_by("name_pl"):
        lines.append(line(t.name_pl, t.name_en))
    lines.append("")

    lines.append("## Katalog stylów")
    lines.append("")
    for s in Style.objects.filter(active=True).prefetch_related("tags", "style_types", "facts", "sources").order_by("catalog_set", "sort_order", "name_pl"):
        lines.append(f"### {s.slug} ({s.catalog_set})")
        lines.append(line(s.name_pl, s.name_en))
        lines.append(line(s.get_family_display(), s.family_en))
        if s.summary_pl:
            lines.append("**O stylu / summary**")
            lines.append(line(s.summary_pl.strip(), s.summary_en.strip()))
        if s.origin_pl:
            lines.append(line(s.origin_pl, s.origin_en))
        if s.period_pl:
            lines.append(line(s.period_pl, s.period_en))
        if s.region:
            lines.append(f"Region: {s.region}")
        if s.history_pl:
            lines.append("**Historia**")
            lines.append(line(s.history_pl.strip(), s.history_en.strip()))
        if s.practice_pl:
            lines.append("**Jak się walczy**")
            lines.append(line(s.practice_pl.strip(), s.practice_en.strip()))
        if s.joke_pl:
            lines.append("**Żart**")
            lines.append(line(s.joke_pl, s.joke_en))
        for fact in s.facts.all():
            lines.append(line(fact.text_pl.strip(), fact.text_en.strip()))
        lines.append("")

    lines.append("## Relacje między stylami")
    lines.append("")
    for rel in StyleRelation.objects.select_related("from_style", "to_style").order_by("from_style__slug"):
        lines.append(f"### {rel.from_style.slug} → {rel.to_style.slug}")
        if rel.note_pl:
            lines.append(line(rel.note_pl, rel.note_en))
        lines.append("")

    lines.append("## Badania (porównywarka)")
    lines.append("")
    for st in Study.objects.prefetch_related("styles").order_by("pk"):
        lines.append(line(st.finding_pl.strip(), st.finding_en.strip()))
        if st.limitation_pl:
            lines.append(line(st.limitation_pl.strip(), st.limitation_en.strip()))
        lines.append("")

    if Archetype.objects.exists():
        lines.append("## Archetypy (żart — jeśli w bazie)")
        lines.append("")
        for a in Archetype.objects.order_by("pk"):
            lines.append(line(a.name_pl, a.name_en))
            if a.description_pl:
                lines.append(line(a.description_pl, a.description_en))
            lines.append("")

    out_path = ROOT / "walczak" / "teksty-eksport.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_path} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
