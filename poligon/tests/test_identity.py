import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from poligon.identity import GUEST_COOKIE
from poligon.models import LearnerState, Review, StudyEvent, Submission
from poligon.tests.factories import make_mcq, make_vocabulary


def confirmed_user(username="walery", password="Poligon!2345") -> User:
    user = User.objects.create_user(username=username, email=f"{username}@example.com", password=password)
    user.profile.email_confirmed = True
    user.profile.save(update_fields=["email_confirmed"])
    return user


def answer(client, exercise, correct=True):
    option = exercise.options.get(is_correct=correct)
    return client.post(reverse("poligon:exercise", args=[exercise.slug]), {"option_id": option.pk})


@pytest.mark.django_db
def test_a_guest_gets_a_cookie_and_keeps_progress_across_sessions(client):
    exercise = make_mcq()
    answer(client, exercise)
    token = client.cookies[GUEST_COOKIE].value
    assert token

    # A new session with the same cookie is the same learner.
    returning = Client()
    returning.cookies[GUEST_COOKIE] = token
    assert returning.get(reverse("poligon:api_progress")).json()["submissions"] == 1
    assert LearnerState.objects.count() == 1


@pytest.mark.django_db
def test_a_different_browser_is_a_different_learner(client):
    answer(client, make_mcq())
    assert Client().get(reverse("poligon:api_progress")).json()["submissions"] == 0


@pytest.mark.django_db
def test_practice_needs_no_account(client):
    exercise = make_mcq()
    posted = answer(client, exercise)
    assert posted.status_code == 302
    assert client.get(reverse("poligon:dashboard")).status_code == 200
    assert LearnerState.objects.get().user is None


@pytest.mark.django_db
def test_the_dashboard_only_nags_a_guest_who_has_something_to_lose(client):
    quiet = client.get(reverse("poligon:dashboard")).content.decode()
    assert "tylko w tej przeglądarce" not in quiet

    answer(client, make_mcq())
    nagged = client.get(reverse("poligon:dashboard")).content.decode()
    assert "tylko w tej przeglądarce" in nagged
    assert reverse("poligon:account") in nagged


@pytest.mark.django_db
def test_signing_in_moves_the_guest_work_onto_the_account(client):
    password = "Poligon!2345"
    user = confirmed_user(password=password)
    exercise = make_mcq()
    answer(client, exercise)
    make_vocabulary()
    client.get(reverse("poligon:reviews"))
    client.post(
        reverse("poligon:settings"),
        {"practice_level": "4", "daily_minutes": "50", "target_date": ""},
    )
    guest = LearnerState.objects.get()

    signed_in = client.post(
        reverse("poligon:login"),
        {"username": user.username, "password": password},
    )
    assert signed_in.status_code == 302
    assert signed_in.url == reverse("poligon:dashboard")

    state = LearnerState.objects.get()
    assert state.user == user
    assert not LearnerState.objects.filter(pk=guest.pk).exists()
    assert Submission.objects.filter(learner=state).count() == 1
    assert StudyEvent.objects.filter(learner=state).count() == 1
    assert Review.objects.filter(learner=state).exists()
    assert state.practice_level == 4
    assert state.target_profile == "4444"
    assert state.daily_minutes == 50
    assert client.cookies[GUEST_COOKIE].value == ""


@pytest.mark.django_db
def test_the_account_keeps_the_harder_level_after_a_merge(client):
    password = "Poligon!2345"
    user = confirmed_user(password=password)
    account = LearnerState.objects.create(user=user, practice_level=5, target_profile="5555")
    Submission.objects.create(learner=account, exercise=make_mcq(slug="old-work"), score=90)

    client.post(
        reverse("poligon:settings"),
        {"practice_level": "1", "daily_minutes": "20", "target_date": ""},
    )
    client.post(reverse("poligon:login"), {"username": user.username, "password": password})

    state = LearnerState.objects.get(user=user)
    assert state.practice_level == 5
    assert state.target_profile == "5555"


@pytest.mark.django_db
def test_a_fresh_account_takes_the_plan_the_guest_already_chose(client):
    password = "Poligon!2345"
    user = confirmed_user(password=password)
    client.post(
        reverse("poligon:settings"),
        {"practice_level": "1", "daily_minutes": "20", "target_date": ""},
    )
    client.post(reverse("poligon:login"), {"username": user.username, "password": password})

    state = LearnerState.objects.get(user=user)
    assert state.practice_level == 1
    assert state.daily_minutes == 20


@pytest.mark.django_db
def test_a_second_browser_sees_the_account_progress(client):
    password = "Poligon!2345"
    user = confirmed_user(password=password)
    answer(client, make_mcq())
    client.post(reverse("poligon:login"), {"username": user.username, "password": password})

    elsewhere = Client()
    elsewhere.post(reverse("poligon:login"), {"username": user.username, "password": password})
    assert elsewhere.get(reverse("poligon:api_progress")).json()["submissions"] == 1


@pytest.mark.django_db
def test_two_accounts_never_see_each_other(client):
    password = "Poligon!2345"
    mine = confirmed_user(password=password)
    confirmed_user(username="other", password=password)
    answer(client, make_mcq())
    client.post(reverse("poligon:login"), {"username": mine.username, "password": password})

    theirs = Client()
    theirs.post(reverse("poligon:login"), {"username": "other", "password": password})
    assert theirs.get(reverse("poligon:api_progress")).json()["submissions"] == 0


@pytest.mark.django_db
def test_an_unconfirmed_account_cannot_sign_in(client):
    password = "Poligon!2345"
    User.objects.create_user(username="fresh", email="fresh@example.com", password=password)
    response = client.post(reverse("poligon:login"), {"username": "fresh", "password": password})
    assert response.status_code == 200
    assert "Nie udało się zalogować" in response.content.decode()


@pytest.mark.django_db
def test_signing_out_leaves_the_progress_on_the_account(client):
    password = "Poligon!2345"
    user = confirmed_user(password=password)
    answer(client, make_mcq())
    client.post(reverse("poligon:login"), {"username": user.username, "password": password})

    assert client.post(reverse("poligon:logout")).status_code == 302
    assert client.get(reverse("poligon:api_progress")).json()["submissions"] == 0
    assert Submission.objects.filter(learner__user=user).count() == 1


@pytest.mark.django_db
def test_the_account_page_speaks_to_guests_and_to_members(client):
    guest = client.get(reverse("poligon:account")).content.decode()
    assert "tylko w tej przeglądarce" in guest
    assert reverse("poligon:register") in guest

    password = "Poligon!2345"
    user = confirmed_user(password=password)
    client.post(reverse("poligon:login"), {"username": user.username, "password": password})
    member = client.get(reverse("poligon:account")).content.decode()
    assert user.username in member
    assert reverse("poligon:logout") in member
