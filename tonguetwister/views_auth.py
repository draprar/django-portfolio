import logging

import sentry_sdk
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.html import escape
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.csrf import csrf_protect
from django_ratelimit.decorators import ratelimit

from core.email import send_brevo_email

from .forms import ContactForm, CustomUserCreationForm
from .tokens import account_activation_token

logger = logging.getLogger(__name__)


@csrf_protect
@ratelimit(key="ip", rate="10/5m", method="POST", block=True)
def login_view(request):
    # Ratelimit counts all failed payloads, including invalid forms.
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            login(request, form.get_user())
            return redirect("main")
        messages.error(request, "Nie udało się zalogować. Sprawdź dane i spróbuj ponownie.")

    return render(request, "tonguetwister/registration/login.html", {"form": form})


def send_activation_email(user, request):
    try:
        subject = "Witamy na pokładzie!"

        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = request.build_absolute_uri(reverse("activate", args=[uid, token]))

        username = escape(user.username)
        safe_link = escape(activation_link)

        html_message = f"""
        <p><strong>Czołem, {username}!</strong></p>

        <p>
        Dziękujemy za rejestrację w LingwoŁamkach.
        Aby aktywować konto i potwierdzić adres e-mail, kliknij w poniższy link:
        </p>

        <p>
        <a href="{safe_link}">
        Aktywuj swoje konto
        </a>
        </p>

        <p>
        Jeżeli link nie działa, skopiuj go i wklej do przeglądarki:<br>
        {safe_link}
        </p>

        <p>
        <strong>Potrzebujesz pomocy?</strong><br>
        <a href="mailto:kontakt@walery.online">
        Z radością odpowiemy na Twoje pytania.
        </a>
        </p>

        <p>
        Pozdrawiamy<br>
        <strong>Zespół LingwoŁamki</strong>
        </p>
        """

        recipient_list = [user.email]
        if not user.email:
            logger.warning("Pomijam wysyłkę aktywacji: brak email dla user_id=%s", user.pk)
            return
        send_brevo_email(subject, html_message, recipient_list)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        logger.exception("Błąd przy wysyłaniu e-maila aktywacyjnego")


@ratelimit(key="ip", rate="5/10m", method="POST", block=True)
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            send_activation_email(user, request)
            messages.success(
                request,
                "Brawo! Możesz się zalogować. Sprawdź swoją skrzynkę e-mail, aby aktywować konto.",
            )
            return redirect("login")

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)
        return render(request, "tonguetwister/registration/register.html", {"form": form})

    form = CustomUserCreationForm()
    return render(request, "tonguetwister/registration/register.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        try:
            profile = user.profile
            profile.email_confirmed = True
            profile.save(update_fields=["email_confirmed"])
        except ObjectDoesNotExist:
            logger.warning("Aktywacja bez profilu dla user_id=%s", user.pk)
            messages.error(request, "Nie udało się aktywować konta. Skontaktuj się z administratorem.")
            return redirect("register")
        messages.success(request, "Dziękujemy za potwierdzenie :) Twoje konto zostało zweryfikowane.")
        return redirect("login")

    messages.error(request, "Link aktywacyjny jest nieprawidłowy!")
    return redirect("register")


@csrf_protect
@ratelimit(key="ip", rate="5/10m", method="POST", block=True)
def password_reset_view(request):
    if request.method == "POST":
        email = (request.POST.get("email") or "").strip()

        try:
            user = User.objects.get(email__iexact=email)

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_link = request.build_absolute_uri(reverse("password_reset_confirm", args=[uid, token]))

            html_message = f"""
            <p>Czołem <strong>{escape(user.username)}</strong>,</p>

            <p>
                Otrzymaliśmy prośbę o zresetowanie hasła do Twojego konta.
                Kliknij poniższy link, aby je zresetować:
            </p>

            <p>
                <a href="{escape(reset_link)}">{escape(reset_link)}</a>
            </p>

            <p>
                Jeśli to nie Ty prosiłeś o zresetowanie hasła,
                po prostu zignoruj tę wiadomość.
                Twoje hasło pozostanie bez zmian.
            </p>

            <p>
                Pozdrawiamy<br>
                <strong>Zespół LingwoŁamki</strong>
            </p>
            """

            subject = "Resetuj swoje hasło"
            recipient_list = [email]
            send_brevo_email(subject, html_message, recipient_list)

        except User.DoesNotExist:
            sentry_sdk.capture_message("Nieudana próba resetowania hasła dla nieistniejacego konta", level="warning")

        return redirect("password_reset_done")

    return render(request, "tonguetwister/registration/password_reset_form.html")


@csrf_protect
def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password1 = request.POST.get("new_password1") or ""
            new_password2 = request.POST.get("new_password2") or ""
            if not new_password1 or not new_password2:
                messages.error(request, "Wprowadź oba pola hasła.")
                return render(request, "tonguetwister/registration/password_reset_confirm.html")

            if new_password1 == new_password2:
                try:
                    validate_password(new_password1, user=user)
                except ValidationError as e:
                    for msg in e.messages:
                        messages.error(request, msg)
                    return render(request, "tonguetwister/registration/password_reset_confirm.html")

                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Twoje hasło zostało zmienione.")
                return redirect("password_reset_complete")

            messages.error(request, "Hasła nie są identyczne.")

        return render(request, "tonguetwister/registration/password_reset_confirm.html")

    messages.error(request, "Link resetowania hasła jest nieprawidłowy.")
    return redirect("password_reset")


@csrf_protect
def password_reset_complete_view(request):
    return render(request, "tonguetwister/registration/password_reset_complete.html")


@csrf_protect
def password_reset_done_view(request):
    return render(request, "tonguetwister/registration/password_reset_done.html")


@csrf_protect
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            subject = f"Kontakt od {name}"
            message_with_email = f"Od: {email}\n\n{message}"

            try:
                send_mail(
                    subject=subject,
                    message=message_with_email,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                messages.success(request, "Twoja wiadomość została Nam przekazana")
            except Exception:
                logger.exception("Blad przy wysylaniu formularza kontaktowego")
                messages.error(request, "Nie udalo sie wyslac wiadomosci. Sprobuj ponownie pozniej.")
            return redirect("tw_contact")
    else:
        form = ContactForm()

    return render(request, "tonguetwister/partials/static/contact.html", {"form": form})
