import logging

from django.db import DatabaseError

from .identity import account_state
from .services import due_review_count

logger = logging.getLogger(__name__)


def nav(request):
    """Flashcard badge for the Ćwiczba header. Only an account has cards."""
    match = getattr(request, "resolver_match", None)
    if match is None or match.app_name != "poligon":
        return {}
    try:
        state = account_state(request)
        due = due_review_count(state) if state else 0
    except DatabaseError:
        logger.exception("Failed to count due Ćwiczba reviews")
        return {"poligon_due_reviews": 0}
    return {"poligon_due_reviews": due}
