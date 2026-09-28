import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from poligon.identity import LEVEL_KEY
from poligon.models import LearnerState

PASSWORD = "Poligon!2345"


def make_confirmed_user(username: str = "walery") -> User:
    """A user who has clicked the activation link, so sign-in works."""
    user = User.objects.create_user(
        username=username,
        email=f"{username}@example.com",
        password=PASSWORD,
    )
    user.profile.email_confirmed = True
    user.profile.save(update_fields=["email_confirmed"])
    return user


def sign_in(client: Client, user: User) -> None:
    """Through the form, so the sign-in side effects run as they do live."""
    client.post(reverse("poligon:login"), {"username": user.username, "password": PASSWORD})


def pick_level(client: Client, level: int = 2) -> None:
    """What a guest does on the start page before anything else works."""
    session = client.session
    session[LEVEL_KEY] = level
    session.save()


@pytest.fixture
def member(db) -> User:
    return make_confirmed_user()


@pytest.fixture
def member_client(client, member) -> Client:
    client.force_login(member)
    return client


@pytest.fixture
def guest_client(client) -> Client:
    pick_level(client)
    return client


@pytest.fixture
def state(member) -> LearnerState:
    return LearnerState.objects.get_or_create(user=member)[0]
