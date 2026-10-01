from django.core.management.base import BaseCommand, CommandError

from poligon.content_validation import validate_catalog


class Command(BaseCommand):
    help = "Check the exercise catalog and print level-by-skill coverage."

    def add_arguments(self, parser):
        parser.add_argument(
            "--strict",
            action="store_true",
            help="Fail legacy published items for the same gaps as new publishes.",
        )

    def handle(self, *args, **options):
        report = validate_catalog(strict=options["strict"])
        self.stdout.write(report.text())
        if report.errors:
            raise CommandError(f"{len(report.errors)} content errors")
        self.stdout.write(self.style.SUCCESS("Content catalog passed."))
