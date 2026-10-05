"""Load the current catalog when migrate runs outside the test suite.

The free Render plan has no shell. Deploy already runs migrate, and that is
what has to insert the preference questions, the joke, and the sketch.
"""

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
    call_command("import_wiciedzy")


class Migration(migrations.Migration):
    dependencies = [
        ("walczak", "0004_quality_pass"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop, atomic=False),
    ]
