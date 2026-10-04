"""Refresh boxing copy and related catalog fields."""

import os
import sys

from django.core.management import call_command
from django.db import migrations


def _is_test_run() -> bool:
    if os.environ.get("DJANGO_TESTING", "").lower() in {"1", "true", "yes", "on"}:
        return True
    command = " ".join(sys.argv).lower()
    return "pytest" in command or any(part == "test" for part in sys.argv)


def forwards(apps, schema_editor):
    if _is_test_run():
        return
    call_command("import_walczak")


class Migration(migrations.Migration):
    dependencies = [
        ("walczak", "0006_preference_copy_refresh"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop, atomic=False),
    ]
