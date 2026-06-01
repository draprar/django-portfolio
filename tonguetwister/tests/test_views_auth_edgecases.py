import pytest
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.test import RequestFactory
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from tonguetwister.tokens import account_activation_token
from tonguetwister.views_auth import contact, send_activation_email


@pytest.mark.django_db
def test_send_activation_email_skips_when_user_has_no_email(monkeypatch, rf):
    user = User.objects.create_user(username="no-email-user", email="", password="StrongPass123!")
    request = rf.get("/")

    sent = {"called": False}

    def _fake_send(*_args, **_kwargs):
        sent["called"] = True

    monkeypatch.setattr("tonguetwister.views_auth.send_brevo_email", _fake_send)

    send_activation_email(user, request)

    assert sent["called"] is False


@pytest.mark.django_db
def test_activate_handles_user_without_profile(client):
    user = User.objects.create_user(username="no-profile-user", email="u@example.com", password="StrongPass123!")
    user.profile.delete()

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    response = client.get(reverse("activate", args=[uid, token]))

    assert response.status_code == 302
    assert response.url == reverse("register")
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert any("Nie udało się aktywować konta" in msg for msg in messages)


@pytest.mark.django_db
def test_password_reset_confirm_rejects_invalid_token(client):
    user = User.objects.create_user(username="reset-invalid-token", email="r@example.com", password="StrongPass123!")
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    response = client.get(reverse("password_reset_confirm", args=[uid, "bad-token"]))

    assert response.status_code == 302
    assert response.url == reverse("password_reset")
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert any("Link resetowania hasła jest nieprawidłowy" in msg for msg in messages)


@pytest.mark.django_db
def test_login_view_invalid_does_not_authenticate_user(client):
    User.objects.create_user(username="login-user", email="login@example.com", password="CorrectPass123!")

    response = client.post(reverse("login"), {"username": "login-user", "password": "wrong-pass"})

    assert response.status_code == 200
    assert "_auth_user_id" not in client.session
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert any("Nie udało się zalogować" in msg for msg in messages)


@pytest.mark.django_db
def test_password_reset_view_get_renders_template_with_form():
    request = RequestFactory().get(reverse("password_reset"))
    session_middleware = SessionMiddleware(lambda req: None)
    session_middleware.process_request(request)
    request.session.save()
    request._messages = FallbackStorage(request)

    from tonguetwister.views_auth import password_reset_view

    response = password_reset_view(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_send_activation_email_captures_exception(monkeypatch, rf):
    user = User.objects.create_user(username="mail-fail-user", email="mail@example.com", password="StrongPass123!")
    request = rf.get("/")

    monkeypatch.setattr("tonguetwister.views_auth.send_brevo_email", lambda *_a, **_k: (_ for _ in ()).throw(RuntimeError("boom")))
    captured = {"called": False}
    monkeypatch.setattr("tonguetwister.views_auth.sentry_sdk.capture_exception", lambda _exc: captured.__setitem__("called", True))

    send_activation_email(user, request)
    assert captured["called"] is True


@pytest.mark.django_db
def test_register_view_get_returns_200(client):
    response = client.get(reverse("register"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_activate_invalid_uid_redirects_to_register(client):
    response = client.get(reverse("activate", args=["bad-uid", "token"]))

    assert response.status_code == 302
    assert response.url == reverse("register")
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert any("Link aktywacyjny jest nieprawidłowy" in msg for msg in messages)


@pytest.mark.django_db
def test_password_reset_confirm_invalid_uid_redirects(client):
    response = client.get(reverse("password_reset_confirm", args=["bad-uid", "token"]))

    assert response.status_code == 302
    assert response.url == reverse("password_reset")


@pytest.mark.django_db
def test_password_reset_complete_and_done_views_render(client):
    complete = client.get(reverse("password_reset_complete"))
    done = client.get(reverse("password_reset_done"))

    assert complete.status_code == 200
    assert done.status_code == 200


@pytest.mark.django_db
def test_contact_get_renders_form(rf):
    request = rf.get("/tonguetwister/contact/")
    session_middleware = SessionMiddleware(lambda req: None)
    session_middleware.process_request(request)
    request.session.save()
    request._messages = FallbackStorage(request)

    response = contact(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_contact_post_handles_send_mail_exception(monkeypatch, rf):
    request = rf.post("/tonguetwister/contact/", {"name": "A", "email": "a@b.com", "message": "Hi"})
    session_middleware = SessionMiddleware(lambda req: None)
    session_middleware.process_request(request)
    request.session.save()
    request._messages = FallbackStorage(request)

    class DummyForm:
        cleaned_data = {"name": "A", "email": "a@b.com", "message": "Hi"}

        def __init__(self, *_args, **_kwargs):
            pass

        def is_valid(self):
            return True

    monkeypatch.setattr("tonguetwister.views_auth.ContactForm", DummyForm)
    monkeypatch.setattr("tonguetwister.views_auth.send_mail", lambda *_a, **_k: (_ for _ in ()).throw(RuntimeError("smtp")))
    monkeypatch.setattr("tonguetwister.views_auth.redirect", lambda _name: HttpResponse(status=302))

    raw_contact = contact.__wrapped__.__wrapped__
    response = raw_contact(request)
    assert response.status_code == 302
    messages = [m.message for m in get_messages(request)]
    assert any("Nie udalo sie wyslac wiadomosci" in msg for msg in messages)



