import pytest
from django.test import override_settings

JEDZIEN_HOSTS = ["jedzien.pl", "www.jedzien.pl"]
HOST_SETTINGS = {
    "ALLOWED_HOSTS": [*JEDZIEN_HOSTS, "walery.onrender.com", "walery.site", "testserver"],
    "JEDZIEN_REDIRECT_HOSTS": JEDZIEN_HOSTS,
}


@pytest.mark.django_db
@pytest.mark.parametrize("host", JEDZIEN_HOSTS)
@override_settings(**HOST_SETTINGS)
def test_jedzien_root_serves_hub_without_redirect(client, host):
    response = client.get("/", HTTP_HOST=host)
    assert response.status_code == 200
    assert "Location" not in response
    content = response.content.decode()
    assert "Se wybierz" in content
    assert "/gallery/" in content
    assert "/code/" in content
    assert "walery.site" not in content
    assert "walery.onrender.com" not in content


@pytest.mark.parametrize("host", JEDZIEN_HOSTS)
@override_settings(**HOST_SETTINGS)
def test_jedzien_other_paths_stay_on_host(client, host):
    response = client.get("/health/", HTTP_HOST=host)
    assert response.status_code == 200
    assert "Location" not in response


@pytest.mark.django_db
@pytest.mark.parametrize("host", ["walery.onrender.com", "walery.site"])
@override_settings(**HOST_SETTINGS)
def test_walery_root_is_portfolio_not_jedzien_hub(client, host):
    response = client.get("/", HTTP_HOST=host)
    assert response.status_code == 200
    assert "Location" not in response
    assert "Se wybierz" not in response.content.decode()
