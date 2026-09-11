from io import BytesIO
from unittest.mock import Mock

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import DatabaseError
from django.urls import reverse
from PIL import Image

from core.models import Project


def _tiny_png() -> SimpleUploadedFile:
    buf = BytesIO()
    Image.new("RGB", (8, 8), (20, 20, 20)).save(buf, format="PNG")
    return SimpleUploadedFile("shot.png", buf.getvalue(), content_type="image/png")


@pytest.mark.django_db
def test_code_page_renders_intro_and_project(client):
    Project.objects.create(
        title_en="Sample Repo",
        title_pl="Przykladowe repo",
        desc_en="Long CV description from the recruiter landing.",
        desc_pl="Dlugi opis CV z landinga rekrutera.",
        desc_code_en="Short kodzillin blurb for the IG page (EN).",
        desc_code_pl="Krotki opis kodzillin dla strony IG (PL).",
        github_url="https://github.com/example/sample-repo",
        live_url="https://example.com",
    )

    response = client.get(reverse("code:index"))
    content = response.content.decode()

    assert response.status_code == 200
    assert "kodzillin'" in content
    assert "Na co dzień jestem inżynierem danych" in content
    assert 'data-pl="Co tam?"' in content
    assert 'data-pl="Reposy"' in content
    assert 'data-pl="skrobnij"' in content
    assert 'data-pl="Stronki, aplikacje, narzędzia, SEO i se wyślesz linkiem."' in content
    assert 'data-pl="Kod"' in content
    assert 'href="#contact"' in content
    assert 'id="contact"' in content
    assert 'id="contact-form"' in content
    assert reverse("contact") in content
    assert "Sample Repo" in content
    assert "Przykladowe repo" in content
    assert "Short kodzillin blurb for the IG page (EN)." in content
    assert "Krotki opis kodzillin dla strony IG (PL)." in content
    assert "Long CV description from the recruiter landing." not in content
    assert 'class="intro-link"' in content
    assert "https://github.com/example/sample-repo" in content
    assert "https://example.com" in content
    assert 'class="lang-btn"' in content
    assert "core/js/lang.js" in content
    assert "code/js/contact.js" in content


@pytest.mark.django_db
def test_code_page_renders_project_thumb(client, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    Project.objects.create(
        title_en="Shot",
        title_pl="Zrzut",
        desc_en="Quick screenshot.",
        image=_tiny_png(),
    )

    response = client.get(reverse("code:index"))
    content = response.content.decode()

    assert response.status_code == 200
    assert "repo-thumb" in content
    assert "shot.png" in content


@pytest.mark.django_db
def test_code_page_falls_back_to_cv_desc(client):
    """When desc_code_* is empty, /code/ should show desc_* (CV description)."""
    Project.objects.create(
        title_en="CV only",
        title_pl="Tylko CV",
        desc_en="Only on the recruiter landing.",
        desc_pl="Tylko na landingu rekrutera.",
        desc_code_en="",
        desc_code_pl="",
    )

    response = client.get(reverse("code:index"))
    content = response.content.decode()

    assert response.status_code == 200
    assert "CV only" in content
    assert "Only on the recruiter landing." in content
    assert "Nothing listed yet." not in content


@pytest.mark.django_db
def test_code_page_empty_projects(client):
    response = client.get(reverse("code:index"))
    content = response.content.decode()

    assert response.status_code == 200
    assert "Nothing listed yet." in content


def test_code_view_handles_database_error(monkeypatch):
    import code.views as views_mod

    def raise_db_error(*args, **kwargs):
        raise DatabaseError("db down")

    monkeypatch.setattr(
        "code.views.Project",
        Mock(objects=Mock(all=raise_db_error)),
    )

    def fake_render(request, template_name, context):
        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.context_data = context
        fake_response.template_name = template_name
        return fake_response

    monkeypatch.setattr("code.views.render", fake_render)

    resp = views_mod.CodeView().get(Mock())
    assert resp.status_code == 200
    assert resp.context_data["projects"] == []
    assert resp.template_name == "code/index.html"
    assert "form" in resp.context_data
