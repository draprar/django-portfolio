import logging

from django.db import DatabaseError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from core.models import Project

logger = logging.getLogger(__name__)


class CodeView(View):
    """
    Instagram-facing kodzillin' page at /code/.

    Shows all Project rows, prefers short `desc_code_*` blurbs;
    falls back to CV descriptions (`desc_*`) if code blurbs are empty.
    """

    template_name = "code/index.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            projects = list(Project.objects.all())
        except DatabaseError:
            logger.exception("Failed to load projects for code page")
            projects = []
        return render(
            request,
            self.template_name,
            {"projects": projects},
        )
