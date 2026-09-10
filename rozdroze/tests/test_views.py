import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_wybierz_renders_crossroads(client):
    response = client.get(reverse("rozdroze:wybierz"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "Se wybierz" in content
    assert "/gallery/" in content
    assert "/wyraj/" in content
    assert "/tonguetwister/" in content
    assert "/code/" in content
    assert "kodzillin'" in content
    assert "code-bg.gif" in content
    assert 'panel-code' in content
    assert 'class="cta-arrow"' in content
    assert "Komputerek" in content


@pytest.mark.django_db
def test_wybierz_is_polish_only(client):
    """The hub ships without the language switcher, so nothing can flip it to EN."""
    response = client.get(reverse("rozdroze:wybierz"))
    content = response.content.decode()

    assert 'class="lang-btn"' not in content
    assert "lang-switcher" not in content
    assert "core/js/lang.js" not in content
    assert "data-en=" not in content
