"""Check the catalog. ERROR exits with status 1. WARNING and INFO do not."""

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db.models import Count

from walczak.models import Study, Style, StyleRelation

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


class Command(BaseCommand):
    help = "Validate Walczak content. Prints ERROR, WARNING, and INFO. Exits 1 only on ERROR."

    def handle(self, *args, **options) -> None:
        errors, warnings, infos = self._findings()
        for error in errors:
            self.stdout.write(f"ERROR: {error}")
        for warning in warnings:
            self.stdout.write(f"WARNING: {warning}")
        for info in infos:
            self.stdout.write(f"INFO: {info}")
        if errors:
            raise SystemExit(1)

    def _findings(self) -> tuple[list[str], list[str], list[str]]:
        errors: list[str] = []
        warnings: list[str] = []
        infos: list[str] = []
        core = Style.objects.filter(catalog_set="core", active=True)
        golden = Style.objects.filter(catalog_set="golden", active=True)
        if core.count() < 30:
            errors.append(f"core ma {core.count()}, a potrzeba co najmniej 30")
        if golden.count() < 10:
            errors.append(f"golden ma {golden.count()}, a potrzeba co najmniej 10")
        if Style.objects.values("slug").annotate(n=Count("id")).filter(n__gt=1).exists():
            errors.append("slug się powtarza")
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
            if any(not source.url for source in sources):
                errors.append(f"{style.slug}: źródło bez URL")
            roles = {source.role for source in sources}
            if not roles & HELPFUL_ROLES:
                warnings.append(f"{style.slug}: brak źródła o roli history albo definition")
        for relation in StyleRelation.objects.prefetch_related("sources"):
            if not relation.sources.exists():
                errors.append(f"relacja {relation.pk} nie ma źródła")
        studies = Study.objects.prefetch_related("sources")
        if not studies.exists():
            infos.append("brak badań — to nie jest błąd")
        for study in studies:
            if not study.sources.exists():
                errors.append(f"badanie {study.pk} nie ma źródła")
        return errors, warnings, infos


def _has_profile(style: Style) -> bool:
    try:
        style.profile
    except Style.profile.RelatedObjectDoesNotExist:
        return False
    return True
