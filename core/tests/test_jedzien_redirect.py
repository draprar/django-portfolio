import pytest
from django.test import override_settings

REDIRECT_HOSTS = ["jedzien.pl", "www.jedzien.pl"]
HOST_SETTINGS = {
    "ALLOWED_HOSTS": [*REDIRECT_HOSTS, "walery.onrender.com", "walery.site", "testserver"],
    "JEDZIEN_REDIRECT_HOSTS": REDIRECT_HOSTS,
    "JEDZIEN_REDIRECT_URL": "/wybierz/",
}


@pytest.mark.parametrize("host", REDIRECT_HOSTS)
@override_settings(**HOST_SETTINGS)
def test_jedzien_root_stays_on_same_host_wybierz(client, host):
    response = client.get("/", HTTP_HOST=host)
    assert response.status_code == 301
    assert response["Location"] == "/wybierz/"


@pytest.mark.parametrize("host", REDIRECT_HOSTS)
@override_settings(**HOST_SETTINGS)
def test_jedzien_other_paths_are_not_bounced_off_host(client, host):
    response = client.get("/health/", HTTP_HOST=host)
    assert response.status_code == 200
    assert "Location" not in response


@pytest.mark.parametrize("host", ["walery.onrender.com", "walery.site"])
@override_settings(**HOST_SETTINGS)
def test_walery_hosts_are_not_redirected(client, host):
    response = client.get("/health/", HTTP_HOST=host)
    assert response.status_code == 200
    assert "Location" not in response


@override_settings(**{**HOST_SETTINGS, "JEDZIEN_REDIRECT_URL": "https://walery.onrender.com/wybierz/"})
def test_legacy_absolute_redirect_url_is_treated_as_path(client):
    response = client.get("/", HTTP_HOST="jedzien.pl")
    assert response.status_code == 301
    assert response["Location"] == "/wybierz/"
