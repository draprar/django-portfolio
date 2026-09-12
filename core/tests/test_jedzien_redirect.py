import pytest
from django.test import override_settings

REDIRECT_HOSTS = ["jedzien.pl", "www.jedzien.pl"]
REDIRECT_URL = "https://walery.onrender.com/wybierz/"
HOST_SETTINGS = {
    "ALLOWED_HOSTS": [*REDIRECT_HOSTS, "walery.onrender.com", "walery.site", "testserver"],
    "JEDZIEN_REDIRECT_HOSTS": REDIRECT_HOSTS,
    "JEDZIEN_REDIRECT_URL": REDIRECT_URL,
}


@pytest.mark.parametrize("host", REDIRECT_HOSTS)
@pytest.mark.parametrize("path", ["/", "/cokolwiek/", "/wybierz/"])
@override_settings(**HOST_SETTINGS)
def test_jedzien_hosts_redirect_to_wybierz(client, host, path):
    response = client.get(path, HTTP_HOST=host)
    assert response.status_code == 301
    assert response["Location"] == REDIRECT_URL


@pytest.mark.parametrize("host", ["walery.onrender.com", "walery.site"])
@override_settings(**HOST_SETTINGS)
def test_walery_hosts_are_not_redirected(client, host):
    response = client.get("/health/", HTTP_HOST=host)
    assert response.status_code == 200
    assert "Location" not in response
