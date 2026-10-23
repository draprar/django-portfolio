"""Rugby has no ORM models — public content lives in rugby/data/."""


def test_rugby_has_no_orm_models():
    from django.apps import apps

    assert list(apps.get_app_config("rugby").get_models()) == []
