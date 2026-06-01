import logging

import pytest
from django.urls import reverse

from config.urls import handler404
from config.views import custom_404_view


@pytest.mark.django_db
def test_custom_404_view_returns_404_and_logs_request(rf, caplog):
    request = rf.get("/missing-page/")
    request.META["REMOTE_ADDR"] = "203.0.113.42"

    with caplog.at_level(logging.WARNING):
        response = custom_404_view(request, Exception("missing"))

    assert response.status_code == 404
    assert any("path=/missing-page/" in rec.message for rec in caplog.records)
    assert any("ip=203.0.113.42" in rec.message for rec in caplog.records)


def test_handler404_points_to_project_custom_view():
    assert handler404 == "config.views.custom_404_view"


@pytest.mark.django_db
def test_api_docs_and_redoc_endpoints_render(client):
    docs = client.get(reverse("swagger-ui"))
    redoc = client.get(reverse("redoc"))

    assert docs.status_code == 200
    assert redoc.status_code == 200


