import importlib

migration = importlib.import_module("walczak.migrations.0005_import_catalog")


def test_catalog_import_skips_the_test_suite():
    called = []
    original = migration.call_command
    migration.call_command = lambda *args, **kwargs: called.append(args)
    try:
        migration.forwards(None, None)
    finally:
        migration.call_command = original

    assert called == []


def test_catalog_import_runs_for_a_normal_migrate(monkeypatch):
    monkeypatch.setattr(migration.sys, "argv", ["manage.py", "migrate", "--noinput"])
    monkeypatch.delenv("DJANGO_TESTING", raising=False)
    called = []
    monkeypatch.setattr(migration, "call_command", lambda *args, **kwargs: called.append(args))

    migration.forwards(None, None)

    assert called == [("import_walczak",)]
