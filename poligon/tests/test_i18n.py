import pytest
from django.urls import reverse
from django.utils import translation


@pytest.mark.django_db
def test_the_english_interface_translates_the_title_and_the_navigation(client):
    switched = client.post(
        reverse("poligon:language"),
        {"lang": "en", "next": reverse("poligon:start")},
    )
    assert switched.status_code == 302
    assert client.session["poligon_lang"] == "en"
    page = client.get(switched.url)
    content = page.content.decode()
    assert "<title>Choose a level | Ćwiczba</title>" in content
    assert "Flashcards" in content
    assert "Sign in" in content
    assert 'lang="en"' in content


@pytest.mark.django_db
def test_polish_stays_the_default_interface(client):
    page = client.get(reverse("poligon:start"))
    content = page.content.decode()
    assert "<title>Wybierz poziom | Ćwiczba</title>" in content
    assert "Fiszki" in content
    assert 'lang="pl"' in content


def test_account_messages_have_an_english_catalog_entry():
    with translation.override("en"):
        assert translation.gettext("Konto potwierdzone. Możesz się zalogować.") == "Account confirmed. You can sign in."
    with translation.override("pl"):
        assert translation.gettext("Fiszki") == "Fiszki"
