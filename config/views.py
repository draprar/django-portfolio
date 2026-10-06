import logging

from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render

logger = logging.getLogger(__name__)


def legacy_wiciedze_redirect(request, path=""):
    target = f"/wiciedze/{path}" if path else "/wiciedze/"
    qs = request.META.get("QUERY_STRING")
    if qs:
        target = f"{target}?{qs}"
    return HttpResponsePermanentRedirect(target)


def custom_404_view(request, exception):
    logger.warning("404 Not Found: path=%s ip=%s", request.path, request.META.get("REMOTE_ADDR"))
    if request.path.startswith("/wiciedze/"):
        return render(request, "wiciedzy/404.html", status=404)
    return render(request, "404.html", status=404)
