import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def drop_guest_rows(apps, schema_editor):
    """Guest practice is no longer stored, so the rows it left behind go away."""
    LearnerState = apps.get_model("poligon", "LearnerState")
    LearnerState.objects.filter(user__isnull=True).delete()


class Migration(migrations.Migration):
    # PostgreSQL cannot ALTER TABLE in the same transaction as DML that
    # fired triggers on that table (ObjectInUse: pending trigger events).
    atomic = False

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("poligon", "0006_seed_catalog"),
    ]

    operations = [
        migrations.RunPython(drop_guest_rows, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="learnerstate",
            name="guest_token",
        ),
        migrations.AlterField(
            model_name="learnerstate",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="poligon_state",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
