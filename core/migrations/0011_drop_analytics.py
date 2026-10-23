"""Drop database tables and metadata for the removed analytics app (deploy cleanup)."""

from django.db import migrations

_APP_LABEL = "analytics"

# VisitLog references Visit — drop child first on SQLite; Postgres uses CASCADE.
_TABLES = (
    "analytics_visitlog",
    "analytics_visit",
)


def _drop_retired_app_schema(apps, schema_editor):
    connection = schema_editor.connection
    if connection.vendor == "postgresql":
        quoted = ", ".join(f'"{table}"' for table in _TABLES)
        schema_editor.execute(f"DROP TABLE IF EXISTS {quoted} CASCADE")
    else:
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
        ("core", "0010_alter_project_desc_code_help_text"),
    ]

    operations = [
        migrations.RunPython(_drop_retired_app_schema, migrations.RunPython.noop),
    ]
