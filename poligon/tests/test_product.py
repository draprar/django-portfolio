import json
from io import StringIO

import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from django.urls import reverse

from poligon.models import LearnerState, ProductEvent
from poligon.tests.conftest import PASSWORD, make_confirmed_user


@pytest.mark.django_db
def test_content_diff_is_empty_after_seed():
    call_command("seed_poligon")
    out = StringIO()
    call_command("diff_poligon_content", stdout=out)
    text = out.getvalue()
    report = json.loads(text.splitlines()[0])
    assert report["added"] == []
    assert report["removed"] == []
    assert report["changed"] == []
    call_command("smoke_poligon")


@pytest.mark.django_db
def test_an_account_can_export_and_then_delete_itself(client):
    user = make_confirmed_user()
    client.post(reverse("poligon:login"), {"username": user.username, "password": PASSWORD})
    state = LearnerState.objects.get(user=user)
    exported = client.get(reverse("poligon:export"))
    assert exported.status_code == 200
    payload = json.loads(exported.content)
    assert payload["username"] == user.username
    assert "password" not in payload

    refused = client.post(reverse("poligon:delete_account"), {"confirm": "no"})
    assert refused.status_code == 302
    assert User.objects.filter(pk=user.pk).exists()

    removed = client.post(reverse("poligon:delete_account"), {"confirm": "usuń"})
    assert removed.status_code == 302
    assert not User.objects.filter(pk=user.pk).exists()
    assert not LearnerState.objects.filter(pk=state.pk).exists()
    assert ProductEvent.objects.filter(learner_id=state.pk).count() == 0


@pytest.mark.django_db
def test_an_empty_sign_in_form_is_explained_on_the_server(client):
    page = client.post(reverse("poligon:login"), {"username": "", "password": ""})
    assert page.status_code == 200
    assert "Uzupełnij nazwę i hasło" in page.content.decode()
