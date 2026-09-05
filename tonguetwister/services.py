from django.contrib.auth.models import User


def is_email_confirmed(user) -> bool:
    """Return True only when the user has a profile with a confirmed email."""
    profile = getattr(user, "profile", None)
    return bool(profile and profile.email_confirmed)


def find_unique_user_by_email(email: str) -> User | None:
    """
    Look up a user by email without raising on duplicates.

    auth.User.email is not unique. Reset mail is sent only when exactly one
    account matches (case-insensitive). Zero or many matches are treated as
    "not found" so the view can keep a uniform response.
    """
    matches = list(User.objects.filter(email__iexact=email)[:2])
    if len(matches) != 1:
        return None
    return matches[0]
