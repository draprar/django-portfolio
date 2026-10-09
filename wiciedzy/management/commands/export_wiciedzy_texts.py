"""Eksport tekstów widocznych pod /wiciedze/ (szablony + baza). Nie eksportuje martwych tras ani żartów z modelu."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

from django.core.management.base import BaseCommand

from wiciedzy.dimensions import (
    DIFF_COPY,
    DIMENSION_LABELS,
    LOW_REASON_COPY,
    REASON_COPY,
    level_words,
)
from wiciedzy.display import COMPETITION_WORDS, GROUP_LABELS, WEAPON_WORDS, region_labels
from wiciedzy.models import (
    PreferenceQuestion,
    Study,
    Style,
    StyleType,
    Tag,
    TrainingProfile,
)

TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "templates" / "wiciedzy"

PAGE_ROUTES: tuple[tuple[str, str], ...] = (
    ("/wiciedze/", "home.html"),
    ("/wiciedze/spis/", "list.html"),
    ("/wiciedze/spis/<styl>/", "detail.html"),
    ("/wiciedze/test/", "test.html"),
    ("/wiciedze/dopasowanie/", "match.html"),
    ("/wiciedze/porownaj/", "compare_form.html"),
    ("/wiciedze/porownaj/<a>/<b>/", "compare.html"),
    ("/wiciedze/test/ (brak pytań)", "empty.html"),
    ("404 w wiciędze", "404.html"),
)

LEGEND_ON_PAGES = frozenset({"detail.html", "compare.html"})


BLOCK_WALCZAK_RE = re.compile(r"\{% block wiciedzy %\}(.*?)\{% endblock %\}", re.DOTALL)

BLOCK_META_RE = re.compile(r"\{% block meta_description %\}(.*?)\{% endblock %\}", re.DOTALL)

HEAD_RE = re.compile(r"<head>(.*?)</head>", re.DOTALL | re.IGNORECASE)

BODY_RE = re.compile(r"<body>(.*?)</body>", re.DOTALL | re.IGNORECASE)


PAIR_RE = re.compile(
    r'data-pl="([^"]*)"\s+data-en="([^"]*)"|data-en="([^"]*)"\s+data-pl="([^"]*)"',
    re.MULTILINE,
)


def _read_template(name: str) -> str:

    path = TEMPLATE_DIR / name

    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _is_static_copy(text: str) -> bool:
    return "{{" not in text and "{%" not in text


def _pairs_from_text(text: str) -> list[tuple[str, str]]:

    pairs: list[tuple[str, str]] = []

    seen: set[tuple[str, str]] = set()

    for match in PAIR_RE.finditer(text):
        if match.group(1) is not None:
            pl, en = match.group(1), match.group(2)

        else:
            en, pl = match.group(3), match.group(4)

        key = (pl, en)

        if key not in seen:
            seen.add(key)

            pairs.append(key)

    return pairs


def _strip_scripts(html: str) -> str:

    return re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)


def _chrome_visible_fragment() -> str:

    text = _read_template("base.html")

    body_match = BODY_RE.search(text)

    if not body_match:
        return ""

    body = body_match.group(1)

    body = re.sub(r"<main\b[^>]*>.*?</main>", "", body, flags=re.DOTALL | re.IGNORECASE)

    return _strip_scripts(body)


def _page_visible_fragment(name: str) -> str:

    text = _read_template(name)

    text = re.sub(r"\{% extends[^%]+%\}\s*", "", text)

    for block in ("title", "title_i18n", "og_title", "meta_description", "robots", "extra_js"):
        text = re.sub(
            rf"\{{% block {block} %\}}.*?\{{% endblock %\}}",
            "",
            text,
            flags=re.DOTALL,
        )

    match = BLOCK_WALCZAK_RE.search(text)

    fragment = match.group(1) if match else text

    return _strip_scripts(fragment)


def _legend_pairs() -> list[tuple[str, str]]:
    return _pairs_from_text(_read_template("_profile_scale_legend.html"))


def _legend_pl_lines() -> list[str]:

    pairs = _legend_pairs()

    if not pairs:
        return []

    lines = [pairs[0][0].strip()]

    index = 1

    while index < len(pairs):
        word = pairs[index][0].strip()

        if index + 1 < len(pairs) and pairs[index + 1][0].startswith(" —"):
            lines.append(word + pairs[index + 1][0])

            index += 2

        else:
            lines.append(word)

            index += 1

    return lines


def _static_pl_from_text(text: str) -> list[str]:

    return [pl.strip() for pl, _ in _pairs_from_text(text) if pl.strip() and _is_static_copy(pl)]


def _visible_pl_for_page(template_name: str) -> list[str]:

    lines = _static_pl_from_text(_page_visible_fragment(template_name))

    if template_name in LEGEND_ON_PAGES:
        lines.extend(_legend_pl_lines())

    return lines


def _seo_fragments() -> list[tuple[str, str]]:

    found: list[tuple[str, str]] = []

    base = _read_template("base.html")

    head = HEAD_RE.search(base)

    if head:
        found.append(("base.html — domyślny <head> (gdy strona nie nadpisuje meta)", head.group(1)))

    for _route, name in PAGE_ROUTES:
        text = _read_template(name)

        meta = BLOCK_META_RE.search(text)

        if meta:
            found.append((f"{name} — block meta_description", meta.group(1)))

        for block in ("title_i18n",):
            match = re.search(rf"\{{% block {block} %\}}(.*?)\{{% endblock %\}}", text, re.DOTALL)

            if match and "data-pl" in match.group(1):
                found.append((f"{name} — block {block}", match.group(1)))

    return found


class ExportWriter:
    def __init__(self, pl_only: bool, plain: bool) -> None:

        self.pl_only = pl_only

        self.plain = plain

        self.lines: list[str] = []

    def blank(self) -> None:

        if self.lines and self.lines[-1] != "":
            self.lines.append("")

    def text(self, pl: str, en: str = "") -> None:

        pl = (pl or "").strip()

        en = (en or "").strip()

        if self.pl_only:
            if pl:
                self.lines.append(pl)

            return

        if self.plain:
            if pl:
                self.lines.append(pl)

            if en:
                self.lines.append(en)

            return

        self.lines.append(f"**PL:** {pl}")

        self.lines.append(f"**EN:** {en}")

        self.lines.append("")

    def mono(self, text: str, label_pl: str = "Źródło", label_en: str = "Source") -> None:

        text = (text or "").strip()

        if not text:
            return

        if self.pl_only:
            self.lines.append(text)
            return

        if self.plain:
            self.lines.append(text)
            return

        self.lines.append(f"**{label_pl}:** {text}")

        self.lines.append(f"**{label_en}:** {text}")

        self.lines.append("")

    def heading(self, markdown: str, plain: str) -> None:

        if self.pl_only:
            return

        if self.plain:
            if plain.strip():
                self.blank()

                self.lines.append(plain.strip())

                self.blank()

            return

        self.lines.append(markdown)

        self.lines.append("")

    def raw(self, line: str) -> None:

        if line.strip() or not self.plain:
            self.lines.append(line)


def _build_lines(pl_only: bool, plain: bool, include_seo: bool) -> list[str]:

    w = ExportWriter(pl_only=pl_only, plain=plain)

    if not pl_only and not plain:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        w.raw("# wiciędze — teksty na stronie (obecny UI)")

        w.blank()

        w.raw(f"Wygenerowano: **{now}** poleceniem `python manage.py export_wiciedzy_texts`.")

        w.blank()

        w.raw(
            "Źródło: aktywne trasy w `wiciedzy/urls.py`, szablony, "
            "modele `Style` (`active=True`), `PreferenceQuestion` (`active=True`), "
            "teksty z `dimensions.py` / `display.py`."
        )

        w.blank()

        w.raw(
            "**Nie wchodzi:** `/wiciedze/quiz/`, archetyp, `joke_*`, `_quick.html`, stary `teksty.md`. "
            "Sekcja 1 = treść w przeglądarce; SEO na końcu."
        )

        w.blank()

        w.raw("---")

    w.heading("## 1. Teksty widoczne w przeglądarce (PL/EN)", "Teksty widoczne w przeglądarce")

    w.heading("### Wspólne: nawigacja i stopka", "Nawigacja i stopka (każda strona)")

    if not pl_only and not plain:
        w.raw("- Marka: **wiciędze** (bez przełącznika języka)")

        w.raw("- Przełącznik: **PL** / **EN**")

        w.blank()

    else:
        w.text("wiciędze")

        w.text("PL")

        w.text("EN")

    for pl, en in _pairs_from_text(_chrome_visible_fragment()):
        if pl_only and not _is_static_copy(pl):
            continue

        w.text(pl, en)

    for route, name in PAGE_ROUTES:
        w.heading(f"### `{route}`", route)

        if not pl_only and not plain:
            w.raw(f"_Szablon:_ `{name}` — stałe napisy; nazwy stylów i opisy z sekcji katalogu.")

            w.blank()

        if pl_only:
            for line in _visible_pl_for_page(name):
                w.text(line)

            continue

        pairs = [(pl, en) for pl, en in _pairs_from_text(_page_visible_fragment(name)) if _is_static_copy(pl)]

        if name in LEGEND_ON_PAGES:
            for pl, en in _legend_pairs():
                w.text(pl, en)

        if not pairs and name not in LEGEND_ON_PAGES:
            if not pl_only and not plain:
                w.raw("_Tylko treść z bazy (np. karty stylów)._")

                w.blank()

            continue

        for pl, en in pairs:
            w.text(pl, en)

    w.heading("## 2. Tagi", "Tagi")

    for tag in Tag.objects.order_by("name_pl"):
        w.text(tag.name_pl, tag.name_en)

    w.heading("## 3. Typy stylu", "Typy stylu")

    for st in StyleType.objects.order_by("name_pl"):
        w.text(st.name_pl, st.name_en)

    w.heading("## 4. Katalog stylów", "Katalog stylów")

    styles = (
        Style.objects.filter(active=True)
        .prefetch_related("style_types", "tags", "facts", "sources", "relations_out__to_style")
        .order_by("sort_order", "name_pl")
    )

    for style in styles:
        if pl_only or plain:
            w.blank()

            w.text(style.name_pl)

        else:
            w.raw(f"### {style.slug} — {style.name_pl}")

            w.blank()

            w.text(style.name_pl, style.name_en)

        w.text(style.get_family_display(), style.family_en)

        if style.sources_disagree:
            w.text(
                "Nie da się uczciwie podać jednej wersji, źródła są niejasne.",
                "There's no honest single version — the sources are unclear.",
            )

        w.text(style.summary_pl, style.summary_en)

        if style.origin_pl or style.origin_en:
            w.text(style.origin_pl, style.origin_en)

        if style.period_pl or style.period_en:
            w.text(style.period_pl, style.period_en)

        if style.region:
            region_pl, region_en = region_labels(style.region)
            w.text(region_pl, region_en)

        for t in style.style_types.all():
            w.text(t.name_pl, t.name_en)

        if style.history_pl or style.history_en:
            w.text(style.history_pl, style.history_en)

        if style.practice_pl or style.practice_en:
            w.text(style.practice_pl, style.practice_en)

        try:
            profile = style.profile

        except TrainingProfile.DoesNotExist:
            profile = None

        if profile is not None:
            for pl, en in _legend_pairs():
                w.text(pl, en)

            for key, names in (
                ("uderzenia", ("striking", "punches", "kicks", "knees", "elbows")),
                ("chwyt", ("grappling", "clinch", "throws", "takedowns", "ground_fighting", "submissions")),
                ("bron", ("weapons",)),
                (
                    "trening",
                    (
                        "solo_training",
                        "partner_training",
                        "contact_level",
                        "competition_level",
                        "tradition_level",
                        "technical_complexity",
                        "athletic_demand",
                        "endurance_demand",
                        "explosiveness",
                        "equipment_required",
                    ),
                ),
            ):
                g_pl, g_en = GROUP_LABELS[key]

                if not pl_only:
                    w.text(g_pl, g_en)

                else:
                    w.text(g_pl)

                for name in names:
                    w_pl, w_en = level_words(int(getattr(profile, name)))

                    l_pl, _l_en = DIMENSION_LABELS[name]

                    w.text(f"{l_pl}: {w_pl}", f"{_l_en}: {w_en}")

            comp = COMPETITION_WORDS.get(style.competition_status)

            if comp:
                w.text(comp[0], comp[1])

            weap = WEAPON_WORDS.get(style.weapon_status)

            if weap:
                w.text(weap[0], weap[1])

        for rel in style.relations_out.all():
            if not rel.note_pl and not rel.note_en:
                continue

            w.text(rel.to_style.name_pl, rel.to_style.name_en)

            w.text(rel.note_pl, rel.note_en)

        for fact in style.facts.all():
            w.text(fact.text_pl, fact.text_en)

            if fact.is_legend:
                w.text("Późniejsza tradycja / legenda.", "Later tradition / legend.")

        for src in style.sources.all():
            parts = [src.title]

            if src.author:
                parts.append(src.author)

            if src.license:
                parts.append(src.license)

            w.mono(" — ".join(parts))

    w.heading("## 5. Quizopasowanie — pytania", "Quizopasowanie — pytania")

    questions = PreferenceQuestion.objects.filter(active=True).prefetch_related("options").order_by("sort_order", "pk")

    for q in questions:
        w.text(q.text_pl, q.text_en)

        for opt in q.options.all().order_by("sort_order", "pk"):
            w.text(opt.text_pl, opt.text_en)

    w.heading("## 6. Badania (porównanie)", "Badania przy porównaniu")

    for study in Study.objects.distinct().order_by("title"):
        title = study.title + (f" ({study.year})" if study.year else "")

        w.text(title, title)

        w.text(study.finding_pl, study.finding_en)

        w.text(study.limitation_pl, study.limitation_en)

    w.heading("## 7. Teksty dopasowania i porównania", "Teksty dopasowania i porównania (szablony)")

    w.text("nisko", "low")

    w.text("średnio", "medium")

    w.text("wysoko", "high")

    for _key, triple in sorted(REASON_COPY.items()):
        plus, minus_high, minus_low = triple

        w.text(plus[0], plus[1])

        w.text(minus_high[0], minus_high[1])

        w.text(minus_low[0], minus_low[1])

    for _key, pair in sorted(LOW_REASON_COPY.items()):
        w.text(pair[0], pair[1])

    for _key, pair in sorted(DIFF_COPY.items()):
        w.text(pair[0], pair[1])

    if include_seo and not pl_only:
        w.heading("## Załącznik: SEO", "Załącznik: SEO (niewidoczne w treści)")

        for _label, fragment in _seo_fragments():
            for pl, en in _pairs_from_text(fragment):
                w.text(pl, en)

    while w.lines and w.lines[-1] == "":
        w.lines.pop()

    return w.lines


class Command(BaseCommand):
    help = "Zapisuje teksty UI + katalog (md lub PL plain)"

    def add_arguments(self, parser):

        parser.add_argument(
            "-o",
            "--output",
            default="",
            help="Ścieżka pliku względem katalogu projektu",
        )

        parser.add_argument(
            "--polish-only",
            action="store_true",
            help="Tylko polskie teksty",
        )

        parser.add_argument(
            "--plain",
            action="store_true",
            help="Bez markdownu i znaczników — sama treść, linia po linii",
        )

    def handle(self, *args, **options):

        pl_only = bool(options["polish_only"])

        plain = bool(options["plain"])

        root = Path(__file__).resolve().parents[3]

        out_default = "wiciedzy/teksty-pl.txt" if (pl_only and plain) else "wiciedzy/teksty-eksport.md"

        out_path = root / (options["output"] or out_default)

        include_seo = not pl_only

        lines = _build_lines(pl_only=pl_only, plain=plain or pl_only, include_seo=include_seo)

        out_path.parent.mkdir(parents=True, exist_ok=True)

        encoding = "utf-8-sig" if out_path.suffix.lower() in {".md", ".txt"} else "utf-8"

        out_path.write_text("\n".join(lines) + "\n", encoding=encoding)

        self.stdout.write(self.style.SUCCESS(f"Zapisano: {out_path} ({len(lines)} linii)"))
