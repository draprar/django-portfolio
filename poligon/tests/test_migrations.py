import importlib


def _migration(module_name: str):
    return importlib.import_module(f"poligon.migrations.{module_name}").Migration


def test_identity_migration_does_not_share_a_transaction_with_alters():
    """DML then ALTER on poligon_learnerstate fails on PostgreSQL if atomic."""
    assert _migration("0004_learner_identity").atomic is False


def test_account_migration_does_not_share_a_transaction_with_alters():
    """Deleting guest rows then dropping guest_token hits the same PostgreSQL error."""
    assert _migration("0007_learner_state_needs_an_account").atomic is False
