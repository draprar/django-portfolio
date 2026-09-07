import json
from unittest.mock import MagicMock

import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError

from tonguetwister.models import Articulator, OldPolish, UserProfileArticulator
from tonguetwister.services import (
    add_user_collection_item,
    find_unique_user_by_email,
    is_email_confirmed,
    pick_random_row,
)
from tonguetwister.tokens import account_activation_token


@pytest.mark.django_db
def test_is_email_confirmed_requires_profile_flag():
    user = User.objects.create_user(username="u1", email="u1@example.com", password="pass")
    assert is_email_confirmed(user) is False
    user.profile.email_confirmed = True
    user.profile.save(update_fields=["email_confirmed"])
    user.refresh_from_db()
    assert is_email_confirmed(user) is True


@pytest.mark.django_db
def test_is_email_confirmed_false_without_profile():
    user = User.objects.create_user(username="u2", email="u2@example.com", password="pass")
    user.profile.delete()
    user.refresh_from_db()
    assert is_email_confirmed(user) is False


@pytest.mark.django_db
def test_find_unique_user_by_email_is_case_insensitive():
    user = User.objects.create_user(username="u3", email="Reset@Example.com", password="pass")
    assert find_unique_user_by_email("reset@example.com") == user


@pytest.mark.django_db
def test_find_unique_user_by_email_returns_none_for_duplicates(monkeypatch):
    queryset = MagicMock()
    queryset.__getitem__.return_value = [object(), object()]
    monkeypatch.setattr("tonguetwister.services.User.objects.filter", lambda **_kwargs: queryset)
    assert find_unique_user_by_email("dup@example.com") is None


@pytest.mark.django_db
def test_user_email_unique_constraint_is_case_insensitive():
    User.objects.create_user(username="a", email="Taken@Example.com", password="x")
    with pytest.raises(IntegrityError):
        User.objects.create_user(username="b", email="taken@example.com", password="x")


@pytest.mark.django_db
def test_pick_random_row_returns_none_for_empty_queryset():
    assert pick_random_row(OldPolish.objects.all()) is None


@pytest.mark.django_db
def test_pick_random_row_returns_the_only_row():
    obj = OldPolish.objects.create(old_text="stare", new_text="nowe")
    assert pick_random_row(OldPolish.objects.all()) == obj


@pytest.mark.django_db
def test_add_user_collection_item_handles_integrity_error(monkeypatch):
    user = User.objects.create_user(username="race-user", password="pass")
    articulator = Articulator.objects.create(text="art")

    def _raise(**_kwargs):
        raise IntegrityError("duplicate")

    monkeypatch.setattr(UserProfileArticulator.objects, "create", _raise)
    response = add_user_collection_item(
        model=UserProfileArticulator,
        user=user,
        related=articulator,
        related_field="articulator",
        duplicate_status="Duplicate articulator",
        added_status="Articulator added",
        id_key="userArticulatorId",
    )
    assert response.status_code == 200
    assert json.loads(response.content)["status"] == "Duplicate articulator"


@pytest.mark.django_db
def test_activation_token_invalid_after_email_confirmed():
    user = User.objects.create_user(username="tok", email="tok@example.com", password="pass")
    token = account_activation_token.make_token(user)
    assert account_activation_token.check_token(user, token) is True
    user.profile.email_confirmed = True
    user.profile.save(update_fields=["email_confirmed"])
    user.refresh_from_db()
    assert account_activation_token.check_token(user, token) is False
