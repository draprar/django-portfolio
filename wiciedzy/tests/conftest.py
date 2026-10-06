import pytest
from django.core.management import call_command


@pytest.fixture
def full_catalog(db):
    call_command("import_wiciedzy")
