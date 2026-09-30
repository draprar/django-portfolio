from django.db import migrations

from walczak.seed import load


def forwards(apps, schema_editor):
    load(
        apps.get_model("walczak", "Style"),
        apps.get_model("walczak", "Source"),
        apps.get_model("walczak", "Question"),
        apps.get_model("walczak", "Choice"),
    )


def backwards(apps, schema_editor):
    apps.get_model("walczak", "Question").objects.all().delete()
    apps.get_model("walczak", "Source").objects.all().delete()
    apps.get_model("walczak", "Style").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("walczak", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
