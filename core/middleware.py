from urllib.parse import urlparse

from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class JedzienRedirectMiddleware:
    """Keep jedzien.pl in the address bar, like walery.site.

    Only the site root jumps to /wybierz/ on the same host. Other paths
    (gallery, code, health) stay on jedzien.pl. walery hosts are untouched.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        hosts = {host.lower() for host in getattr(settings, "JEDZIEN_REDIRECT_HOSTS", ())}
        if not hosts:
            return self.get_response(request)

        host = request.get_host().split(":")[0].lower()
        if host not in hosts:
            return self.get_response(request)

        if request.path not in {"/", ""}:
            return self.get_response(request)

        return HttpResponsePermanentRedirect(_landing_path())


def _landing_path() -> str:
    target = getattr(settings, "JEDZIEN_REDIRECT_URL", "/wybierz/")
    if "://" in target:
        target = urlparse(target).path or "/wybierz/"
    if not target.startswith("/"):
        target = f"/{target}"
    if not target.endswith("/"):
        target = f"{target}/"
    return target
