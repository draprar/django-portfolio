import pytest
from django.contrib import admin
from django.core.cache import cache
from django.test import override_settings
from django.urls import reverse

from walczak.models import Archetype, HumorChoice, HumorQuestion, Question, Style, Tag


@pytest.mark.django_db
def test_home_is_bilingual(client):
    response = client.get(reverse("walczak:home"))
    content = response.content.decode()

    assert response.status_code == 200
    assert "Walczak" in content
    assert 'data-pl="Poznaj"' in content
    assert 'data-en="Browse"' in content
    assert "nie wybiera stylu" in content
    assert 'property="og:title"' in content
    assert 'data-en="A catalog of combat sports and martial arts, a preference check, a comparison, and a joke."' in content
    assert 'data-pl="Jaki trening"' in content
    assert 'data-pl="Żart"' in content
    assert 'data-pl="Szkic"' in content
    assert 'data-pl="Porównaj"' in content
    assert "core/js/lang.js" in content
    assert "lang-btn" in content


@pytest.mark.django_db
def test_list_filters_by_family(client):
    response = client.get(reverse("walczak:list"), {"rodzina": "chwyty"})
    content = response.content.decode()

    assert response.status_code == 200
    assert "Judo" in content
    assert "Boks" not in content


@pytest.mark.django_db
def test_unknown_family_shows_the_whole_list(client):
    response = client.get(reverse("walczak:list"), {"rodzina": "nie-ma"})
    content = response.content.decode()

    assert "Boks" in content
    assert "Judo" in content


@pytest.mark.django_db
def test_empty_family_says_so(client):
    Style.objects.filter(family="chwyty").update(active=False)

    response = client.get(reverse("walczak:list"), {"rodzina": "chwyty"})
    content = response.content.decode()

    assert "Brak stylów w tej rodzinie" in content
    assert "Pokaż wszystkie" in content


@pytest.mark.django_db
def test_detail_shows_history_and_source(client):
    response = client.get(reverse("walczak:detail", args=["boks"]))
    content = response.content.decode()

    assert response.status_code == 200
    assert "Historia" in content
    assert "Jak się walczy" in content
    assert "https://www.britannica.com/sports/boxing" in content
    assert 'data-en="Boxing"' in content


@pytest.mark.django_db
def test_inactive_style_is_missing(client):
    Style.objects.filter(slug="boks").update(active=False)

    response = client.get(reverse("walczak:detail", args=["boks"]))

    assert response.status_code == 404


@pytest.fixture
def humor_ready(db):
    archetype = Archetype.objects.create(
        slug="chce-miecz",
        name_pl="Człowiek, który chce miecz",
        name_en="The person who wants a sword",
        description_pl="Pytasz o stal.",
        description_en="You ask about the steel.",
    )
    question = HumorQuestion.objects.create(
        text_pl="Wchodzisz na salę pierwszy raz. Czego szukasz wzrokiem?",
        text_en="You walk into a hall for the first time. What do your eyes look for?",
        sort_order=1,
    )
    HumorChoice.objects.create(
        question=question,
        text_pl="Czy jest tu miecz.",
        text_en="Whether there is a sword.",
        archetype=archetype,
        points=1,
    )
    return archetype


@pytest.mark.django_db
def test_quiz_page_lists_the_questions(client, humor_ready):
    response = client.get(reverse("walczak:quiz"))
    content = response.content.decode()

    assert response.status_code == 200
    assert "Wchodzisz na salę pierwszy raz" in content
    assert 'data-en="You walk into a hall for the first time. What do your eyes look for?"' in content
    assert "walczak-option" in content


@pytest.mark.django_db
def test_quiz_without_active_styles_stays_empty(client):
    Style.objects.update(active=False)

    response = client.post(reverse("walczak:quiz"), {})

    assert response.status_code == 200
    assert "Brak pytań" in content_of(response)


def content_of(response) -> str:
    return response.content.decode()


@pytest.mark.django_db
def test_blank_quiz_post_stays_on_the_form(client, humor_ready):
    response = client.post(reverse("walczak:quiz"), {})
    content = response.content.decode()

    assert response.status_code == 200
    assert "Zaznacz odpowiedzi." in content
    assert "walczak_result" not in client.session


@pytest.mark.django_db
def test_quiz_post_lands_on_an_archetype(client, humor_ready):
    question = HumorQuestion.objects.get()
    choice = question.choices.get()

    response = client.post(reverse("walczak:quiz"), {f"q{question.pk}": choice.pk})

    assert response.status_code == 302
    result = client.get(reverse("walczak:result"))
    assert result.status_code == 200
    assert client.session["walczak_result"]["archetype_slugs"] == ["chce-miecz"]


@pytest.mark.django_db
def test_result_without_a_session_goes_back_to_the_quiz(client):
    response = client.get(reverse("walczak:result"))

    assert response.status_code == 302
    assert response.url == reverse("walczak:quiz")


@pytest.mark.django_db
def test_result_rejects_a_broken_session(client):
    session = client.session
    session["walczak_result"] = {"style_id": "nie-liczba"}
    session.save()

    response = client.get(reverse("walczak:result"))

    assert response.status_code == 302
    assert response.url == reverse("walczak:quiz")


@pytest.mark.django_db
def test_result_rejects_an_inactive_style(client):
    style = Style.objects.get(slug="boks")
    style.active = False
    style.save(update_fields=["active"])
    session = client.session
    session["walczak_result"] = {"style_id": style.pk}
    session.save()

    response = client.get(reverse("walczak:result"))

    assert response.status_code == 302
    assert response.url == reverse("walczak:quiz")


@pytest.mark.django_db
def test_quiz_without_questions_stays_on_the_page(client, humor_ready):
    HumorQuestion.objects.update(active=False)
    Question.objects.update(active=False)

    response = client.post(reverse("walczak:quiz"), {})
    content = response.content.decode()

    assert response.status_code == 200
    assert "Brak pytań" in content


@pytest.mark.django_db
@override_settings(RATELIMIT_ENABLE=True)
def test_quiz_post_is_rate_limited(client, humor_ready):
    cache.clear()
    url = reverse("walczak:quiz")
    remote = {"REMOTE_ADDR": "203.0.113.44"}

    question = HumorQuestion.objects.get()
    choice = question.choices.get()
    payload = {f"q{question.pk}": choice.pk}
    for _ in range(10):
        response = client.post(url, payload, **remote)
        assert response.status_code == 302

    blocked = client.post(url, payload, **remote)
    assert blocked.status_code == 403


@pytest.mark.django_db
def test_tied_quiz_shows_both_archetypes(client, humor_ready):
    other = Archetype.objects.create(
        slug="rycerz-regulaminu",
        name_pl="Rycerz regulaminu",
        name_en="Knight of the rulebook",
        description_pl="Linia i punkt.",
        description_en="A line and a point.",
    )
    question = HumorQuestion.objects.get()
    HumorChoice.objects.create(
        question=question,
        text_pl="Regulamin jest na ścianie.",
        text_en="The rulebook is on the wall.",
        archetype=other,
        points=1,
        sort_order=1,
    )
    sword = question.choices.get(archetype=humor_ready)
    second = HumorQuestion.objects.create(text_pl="Druga", text_en="Second", sort_order=2)
    HumorChoice.objects.create(
        question=second,
        text_pl="Miecz.",
        text_en="Sword.",
        archetype=humor_ready,
        points=1,
    )
    knight = HumorChoice.objects.create(
        question=second,
        text_pl="Regulamin.",
        text_en="Rules.",
        archetype=other,
        points=1,
        sort_order=1,
    )
    response = client.post(
        reverse("walczak:quiz"),
        {f"q{question.pk}": str(sword.pk), f"q{second.pk}": str(knight.pk)},
    )
    assert response.status_code == 302
    page = client.get(reverse("walczak:result")).content.decode()
    assert "Wyszło równo." in page
    assert page.count("<h1") == 1
    assert "Człowiek, który chce miecz" in page
    assert "Rycerz regulaminu" in page


@pytest.mark.django_db
def test_blank_quiz_after_a_result_drops_the_old_archetype(client, humor_ready):
    question = HumorQuestion.objects.get()
    choice = question.choices.get()
    saved = client.post(reverse("walczak:quiz"), {f"q{question.pk}": choice.pk})
    assert saved.status_code == 302

    blank = client.post(reverse("walczak:quiz"), {})

    assert blank.status_code == 200
    assert "walczak_result" not in client.session
    assert client.get(reverse("walczak:result")).status_code == 302


def test_styles_are_in_the_admin():
    assert Style in admin.site._registry
    assert Question in admin.site._registry


@pytest.mark.django_db
def test_catalog_copy_says_style_not_discipline(client):
    response = client.get(reverse("walczak:list"))
    content = response.content.decode()

    assert "Trzydzieści głównych stylów" in content
    assert "dyscyplin" not in content
    assert 'data-en="Browse"' in content


@pytest.mark.django_db
def test_empty_tag_does_not_blame_the_family(client):
    Tag.objects.create(slug="pusty", name_pl="Pusty", name_en="Empty")
    response = client.get(reverse("walczak:list"), {"tag": "pusty"})
    content = response.content.decode()

    assert "Żaden styl nie ma tego tagu." in content
    assert "Brak stylów w tej rodzinie" not in content


@pytest.mark.django_db
def test_sitemap_lists_public_pages_only(client):
    response = client.get(reverse("walczak:sitemap"))
    body = response.content.decode()

    assert response.status_code == 200
    assert response["Content-Type"].startswith("application/xml")
    assert reverse("walczak:detail", args=["boks"]) in body
    assert reverse("walczak:golden") in body
    assert reverse("walczak:quiz") not in body
    assert reverse("walczak:test") not in body
    assert reverse("walczak:match") not in body
    assert reverse("walczak:fact") not in body
    assert reverse("walczak:personality") not in body
    assert reverse("walczak:result") not in body


@pytest.mark.django_db
def test_api_cache_headers(client):
    listing = client.get(reverse("walczak:api-styles"))
    fact = client.get(reverse("walczak:api-fact"))

    assert "public" in listing["Cache-Control"]
    assert "max-age=300" in listing["Cache-Control"]
    assert "no-store" in fact["Cache-Control"]
