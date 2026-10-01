import pytest
from django.urls import reverse

from poligon.identity import ATTEMPT_KEY, LEVEL_KEY
from poligon.models import Submission
from poligon.tests.factories import make_mcq


def _answer(client, exercise, correct=True):
    option = exercise.options.get(is_correct=correct)
    return client.post(reverse("poligon:exercise", args=[exercise.slug]), {"option_id": option.pk})


@pytest.mark.django_db
def test_opening_an_exercise_does_not_store_an_attempt(guest_client):
    exercise = make_mcq()
    opened = guest_client.get(reverse("poligon:exercise", args=[exercise.slug]))
    assert opened.status_code == 200
    assert ATTEMPT_KEY not in guest_client.session
    assert Submission.objects.count() == 0


@pytest.mark.django_db
def test_a_guest_who_changes_level_does_not_see_the_old_result(guest_client):
    exercise = make_mcq(level=2, skill="R")
    _answer(guest_client, exercise)
    assert ATTEMPT_KEY in guest_client.session

    guest_client.post(reverse("poligon:start"), {"practice_level": "3"})

    assert ATTEMPT_KEY not in guest_client.session
    again = guest_client.get(reverse("poligon:last_result"))
    assert again.status_code == 302
    assert again.url == reverse("poligon:dashboard")


@pytest.mark.django_db
def test_a_result_stored_for_another_level_is_not_presented_as_current(guest_client):
    exercise = make_mcq(level=2)
    _answer(guest_client, exercise)
    session = guest_client.session
    session[LEVEL_KEY] = 3
    session.save()

    response = guest_client.get(reverse("poligon:last_result"))
    assert response.status_code == 302
    assert response.url == reverse("poligon:dashboard")
    assert ATTEMPT_KEY not in guest_client.session


@pytest.mark.django_db
def test_refreshing_a_result_does_not_create_another_attempt(guest_client):
    exercise = make_mcq()
    posted = _answer(guest_client, exercise)
    guest_client.get(posted.url)
    guest_client.get(posted.url)
    assert Submission.objects.count() == 0
    assert guest_client.session[ATTEMPT_KEY]["exercise_id"] == exercise.pk


@pytest.mark.django_db
def test_a_second_post_is_a_new_attempt_and_a_refresh_is_not(member_client):
    exercise = make_mcq()
    first = _answer(member_client, exercise)
    second = _answer(member_client, exercise)

    assert Submission.objects.count() == 2
    assert first.url != second.url
    member_client.get(second.url)
    assert Submission.objects.count() == 2
    page = member_client.get(second.url)
    assert page.status_code == 200


@pytest.mark.django_db
def test_an_account_does_not_see_a_result_from_another_level(member_client, state):
    exercise = make_mcq(level=2)
    posted = _answer(member_client, exercise)
    state.practice_level = 3
    state.save(update_fields=["practice_level"])

    response = member_client.get(posted.url)
    assert response.status_code == 302
    assert response.url == reverse("poligon:dashboard")


@pytest.mark.django_db
def test_a_deep_link_outside_the_plan_level_is_not_served(guest_client):
    other = make_mcq(slug="from-level-five", level=5, skill="R")
    home = make_mcq(slug="from-level-two", level=2, skill="R")

    opened = guest_client.get(reverse("poligon:exercise", args=[other.slug]))
    assert opened.status_code == 404
    posted = _answer(guest_client, other)
    assert posted.status_code == 404
    assert ATTEMPT_KEY not in guest_client.session

    queued = guest_client.get(reverse("poligon:practice"), {"skill": "R"})
    assert queued.url == reverse("poligon:exercise", args=[home.slug])
