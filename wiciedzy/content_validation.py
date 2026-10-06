"""Shared catalog consistency checks (WC-120)."""

from __future__ import annotations

import re
from urllib.parse import urlparse

from django.db.models import Count

from wiciedzy.data.styles import CORE, FACTS, GOLDEN, RELATIONS
from wiciedzy.models import Fact, Style, StyleRelation

CARD_FIELDS = (
    "name_pl",
    "name_en",
    "summary_pl",
    "summary_en",
    "history_pl",
    "history_en",
    "practice_pl",
    "practice_en",
    "origin_pl",
    "origin_en",
    "period_pl",
    "period_en",
    "region",
)

HELPFUL_ROLES = {"history", "definition"}
URL_RE = re.compile(r"^https?://", re.I)
APPROVED_ACTIVE_SLUGS = frozenset(row["slug"] for row in CORE + GOLDEN)
SOURCE_SLUGS = APPROVED_ACTIVE_SLUGS


def source_slugs_for_style(slug: str) -> set[str]:
    row = next((item for item in CORE + GOLDEN if item["slug"] == slug), None)
    if row is None:
        return set()
    return {source["url"] for source in row.get("sources", []) if source.get("url")}


def collect_findings() -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    infos: list[str] = []

    source_count = len(CORE) + len(GOLDEN)
    if len(CORE) < 36:
        errors.append(f"CORE ma {len(CORE)}, a po backfillu potrzeba co najmniej 36")
    if len(GOLDEN) < 10:
        errors.append(f"golden ma {len(GOLDEN)}, a potrzeba co najmniej 10")
    if len(RELATIONS) < 20:
        errors.append(f"RELATIONS ma {len(RELATIONS)}, oczekiwano co najmniej 20")

    core = Style.objects.filter(catalog_set="core", active=True)
    golden = Style.objects.filter(catalog_set="golden", active=True)
    if core.count() < 30:
        errors.append(f"core w DB ma {core.count()}, a potrzeba co najmniej 30")
    if golden.count() < 10:
        errors.append(f"golden w DB ma {golden.count()}, a potrzeba co najmniej 10")

    active_slugs = set(Style.objects.filter(active=True).values_list("slug", flat=True))
    orphans = active_slugs - SOURCE_SLUGS
    if orphans:
        errors.append(f"ORPHAN w DB (brak w styles.py): {', '.join(sorted(orphans))}")
    missing_active = SOURCE_SLUGS - active_slugs
    if missing_active:
        errors.append(f"ACTIVE w źródle, brak w DB: {', '.join(sorted(missing_active))}")

    if Style.objects.values("slug").annotate(n=Count("id")).filter(n__gt=1).exists():
        errors.append("slug się powtarza")

    if StyleRelation.objects.count() != len(RELATIONS):
        errors.append(
            f"relacji w DB jest {StyleRelation.objects.count()}, a w RELATIONS {len(RELATIONS)}"
        )

    allowed_kinds = {choice[0] for choice in StyleRelation.KIND_CHOICES}
    relation_pairs: set[tuple[str, str]] = set()
    for row in RELATIONS:
        if row["from"] == row["to"]:
            errors.append(f"relacja do samej siebie: {row['from']}")
        if row["from"] not in SOURCE_SLUGS or row["to"] not in SOURCE_SLUGS:
            errors.append(f"relacja {row['from']} → {row['to']}: nieznany slug")
        if row["kind"] not in allowed_kinds:
            errors.append(f"relacja {row['from']} → {row['to']}: niedozwolony kind {row['kind']!r}")
        pair = (row["from"], row["to"])
        if pair in relation_pairs:
            errors.append(f"duplikat pary relacji: {row['from']} → {row['to']}")
        relation_pairs.add(pair)

    for fact_row in FACTS:
        for slug in fact_row["styles"]:
            if slug not in SOURCE_SLUGS:
                errors.append(f"fakt odnosi się do nieznanego sluga: {slug}")

    catalog = (core | golden).prefetch_related("sources", "style_types", "tags").distinct()
    for style in catalog:
        for field in CARD_FIELDS:
            if not str(getattr(style, field)).strip():
                errors.append(f"{style.slug}: puste {field}")
        if style.matcher_enabled and not _has_profile(style):
            errors.append(f"{style.slug}: matcher włączony bez profilu")
        if not style.tags.exists():
            warnings.append(f"{style.slug}: brak tagów")
        sources = list(style.sources.all())
        useful = [source for source in sources if source.quality != "discovery_only"]
        if sources and len(useful) < 2:
            warnings.append(f"{style.slug}: drugie źródło jest tylko discovery")
        if style.catalog_set != "core":
            continue
        if not style.style_types.exists():
            errors.append(f"{style.slug}: brak typu")
        if len(sources) < 2:
            errors.append(f"{style.slug}: mniej niż dwa źródła")
        for source in sources:
            if not source.url:
                errors.append(f"{style.slug}: źródło bez URL")
            elif not URL_RE.match(source.url):
                errors.append(f"{style.slug}: źródło ma niepoprawny URL {source.url!r}")
        roles = {source.role for source in sources}
        if not roles & HELPFUL_ROLES:
            warnings.append(f"{style.slug}: brak źródła o roli history albo definition")
        expected_urls = source_slugs_for_style(style.slug)
        extra = {source.url for source in sources} - expected_urls
        if extra:
            warnings.append(f"{style.slug}: URL w DB spoza styles.py: {', '.join(sorted(extra))}")

    inactive_slugs = set(Style.objects.filter(active=False).values_list("slug", flat=True))
    for relation in StyleRelation.objects.select_related("from_style", "to_style").prefetch_related(
        "sources"
    ):
        if not relation.sources.exists():
            errors.append(f"relacja {relation.from_style.slug} → {relation.to_style.slug} nie ma źródła")
        if relation.from_style.slug in inactive_slugs or relation.to_style.slug in inactive_slugs:
            errors.append(
                f"relacja {relation.from_style.slug} → {relation.to_style.slug} wskazuje nieaktywny styl"
            )
        note = relation.note_pl + relation.note_en
        if "kończą się na rzucie i punktach" in note or "end on the throw and the points" in note:
            errors.append(
                f"relacja {relation.from_style.slug} → {relation.to_style.slug}: zabroniona treść o zapasach"
            )

    catch_subset = next(
        (row for row in RELATIONS if row["from"] == "catch" and row["to"] == "zapasy"),
        None,
    )
    if catch_subset is None or catch_subset["kind"] != "subset":
        errors.append("brak relacji catch → zapasy (subset)")

    for fact in Fact.objects.prefetch_related("styles", "sources"):
        if not fact.sources.exists():
            errors.append(f"fakt {fact.pk} nie ma źródła")
        for attached in fact.styles.all():
            if attached.slug not in SOURCE_SLUGS:
                errors.append(f"fakt {fact.pk} wskazuje nieznany slug {attached.slug}")

    if active_slugs != APPROVED_ACTIVE_SLUGS:
        errors.append("zestaw aktywnych slugów nie zgadza się z CORE+GOLDEN")

    return errors, warnings, infos


def _has_profile(style: Style) -> bool:
    try:
        style.profile
    except Style.profile.RelatedObjectDoesNotExist:
        return False
    return True
