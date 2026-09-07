import random

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse

LOGIN_FAILURE_MESSAGE = "Nie udało się zalogować. Sprawdź dane i spróbuj ponownie."
REGISTER_FAILURE_MESSAGE = "Nie udało się utworzyć konta. Sprawdź dane i spróbuj ponownie."


def is_email_confirmed(user) -> bool:
    """Return True only when the user has a profile with a confirmed email."""
    profile = getattr(user, "profile", None)
    return bool(profile and profile.email_confirmed)


def find_unique_user_by_email(email: str) -> User | None:
    """
    Look up a user by email without raising on duplicates.

    Non-empty emails are unique at the database (case-insensitive). This helper
    still treats zero or many matches as "not found" so reset can keep a
    uniform response if a race or empty email slips through.
    """
    matches = list(User.objects.filter(email__iexact=email)[:2])
    if len(matches) != 1:
        return None
    return matches[0]


def pick_random_row(queryset):
    """Return one row via OFFSET/LIMIT instead of ``ORDER BY RANDOM()``."""
    total = queryset.count()
    if total == 0:
        return None
    return queryset[random.randint(0, total - 1)]


def add_user_collection_item(*, model, user, related, related_field, duplicate_status, added_status, id_key):
    lookup = {"user": user, related_field: related}
    if model.objects.filter(**lookup).exists():
        return JsonResponse({"status": duplicate_status})
    try:
        obj = model.objects.create(**lookup)
    except IntegrityError:
        return JsonResponse({"status": duplicate_status})
    return JsonResponse({"status": added_status, id_key: obj.id})
