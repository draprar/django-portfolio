"""Upsert the wiciędze catalog by slug. Does not delete styles or touch sessions."""

from __future__ import annotations

from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import F

from wiciedzy.data.instruments import PREFERENCE, TYPES
from wiciedzy.data.prose import PROSE
from wiciedzy.data.styles import CORE, FACTS, GOLDEN, RELATIONS, STYLE_TAGS, TAG_CATALOG, UMBRELLAS
from wiciedzy.models import (
    Fact,
    OptionWeight,
    PreferenceOption,
    PreferenceQuestion,
    Source,
    Style,
    StyleRelation,
    StyleType,
    Tag,
    TrainingProfile,
)


class Command(BaseCommand):
    help = "Upsert wiciędze styles, sources, profiles, and questionnaires by stable slug."

    def handle(self, *args, **options) -> None:
        with transaction.atomic():
            self._types()
            self._tags()
            for raw in CORE + GOLDEN:
                row = {**raw, **PROSE.get(raw["slug"], {})}
                self._style(row)
            self._relations()
            self._facts()
            self._preference()
        self.stdout.write(self.style.SUCCESS("wiciędze catalog upserted."))

    def _types(self) -> None:
        for row in TYPES:
            StyleType.objects.update_or_create(code=row["code"], defaults={"name_pl": row["name_pl"], "name_en": row["name_en"]})

    def _tags(self) -> None:
        for slug, name_pl, name_en in TAG_CATALOG:
            Tag.objects.update_or_create(slug=slug, defaults={"name_pl": name_pl, "name_en": name_en})

    def _style(self, row: dict) -> Style:
        defaults = {
            "name_pl": row["name_pl"],
            "name_en": row["name_en"],
            "family": row["family"],
            "catalog_set": row["catalog_set"],
            "origin_pl": row.get("origin_pl", ""),
            "origin_en": row.get("origin_en", ""),
            "region": row.get("region", ""),
            "period_pl": row.get("period_pl", ""),
            "period_en": row.get("period_en", ""),
            "competition_status": row.get("competition_status", "both"),
            "weapon_status": row.get("weapon_status", "none"),
            "sources_disagree": row.get("sources_disagree", False),
            "is_umbrella": row["slug"] in UMBRELLAS,
            "matcher_enabled": "profile" in row,
            "joke_pl": row.get("joke_pl", ""),
            "joke_en": row.get("joke_en", ""),
            "summary_pl": row["summary_pl"],
            "summary_en": row["summary_en"],
            "history_pl": row.get("history_pl", ""),
            "history_en": row.get("history_en", ""),
            "practice_pl": row.get("practice_pl", ""),
            "practice_en": row.get("practice_en", ""),
            "sort_order": row.get("sort_order", 0),
            "active": True,
        }
        style, _created = Style.objects.update_or_create(slug=row["slug"], defaults=defaults)
        style.style_types.set(StyleType.objects.filter(code__in=row.get("types", [])))
        style.tags.set(Tag.objects.filter(slug__in=STYLE_TAGS.get(row["slug"], [])))
        if "profile" in row:
            TrainingProfile.objects.update_or_create(style=style, defaults=row["profile"])
        for index, source in enumerate(row.get("sources", [])):
            accessed = source.get("accessed_at") or ""
            Source.objects.update_or_create(
                style=style,
                url=source["url"],
                defaults={
                    "title": source["title"],
                    "author": source.get("author", ""),
                    "source_type": source.get("source_type", "other"),
                    "role": source.get("role", "definition"),
                    "quality": source.get("quality", "secondary"),
                    "license": source.get("license", ""),
                    "license_url": source.get("license_url", ""),
                    "attribution": source.get("attribution", ""),
                    "accessed_at": date.fromisoformat(accessed) if accessed else None,
                    "sort_order": index,
                },
            )
        return style

    def _relations(self) -> None:
        keep: list[int] = []
        for row in RELATIONS:
            left = Style.objects.get(slug=row["from"])
            right = Style.objects.get(slug=row["to"])
            StyleRelation.objects.filter(from_style=left, to_style=right).exclude(kind=row["kind"]).delete()
            relation, _created = StyleRelation.objects.update_or_create(
                from_style=left,
                to_style=right,
                kind=row["kind"],
                defaults={"note_pl": row["note_pl"], "note_en": row["note_en"]},
            )
            relation.sources.set(Source.objects.filter(url__in=row["source_urls"], style__in=[left, right]))
            keep.append(relation.pk)
        StyleRelation.objects.exclude(pk__in=keep).delete()

    def _facts(self) -> None:
        keep: list[int] = []
        for row in FACTS:
            fact, _created = Fact.objects.update_or_create(
                text_pl=row["text_pl"],
                defaults={"text_en": row["text_en"], "is_legend": row["is_legend"]},
            )
            styles = list(Style.objects.filter(slug__in=row["styles"]))
            fact.styles.set(styles)
            fact.sources.set(Source.objects.filter(url__in=row["source_urls"], style__in=styles))
            keep.append(fact.pk)
        Fact.objects.exclude(pk__in=keep).delete()

    def _locate_preference_question(self, row: dict) -> PreferenceQuestion | None:
        kind = row["kind"]
        dimension = row.get("dimension") or ""
        if kind == "scale" and dimension:
            found = PreferenceQuestion.objects.filter(kind=kind, dimension=dimension).first()
            if found:
                return found
        found = PreferenceQuestion.objects.filter(kind=kind, text_en=row["text_en"]).first()
        if found:
            return found
        return PreferenceQuestion.objects.filter(sort_order=row["sort_order"]).first()

    def _preference(self) -> None:
        # Free sort_order slots before reordering (avoid two rows sharing one index).
        PreferenceQuestion.objects.filter(active=True).update(sort_order=F("sort_order") + 1000)
        keep: list[int] = []
        for row in PREFERENCE:
            question = self._locate_preference_question(row)
            if question is None:
                question = PreferenceQuestion()
            question.text_pl = row["text_pl"]
            question.text_en = row["text_en"]
            question.kind = row["kind"]
            question.dimension = row.get("dimension", "")
            question.sort_order = row["sort_order"]
            question.active = True
            question.save()
            question.options.all().delete()
            for index, option in enumerate(row.get("options", [])):
                created = PreferenceOption.objects.create(
                    question=question,
                    text_pl=option["text_pl"],
                    text_en=option["text_en"],
                    sort_order=index,
                )
                for dimension, weight in option["weights"]:
                    OptionWeight.objects.create(option=created, dimension=dimension, weight=weight)
            keep.append(question.pk)
        PreferenceQuestion.objects.exclude(pk__in=keep).delete()
