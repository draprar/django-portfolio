import pytest
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


@pytest.mark.django_db
def test_password_reset_confirm_rejects_weak_password(client):
    user = User.objects.create_user(
        username="reset-user",
        email="reset@example.com",
        password="OldStrongPass123!",
    )
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    url = reverse("password_reset_confirm", args=[uid, token])

    response = client.post(
        url,
        {
            "new_password1": "123",
            "new_password2": "123",
        },
    )

    user.refresh_from_db()
    assert response.status_code == 200
    assert user.check_password("OldStrongPass123!")


@pytest.mark.django_db
def test_password_reset_confirm_accepts_valid_password(client):
    user = User.objects.create_user(
        username="reset-user-2",
        email="reset2@example.com",
        password="OldStrongPass123!",
    )
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    url = reverse("password_reset_confirm", args=[uid, token])

    response = client.post(
        url,
        {
            "new_password1": "NewStrongPass456!",
            "new_password2": "NewStrongPass456!",
        },
    )

    user.refresh_from_db()
    assert response.status_code == 302
    assert response.url == reverse("password_reset_complete")
    assert user.check_password("NewStrongPass456!")


@pytest.mark.django_db
def test_password_reset_confirm_requires_both_password_fields(client):
    user = User.objects.create_user(
        username="reset-user-3",
        email="reset3@example.com",
        password="OldStrongPass123!",
    )
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    url = reverse("password_reset_confirm", args=[uid, token])

    response = client.post(
        url,
        {
            "new_password1": "",
            "new_password2": "",
        },
    )

    user.refresh_from_db()
    assert response.status_code == 200
    assert user.check_password("OldStrongPass123!")


@pytest.mark.django_db
def test_password_reset_email_lookup_is_case_insensitive(client):
    user = User.objects.create_user(
        username="reset-user-4",
        email="ResetCase@example.com",
        password="OldStrongPass123!",
    )

    response = client.post(reverse("password_reset"), {"email": "resetcase@EXAMPLE.com"})

    assert response.status_code == 302
    assert response.url == reverse("password_reset_done")
    user.refresh_from_db()
