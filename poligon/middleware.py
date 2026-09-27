from django.conf import settings

from .identity import GUEST_COOKIE, GUEST_COOKIE_MAX_AGE


class GuestLearnerCookieMiddleware:
    """Writes the anonymous Poligon learner cookie the views asked for."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if getattr(request, "poligon_drop_guest_cookie", False):
            response.delete_cookie(GUEST_COOKIE)
        elif getattr(request, "poligon_guest_token", None):
            response.set_cookie(
                GUEST_COOKIE,
                str(request.poligon_guest_token),
                max_age=GUEST_COOKIE_MAX_AGE,
                httponly=True,
                samesite="Lax",
                secure=getattr(settings, "SESSION_COOKIE_SECURE", False),
            )
        return response
