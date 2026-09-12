from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class JedzienRedirectMiddleware:
    """Send jedzien.pl traffic to /wybierz/ on the Render host.

    Apex and www always land on the same target, matching the old registrar
    URL redirect. Other hosts (walery.onrender.com, walery.site) are untouched.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        hosts = {host.lower() for host in getattr(settings, "JEDZIEN_REDIRECT_HOSTS", ())}
        if hosts:
            host = request.get_host().split(":")[0].lower()
            if host in hosts:
                return HttpResponsePermanentRedirect(settings.JEDZIEN_REDIRECT_URL)
        return self.get_response(request)
