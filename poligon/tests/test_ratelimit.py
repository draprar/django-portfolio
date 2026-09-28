import pytest
from django.core.cache import cache
from django.test import override_settings
from django.urls import reverse


@pytest.mark.django_db
@override_settings(RATELIMIT_ENABLE=True)
def test_settings_post_is_rate_limited(member_client):
    cache.clear()
    url = reverse("poligon:settings")
    posted = {"practice_level": "2", "daily_minutes": "40", "target_date": ""}
    remote = {"REMOTE_ADDR": "203.0.113.20"}

    for _ in range(5):
        response = member_client.post(url, posted, **remote)
        assert response.status_code == 302

    blocked = member_client.post(url, posted, **remote)
    assert blocked.status_code == 403
