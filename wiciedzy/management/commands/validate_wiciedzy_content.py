"""Check the catalog. ERROR exits with status 1. WARNING and INFO do not."""

from __future__ import annotations

from django.core.management.base import BaseCommand

from wiciedzy.content_validation import collect_findings


class Command(BaseCommand):
    help = "Validate wiciędze content. Prints ERROR, WARNING, and INFO. Exits 1 only on ERROR."

    def handle(self, *args, **options) -> None:
        errors, warnings, infos = collect_findings()
        for error in errors:
            self.stdout.write(f"ERROR: {error}")
        for warning in warnings:
            self.stdout.write(f"WARNING: {warning}")
        for info in infos:
            self.stdout.write(f"INFO: {info}")
        if errors:
            raise SystemExit(1)
