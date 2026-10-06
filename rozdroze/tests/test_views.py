import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_wybierz_renders_crossroads(client):
    response = client.get(reverse("rozdroze:wybierz"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "Se klikaj" in content
    assert "Se wybierz" not in content
    assert "/gallery/" in content
    assert "/wyraj/" in content
    assert "/tonguetwister/" in content
    assert "/code/" in content
    assert "/wiciedze/" in content
    assert "kodzillin'" in content
    assert ">wiciędze</h2>" in content
    assert "code-terminal" in content
    assert "wiciedzy-bg.jpg" in content
    assert 'panel-code' in content
    assert 'panel-wiciedzy' in content
    assert 'portal-featured' in content
    assert 'code-hero' in content
    assert 'stage-stack' in content
    assert 'panel-wide' in content
    assert "Wejdź" not in content
    assert 'class="cta-arrow"' not in content
    assert 'panel-cta' not in content
    assert "Komputerek" not in content
    assert 'id="contact-form"' not in content
    assert "rozdroze/js/wybierz.js" in content
    assert "{% static" not in content
    assert "no-cache" in response["Cache-Control"]


@pytest.mark.django_db
def test_wybierz_is_polish_only(client):
    """The hub ships without the language switcher, so nothing can flip it to EN."""
    response = client.get(reverse("rozdroze:wybierz"))
    content = response.content.decode()

    assert 'class="lang-btn"' not in content
    assert "lang-switcher" not in content
    assert "core/js/lang.js" not in content
    assert "data-en=" not in content
