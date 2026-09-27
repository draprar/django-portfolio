"""Who is practising right now.

Practice is open to anyone: a visitor gets a long-lived ``poligon_lid`` cookie
pointing at their own :class:`~poligon.models.LearnerState`. Signing in is only
about keeping that work when the cookie goes away.
"""

from __future__ import annotations

import uuid

from django.http import HttpRequest

from .models import LearnerState, Review, StudyEvent, Submission

GUEST_COOKIE = "poligon_lid"
GUEST_COOKIE_MAX_AGE = 60 * 60 * 24 * 90


def _cookie_token(request: HttpRequest) -> uuid.UUID | None:
    try:
        return uuid.UUID(request.COOKIES.get(GUEST_COOKIE, ""))
    except ValueError:
        return None


def guest_state(request: HttpRequest) -> LearnerState | None:
    token = _cookie_token(request)
    if token is None:
        return None
    return LearnerState.objects.filter(guest_token=token, user__isnull=True).first()


def learner_state(request: HttpRequest) -> LearnerState:
    """The state to write to. Creates one on first practice."""
    if request.user.is_authenticated:
        state, _created = LearnerState.objects.get_or_create(user=request.user)
        return state
    state = guest_state(request) or LearnerState.objects.create()
    # Refresh the cookie on every visit so an active guest never expires.
    request.poligon_guest_token = state.guest_token
    return state


def current_state(request: HttpRequest) -> LearnerState | None:
    """The state to read from. Never creates anything."""
    if request.user.is_authenticated:
        return LearnerState.objects.filter(user=request.user).first()
    return guest_state(request)


def adopt_guest_progress(request: HttpRequest, account: LearnerState) -> bool:
    """Move whatever the guest did onto the account they just signed in to."""
    state = guest_state(request)
    if state is None or state.pk == account.pk:
        return False

    # Checked before the move, so a brand-new account row is not mistaken for history.
    account_has_history = (
        Submission.objects.filter(learner=account).exists() or Review.objects.filter(learner=account).exists()
    )
    Submission.objects.filter(learner=state).update(learner=account)
    StudyEvent.objects.filter(learner=state).update(learner=account)
    # The account keeps its own card when both sides reviewed the same word.
    known = Review.objects.filter(learner=account).values_list("item_id", flat=True)
    Review.objects.filter(learner=state).exclude(item_id__in=known).update(learner=account)
    Review.objects.filter(learner=state).delete()

    _merge_plan(state, account, account_has_history)
    state.delete()
    request.poligon_drop_guest_cookie = True
    return True


def _merge_plan(guest: LearnerState, account: LearnerState, account_has_history: bool) -> None:
    """A fresh account takes the guest's plan. An account with history keeps the harder level."""
    fields = ["practice_level", "target_profile", "daily_minutes", "target_date", "updated_at"]
    if not account_has_history:
        account.practice_level = guest.practice_level
        account.daily_minutes = guest.daily_minutes
        account.target_date = guest.target_date
    else:
        account.practice_level = max(guest.practice_level, account.practice_level)
        if guest.updated_at > account.updated_at:
            account.daily_minutes = guest.daily_minutes
            account.target_date = guest.target_date
    account.target_profile = str(account.practice_level) * 4
    account.save(update_fields=fields)
