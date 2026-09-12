from urllib.parse import urlparse

from django.db import migrations

_EXPIRED_LIVE_HOSTS = frozenset(
    {
        "walery.site",
        "www.walery.site",
    }
)


def rewrite_expired_live_urls(apps, schema_editor):
    Project = apps.get_model("core", "Project")
    for project in Project.objects.exclude(live_url="").iterator():
        parsed = urlparse(project.live_url)
        host = (parsed.hostname or "").lower()
        if host not in _EXPIRED_LIVE_HOSTS:
            continue
        path = parsed.path or "/"
        if parsed.query:
            path = f"{path}?{parsed.query}"
        if parsed.fragment:
            path = f"{path}#{parsed.fragment}"
        project.live_url = path
        project.save(update_fields=["live_url"])


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_populate_project_desc_code"),
    ]

    operations = [
        migrations.RunPython(rewrite_expired_live_urls, migrations.RunPython.noop),
    ]
