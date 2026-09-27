"""Optional accounts for Poligon.

Practice never needs one. An account exists so a learner keeps their level,
flashcard schedule and history when the guest cookie goes away or they open
Poligon somewhere else. It is the project-wide ``django.contrib.auth`` user, so
one account works across the whole portfolio, but every page here is Poligon's.
"""

from __future__ import annotations

import logging

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.html import escape
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

from core.email import send_brevo_email
from tonguetwister.forms import CustomUserCreationForm, StrongSetPasswordForm
from tonguetwister.services import (
    LOGIN_FAILURE_MESSAGE,
    find_unique_user_by_email,
    is_email_confirmed,
)
from tonguetwister.tokens import account_activation_token

from .identity import adopt_guest_progress, learner_state
from .models import Submission
from .services import due_review_count

logger = logging.getLogger(__name__)

SIGNED_UP = "Konto jest prawie gotowe. Sprawdź skrzynkę i kliknij link, żeby je potwierdzić."
ACTIVATED = "Konto potwierdzone. Możesz się zalogować."
ACTIVATION_BROKEN = "Ten link już nie działa. Zarejestruj się jeszcze raz albo napisz do nas."
PROGRESS_MOVED = "Twój dotychczasowy postęp jest już na koncie."
PASSWORD_SENT = "Jeśli konto istnieje, wyślemy link do zmiany hasła."
PASSWORD_CHANGED = "Hasło zmienione. Zaloguj się nowym hasłem."
PASSWORD_LINK_BROKEN = "Ten link do zmiany hasła już nie działa. Poproś o nowy."


def account(request: HttpRequest) -> HttpResponse:
    state = learner_state(request)
    return render(
        request,
        "poligon/account.html",
        {
            "state": state,
            "done": Submission.objects.filter(learner=state).count(),
            "due_reviews": due_review_count(state),
        },
    )


@csrf_protect
@ratelimit(key="ip", rate="10/5m", method="POST", block=True)
def login_view(request: HttpRequest) -> HttpResponse:
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            if not is_email_confirmed(user):
                messages.error(request, LOGIN_FAILURE_MESSAGE)
                return render(request, "poligon/auth_login.html", {"form": form})
            login(request, user)
            if adopt_guest_progress(request, learner_state(request)):
                messages.success(request, PROGRESS_MOVED)
            return redirect("poligon:dashboard")
        messages.error(request, LOGIN_FAILURE_MESSAGE)
    return render(request, "poligon/auth_login.html", {"form": form})


@require_POST
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("poligon:dashboard")


@ratelimit(key="ip", rate="5/10m", method="POST", block=True)
def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            _send_activation_email(user, request)
            messages.success(request, SIGNED_UP)
            return redirect("poligon:login")
        for errors in form.errors.values():
            for error in errors:
                messages.error(request, error)
        return render(request, "poligon/auth_register.html", {"form": form})
    return render(request, "poligon/auth_register.html", {"form": CustomUserCreationForm()})


@ratelimit(key="ip", rate="5/10m", method="GET", block=True)
def activate(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    user = _user_from_uid(uidb64)
    if user is not None and account_activation_token.check_token(user, token):
        try:
            profile = user.profile
        except ObjectDoesNotExist:
            logger.warning("Poligon activation without a profile for user_id=%s", user.pk)
            messages.error(request, ACTIVATION_BROKEN)
            return redirect("poligon:register")
        profile.email_confirmed = True
        profile.save(update_fields=["email_confirmed"])
        messages.success(request, ACTIVATED)
        return redirect("poligon:login")
    messages.error(request, ACTIVATION_BROKEN)
    return redirect("poligon:register")


@csrf_protect
@ratelimit(key="ip", rate="5/10m", method="POST", block=True)
def password_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user = find_unique_user_by_email((request.POST.get("email") or "").strip())
        if user is not None:
            _send_password_email(user, request)
        # Same answer either way, so the form never confirms who has an account.
        messages.success(request, PASSWORD_SENT)
        return redirect("poligon:login")
    return render(request, "poligon/auth_password.html")


@csrf_protect
@ratelimit(key="ip", rate="5/10m", method="GET", block=True)
@ratelimit(key="ip", rate="5/10m", method="POST", block=True)
def password_set_view(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    user = _user_from_uid(uidb64)
    if user is None or not default_token_generator.check_token(user, token):
        messages.error(request, PASSWORD_LINK_BROKEN)
        return redirect("poligon:password")

    if request.method == "POST":
        form = StrongSetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            messages.success(request, PASSWORD_CHANGED)
            return redirect("poligon:login")
        for errors in form.errors.values():
            for error in errors:
                messages.error(request, error)
        return render(request, "poligon/auth_password_set.html", {"form": form})
    return render(request, "poligon/auth_password_set.html", {"form": StrongSetPasswordForm(user)})


def _user_from_uid(uidb64: str) -> User | None:
    try:
        return User.objects.get(pk=force_str(urlsafe_base64_decode(uidb64)))
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None


def _send_activation_email(user: User, request: HttpRequest) -> None:
    if not user.email:
        logger.warning("Skipping Poligon activation mail: no address for user_id=%s", user.pk)
        return
    link = request.build_absolute_uri(
        reverse(
            "poligon:activate",
            args=[urlsafe_base64_encode(force_bytes(user.pk)), account_activation_token.make_token(user)],
        )
    )
    safe_link = escape(link)
    html = f"""
    <p><strong>Cześć, {escape(user.username)}!</strong></p>
    <p>Potwierdź konto w Ćwiczbie, a Twój poziom i fiszki przestaną zależeć od jednej przeglądarki.</p>
    <p><a href="{safe_link}">Potwierdzam konto</a></p>
    <p>Jeśli link nie działa, wklej go do przeglądarki:<br>{safe_link}</p>
    <p>Do zobaczenia na treningu<br><strong>Ćwiczba</strong></p>
    """
    _send(user, "Potwierdź konto w Ćwiczbie", html)


def _send_password_email(user: User, request: HttpRequest) -> None:
    link = request.build_absolute_uri(
        reverse(
            "poligon:password_set",
            args=[urlsafe_base64_encode(force_bytes(user.pk)), default_token_generator.make_token(user)],
        )
    )
    safe_link = escape(link)
    html = f"""
    <p><strong>Cześć, {escape(user.username)}!</strong></p>
    <p>Ktoś poprosił o nowe hasło do konta w Ćwiczbie. Jeśli to Ty, ustaw je tutaj:</p>
    <p><a href="{safe_link}">Ustawiam nowe hasło</a></p>
    <p>Jeśli to nie Ty, zignoruj tę wiadomość. Hasło zostaje bez zmian.</p>
    <p>Ćwiczba</p>
    """
    _send(user, "Nowe hasło do Ćwiczby", html)


def _send(user: User, subject: str, html: str) -> None:
    try:
        send_brevo_email(subject, html, [user.email])
    except Exception:
        logger.exception("Failed to send a Poligon account email to user_id=%s", user.pk)
