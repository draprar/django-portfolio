import pytest
from django.contrib.auth.models import User

from tonguetwister.services import find_unique_user_by_email, is_email_confirmed
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
def test_find_unique_user_by_email_returns_none_for_duplicates():
    User.objects.create_user(username="dup-a", email="dup@example.com", password="pass")
    User.objects.create_user(username="dup-b", email="DUP@example.com", password="pass")
    assert find_unique_user_by_email("dup@example.com") is None


@pytest.mark.django_db
def test_activation_token_invalid_after_email_confirmed():
    user = User.objects.create_user(username="tok", email="tok@example.com", password="pass")
    token = account_activation_token.make_token(user)
    assert account_activation_token.check_token(user, token) is True
    user.profile.email_confirmed = True
    user.profile.save(update_fields=["email_confirmed"])
    user.refresh_from_db()
    assert account_activation_token.check_token(user, token) is False
