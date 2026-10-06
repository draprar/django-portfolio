import pytest
from django.contrib import admin
from django.test import override_settings
from django.urls import reverse

from wiciedzy.models import Question, Style, Tag


@pytest.mark.django_db
def test_home_is_bilingual(client):
    response = client.get(reverse("wiciedzy:home"))
    content = response.content.decode()

    assert response.status_code == 200
    assert ">wiciędze</a>" in content
    assert 'data-pl="Katalog"' in content
    assert 'data-en="Catalog"' in content
    assert "Siemasz na wiciędze" not in content
    assert "Boks boks, albo kop kop" in content
    assert "a jak nie to se ogarnij inne" in content
    assert "wiciedzy-home-tagline" in content
    assert "obczaj niżej" not in content
    assert "Quizopasowanie" in content
    assert 'property="og:title"' in content
    assert 'data-en="A catalog of combat sports and martial arts, a check of what you want from training, a comparison tool and a bit of a laugh."' in content
    assert 'data-pl="Quizopasowanie"' in content
    assert 'data-pl="Archetyp"' not in content
    assert "karuzela śmiechu" not in content
    assert "navbar-toggler" not in content
    assert "navbar navbar-expand" not in content
    assert "bootstrap" not in content
    assert "wiciedzy-stage" in content
    assert "wiciedzy-portal" in content
    assert 'data-pl="Szkic"' not in content
    assert 'data-pl="Poznaj"' not in content
    assert 'data-pl="Jaki trening"' not in content
    assert 'href="/wiciedze/porownaj/"' not in content
    assert "core/js/lang.js" in content
    assert "lang-btn" in content


@pytest.mark.django_db
def test_list_ignores_family_query(client):
    response = client.get(reverse("wiciedzy:list"), {"rodzina": "chwyty"})
    content = response.content.decode()

    assert response.status_code == 200
    assert "Judo" in content
    assert "Boks" in content
    assert "Se porównaj:" in content
    assert reverse("wiciedzy:compare_form") in content
    assert 'name="a"' in content
    assert 'data-pl="Katalog"' in content
    assert 'data-pl="Wszystkie"' not in content
    assert "Mniej oczywiste" not in content
    assert "Losowy fakt" not in content


@pytest.mark.django_db
def test_unknown_family_shows_the_whole_list(client):
    response = client.get(reverse("wiciedzy:list"), {"rodzina": "nie-ma"})
    content = response.content.decode()

    assert "Boks" in content
    assert "Judo" in content


@pytest.mark.django_db
def test_detail_shows_history_and_source(client):
    response = client.get(reverse("wiciedzy:detail", args=["boks"]))
    content = response.content.decode()

    assert response.status_code == 200
    assert "Historia" in content
    assert "Jak się walczy" in content
    assert "https://www.britannica.com/sports/boxing" in content
    assert 'data-en="Boxing"' in content


@pytest.mark.django_db
def test_unclear_sources_copy(client):
    Style.objects.filter(slug="boks").update(sources_disagree=True)
    response = client.get(reverse("wiciedzy:detail", args=["boks"]))
    content = response.content.decode()

    assert response.status_code == 200
    assert "Nie da się uczciwie podać jednej wersji, źródła są niejasne." in content
    assert "Źródła się nie zgadzają." not in content


@pytest.mark.django_db
def test_inactive_style_is_missing(client):
    Style.objects.filter(slug="boks").update(active=False)

    response = client.get(reverse("wiciedzy:detail", args=["boks"]))

    assert response.status_code == 404


@pytest.mark.django_db
@override_settings(DEBUG=False)
def test_archetype_urls_are_gone(client):
    assert client.get("/wiciedze/quiz/").status_code == 404
    assert client.get("/wiciedze/wynik/").status_code == 404
    assert "Tu nic nie ma." in client.get("/wiciedze/quiz/").content.decode()


def test_styles_are_in_the_admin():
    assert Style in admin.site._registry
    assert Question in admin.site._registry


@pytest.mark.django_db
def test_catalog_copy_says_style_not_discipline(client):
    response = client.get(reverse("wiciedzy:list"))
    content = response.content.decode()

    assert "Obczaj różne sporty i sztuki walki" in content
    assert "dyscyplin" not in content
    assert 'data-en="Catalog"' in content


@pytest.mark.django_db
def test_empty_tag_does_not_blame_the_family(client):
    Tag.objects.create(slug="pusty", name_pl="Pusty", name_en="Empty")
    response = client.get(reverse("wiciedzy:list"), {"tag": "pusty"})
    content = response.content.decode()

    assert "Żaden styl nie ma tego tagu." in content
    assert "Brak stylów w tej rodzinie" not in content


@pytest.mark.django_db
def test_sitemap_lists_public_pages_only(client):
    response = client.get(reverse("wiciedzy:sitemap"))
    body = response.content.decode()

    assert response.status_code == 200
    assert response["Content-Type"].startswith("application/xml")
    assert reverse("wiciedzy:detail", args=["boks"]) in body
    assert "/wiciedze/quiz/" not in body
    assert reverse("wiciedzy:test") not in body
    assert reverse("wiciedzy:match") not in body
    assert "/wiciedze/wynik/" not in body
    assert "/wiciedze/zlote/" not in body
    assert "/wiciedze/fakt/" not in body


@pytest.mark.django_db
@override_settings(DEBUG=False)
def test_old_personality_url_is_gone(client):
    response = client.get("/wiciedze/osobowosc/")

    assert response.status_code == 404
    assert "Tu nic nie ma." in response.content.decode()


@pytest.mark.django_db
def test_api_cache_headers(client):
    listing = client.get(reverse("wiciedzy:api-styles"))
    fact = client.get(reverse("wiciedzy:api-fact"))

    assert "public" in listing["Cache-Control"]
    assert "max-age=300" in listing["Cache-Control"]
    assert "no-store" in fact["Cache-Control"]
