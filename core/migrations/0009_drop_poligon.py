"""Drop database tables and metadata for a removed Django app (deploy cleanup)."""

from django.db import migrations

_APP_LABEL = "poligon"

_TABLES = (
    "poligon_choiceoption",
    "poligon_submission",
    "poligon_review",
    "poligon_savedword",
    "poligon_contentreport",
    "poligon_studyevent",
    "poligon_placementattempt",
    "poligon_productevent",
    "poligon_exercise",
    "poligon_vocabularyitem",
    "poligon_learnerstate",
)


def _drop_retired_app_schema(apps, schema_editor):
    connection = schema_editor.connection
    if connection.vendor == "sqlite":
        schema_editor.execute("PRAGMA foreign_keys = OFF")
    for table in _TABLES:
        schema_editor.execute(f'DROP TABLE IF EXISTS "{table}"')
    schema_editor.execute(
        "DELETE FROM auth_permission WHERE content_type_id IN "
        f"(SELECT id FROM django_content_type WHERE app_label = '{_APP_LABEL}')"
    )
    schema_editor.execute(f"DELETE FROM django_content_type WHERE app_label = '{_APP_LABEL}'")
    schema_editor.execute(f"DELETE FROM django_migrations WHERE app = '{_APP_LABEL}'")


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_rewrite_expired_live_urls"),
    ]

    operations = [
        migrations.RunPython(_drop_retired_app_schema, migrations.RunPython.noop),
    ]
