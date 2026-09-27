import os
import sys

from django.db import migrations


def seed_catalog(apps, schema_editor):
    """Load the training catalog into the database migrate is actually using.

    The Render service runs migrate on deploy. The seed command in render.yaml
    is not applied until the blueprint is synced, so a code deploy can leave
    the exercise tables empty. Tests skip this.
    """
    from django.conf import settings

    argv = " ".join(sys.argv).lower()
    database_name = str(settings.DATABASES["default"]["NAME"]).lower()
    if (
        "pytest" in argv
        or "py.test" in argv
        or os.environ.get("PYTEST_CURRENT_TEST")
        or os.environ.get("DJANGO_TESTING", "").lower() in {"1", "true", "yes"}
        or database_name.endswith("test_db.sqlite3")
        or "test_" in database_name
    ):
        return
    from django.core.management import call_command

    call_command("seed_poligon")


class Migration(migrations.Migration):

    dependencies = [
        ("poligon", "0005_exercise_explanation"),
    ]

    operations = [
        migrations.RunPython(seed_catalog, migrations.RunPython.noop),
    ]
