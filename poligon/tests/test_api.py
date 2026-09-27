import pytest
from django.test import Client
from django.urls import reverse

from poligon.tests.factories import make_mcq


@pytest.mark.django_db
def test_progress_is_scoped_to_the_caller_session(client):
    exercise = make_mcq()
    correct = exercise.options.get(is_correct=True)
    client.post(reverse("poligon:exercise", args=[exercise.slug]), {"option_id": correct.pk})

    mine = client.get(reverse("poligon:api_progress"))
    other = Client().get(reverse("poligon:api_progress"))

    assert mine.status_code == 200
    assert mine.json()["target_profile"] == "2222"
    assert mine.json()["submissions"] == 1
    assert mine.json()["scores"]["R"] == 100
    assert other.json()["submissions"] == 0
    assert other.json()["scores"]["R"] == 0
    assert set(other.json()["scores"]) == {"L", "S", "R", "W"}
