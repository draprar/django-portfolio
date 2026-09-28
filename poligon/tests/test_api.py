import pytest
from django.test import Client
from django.urls import reverse

from poligon.tests.factories import make_mcq


@pytest.mark.django_db
def test_progress_belongs_to_the_account_that_earned_it(member_client):
    exercise = make_mcq()
    correct = exercise.options.get(is_correct=True)
    member_client.post(reverse("poligon:exercise", args=[exercise.slug]), {"option_id": correct.pk})

    mine = member_client.get(reverse("poligon:api_progress"))
    assert mine.status_code == 200
    assert mine.json()["target_profile"] == "2222"
    assert mine.json()["submissions"] == 1
    assert mine.json()["scores"]["R"] == 100


@pytest.mark.django_db
def test_a_guest_has_no_progress_to_report(guest_client):
    exercise = make_mcq()
    correct = exercise.options.get(is_correct=True)
    guest_client.post(reverse("poligon:exercise", args=[exercise.slug]), {"option_id": correct.pk})

    payload = guest_client.get(reverse("poligon:api_progress")).json()
    assert payload["submissions"] == 0
    assert payload["due_reviews"] == 0
    assert payload["scores"]["R"] == 0
    assert set(payload["scores"]) == {"L", "S", "R", "W"}


@pytest.mark.django_db
def test_a_caller_without_a_session_gets_zeros():
    payload = Client().get(reverse("poligon:api_progress")).json()
    assert payload["target_profile"] == "2222"
    assert payload["submissions"] == 0
