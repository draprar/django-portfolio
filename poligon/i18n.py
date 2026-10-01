"""Interface language for Ćwiczba.

Polish is the default. English is the other interface language. Exercise text
stays on the record; this module only chooses the language of the chrome,
titles, errors and account mail.
"""

from __future__ import annotations

from django.http import HttpRequest
from django.utils import translation

LANG_KEY = "poligon_lang"
SUPPORTED = ("pl", "en")


def poligon_language(request: HttpRequest) -> str:
    raw = request.session.get(LANG_KEY, "pl")
    return raw if raw in SUPPORTED else "pl"


class PoligonLanguageMiddleware:
    """Activate PL/EN for /cwiczba/ only, so the rest of the portfolio is untouched."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        active = request.path.startswith("/cwiczba/")
        if active:
            lang = poligon_language(request)
            translation.activate(lang)
            request.LANGUAGE_CODE = lang
        response = self.get_response(request)
        if active:
            translation.deactivate()
        return response
