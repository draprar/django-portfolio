import logging
from pathlib import Path

import pytest
from django.conf import settings
from django.urls import reverse

from config.urls import handler404
from config.views import custom_404_view


@pytest.mark.django_db
def test_custom_404_view_returns_404_and_logs_request(rf, caplog):
    # Simulate a request to a missing page.
    request = rf.get("/missing-page/")
    request.META["REMOTE_ADDR"] = "203.0.113.42"

    # Capture warning logs emitted by the custom handler.
    with caplog.at_level(logging.WARNING):
        response = custom_404_view(request, Exception("missing"))

    assert response.status_code == 404
    assert any("path=/missing-page/" in rec.message for rec in caplog.records)
    assert any("ip=203.0.113.42" in rec.message for rec in caplog.records)


def test_handler404_points_to_project_custom_view():
    # Ensure Django uses the project's custom 404 handler.
    assert handler404 == "config.views.custom_404_view"


@pytest.mark.django_db
def test_api_docs_and_redoc_endpoints_render(client):
    # Check that API documentation pages are available.
    docs = client.get(reverse("swagger-ui"))
    redoc = client.get(reverse("redoc"))

    assert docs.status_code == 200
    assert redoc.status_code == 200


def test_login_url_points_to_tonguetwister_not_admin():
    assert settings.LOGIN_URL == "login"
    assert reverse(settings.LOGIN_URL) == "/tonguetwister/login/"


def test_csp_media_src_uses_supabase_project_ref_when_set():
    if settings.SUPABASE_PROJECT_REF:
        assert f"https://{settings.SUPABASE_PROJECT_REF}.supabase.co" in settings.SECURE_CSP["media-src"]
    else:
        assert "supabase.co" not in settings.SECURE_CSP["media-src"]


@pytest.mark.django_db
def test_debug_serves_local_media(client):
    if not settings.DEBUG or not getattr(settings, "MEDIA_ROOT", None):
        pytest.skip("media serving is wired only when DEBUG and MEDIA_ROOT are set at import")
    media_root = Path(settings.MEDIA_ROOT)
    media_root.mkdir(parents=True, exist_ok=True)
    probe = media_root / "audit-probe.txt"
    probe.write_text("ok", encoding="utf-8")
    try:
        response = client.get(f"{settings.MEDIA_URL}audit-probe.txt")
        assert response.status_code == 200
        assert b"ok" in response.content
    finally:
        probe.unlink(missing_ok=True)
