"""Optional accounts for Ćwiczba.

Practice never needs one. Without an account nothing is stored at all, so the
work ends with the visit. An account is what keeps the level, the history and
the flashcard schedule. It is the project-wide ``django.contrib.auth`` user, so
one account works across the whole portfolio, but every page here is Ćwiczba's.
"""

from __future__ import annotations

import json
import logging

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
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
from django.utils.translation import gettext as _
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

from .events import record_event
from .identity import account_state, adopt_guest_level
from .levels import level_names
from .models import PlacementAttempt, ProductEvent, Review, Submission
from .services import due_review_count

logger = logging.getLogger(__name__)

SIGNED_UP = "Konto jest prawie gotowe. Sprawdź skrzynkę i kliknij link, żeby je potwierdzić."
ACTIVATED = "Konto potwierdzone. Możesz się zalogować."
ACTIVATION_BROKEN = "Ten link już nie działa. Zarejestruj się jeszcze raz albo napisz do nas."
LEVEL_MOVED = "Na koncie ustawiliśmy poziom wybrany przed chwilą."
PASSWORD_SENT = "Jeśli konto istnieje, wyślemy link do zmiany hasła."
PASSWORD_CHANGED = "Hasło zmienione. Zaloguj się nowym hasłem."
PASSWORD_LINK_BROKEN = "Ten link do zmiany hasła już nie działa. Poproś o nowy."


def account(request: HttpRequest) -> HttpResponse:
    state = account_state(request)
    names = level_names(state.practice_level) if state is not None else ("", "")
    return render(
        request,
        "poligon/account.html",
        {
            "state": state,
            "done": Submission.objects.filter(learner=state).count() if state else 0,
            "due_reviews": due_review_count(state) if state else 0,
            "level_en": names[0],
            "level_pl": names[1],
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
                messages.error(request, _(LOGIN_FAILURE_MESSAGE))
                return render(request, "poligon/auth_login.html", {"form": form})
            login(request, user)
            state = account_state(request)
            if state is not None and adopt_guest_level(request, state):
                messages.success(request, _(LEVEL_MOVED))
            return redirect("poligon:dashboard")
        if form.non_field_errors():
            messages.error(request, _(LOGIN_FAILURE_MESSAGE))
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
            record_event(request, "account_created", {"user_id": user.pk})
            _send_activation_email(user, request)
            messages.success(request, _(SIGNED_UP))
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
            messages.error(request, _(ACTIVATION_BROKEN))
            return redirect("poligon:register")
        profile.email_confirmed = True
        profile.save(update_fields=["email_confirmed"])
        messages.success(request, _(ACTIVATED))
        return redirect("poligon:login")
    messages.error(request, _(ACTIVATION_BROKEN))
    return redirect("poligon:register")


@csrf_protect
@ratelimit(key="ip", rate="5/10m", method="POST", block=True)
def password_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user = find_unique_user_by_email((request.POST.get("email") or "").strip())
        if user is not None:
            _send_password_email(user, request)
        # Same answer either way, so the form never confirms who has an account.
        messages.success(request, _(PASSWORD_SENT))
        return redirect("poligon:login")
    return render(request, "poligon/auth_password.html")


@csrf_protect
@ratelimit(key="ip", rate="5/10m", method="GET", block=True)
@ratelimit(key="ip", rate="5/10m", method="POST", block=True)
def password_set_view(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    user = _user_from_uid(uidb64)
    if user is None or not default_token_generator.check_token(user, token):
        messages.error(request, _(PASSWORD_LINK_BROKEN))
        return redirect("poligon:password")

    if request.method == "POST":
        form = StrongSetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _(PASSWORD_CHANGED))
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
    intro = _("Potwierdź konto w Ćwiczbie, a Twój poziom i fiszki przestaną zależeć od jednej przeglądarki.")
    action = _("Potwierdzam konto")
    html = (
        f"<p><strong>{escape(user.username)}</strong></p>"
        f"<p>{intro}</p>"
        f'<p><a href="{safe_link}">{action}</a></p>'
        f"<p>{safe_link}</p>"
    )
    text = f"{user.username}\n{intro}\n{action}: {link}\n"
    _send(user, _("Potwierdź konto w Ćwiczbie"), html, text)


def _send_password_email(user: User, request: HttpRequest) -> None:
    link = request.build_absolute_uri(
        reverse(
            "poligon:password_set",
            args=[urlsafe_base64_encode(force_bytes(user.pk)), default_token_generator.make_token(user)],
        )
    )
    safe_link = escape(link)
    intro = _("Ktoś poprosił o nowe hasło do konta w Ćwiczbie. Jeśli to Ty, ustaw je tutaj:")
    action = _("Ustawiam nowe hasło")
    ignore = _("Jeśli to nie Ty, zignoruj tę wiadomość. Hasło zostaje bez zmian.")
    html = (
        f"<p><strong>{escape(user.username)}</strong></p>"
        f"<p>{intro}</p>"
        f'<p><a href="{safe_link}">{action}</a></p>'
        f"<p>{ignore}</p>"
        f"<p>{safe_link}</p>"
    )
    text = f"{user.username}\n{intro}\n{action}: {link}\n{ignore}\n"
    _send(user, _("Nowe hasło do Ćwiczby"), html, text)


@login_required(login_url="poligon:login")
def export_account(request: HttpRequest) -> HttpResponse:
    """A file the learner can keep. It does not include the password."""
    state = account_state(request)
    if state is None:
        return redirect("poligon:account")
    payload = {
        "username": request.user.username,
        "email": request.user.email,
        "practice_level": state.practice_level,
        "daily_minutes": state.daily_minutes,
        "target_date": state.target_date.isoformat() if state.target_date else None,
        "submissions": [
            {
                "slug": row.exercise.slug,
                "score": row.score,
                "answer_text": row.answer_text,
                "completed_at": row.completed_at.isoformat(),
                "feedback": row.feedback,
            }
            for row in Submission.objects.filter(learner=state).select_related("exercise")
        ],
        "reviews": [
            {
                "term": row.item.term,
                "due_at": row.due_at.isoformat(),
                "interval_days": row.interval_days,
                "last_grade": row.last_grade,
            }
            for row in Review.objects.filter(learner=state).select_related("item")
        ],
        "placement": [
            {
                "algorithm_version": row.algorithm_version,
                "correct_count": row.correct_count,
                "suggested_level": row.suggested_level,
                "created_at": row.created_at.isoformat(),
            }
            for row in PlacementAttempt.objects.filter(learner=state)
        ],
        "events": [
            {"name": row.name, "payload": row.payload, "created_at": row.created_at.isoformat()}
            for row in ProductEvent.objects.filter(learner=state)
        ],
    }
    body = json.dumps(payload, ensure_ascii=False, indent=2)
    response = HttpResponse(body, content_type="application/json")
    response["Content-Disposition"] = 'attachment; filename="cwiczba-export.json"'
    return response


@login_required(login_url="poligon:login")
@require_POST
def delete_account(request: HttpRequest) -> HttpResponse:
    """Remove the account and the training stored on it."""
    if request.POST.get("confirm") != "usuń":
        messages.error(request, _("Wpisz usuń, jeśli chcesz skasować konto i trening."))
        return redirect("poligon:account")
    user = request.user
    ProductEvent.objects.filter(payload__user_id=user.pk).delete()
    logout(request)
    user.delete()
    messages.success(request, _("Konto i trening zostały usunięte."))
    return redirect("poligon:start")


def _send(user: User, subject: str, html: str, text: str) -> None:
    try:
        send_brevo_email(subject, html, [user.email], text_content=text)
    except Exception:
        logger.exception("Failed to send a Poligon account email to user_id=%s", user.pk)
