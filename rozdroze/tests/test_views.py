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
    assert 'data-default-lang="pl"' in content
    assert 'class="lang-btn"' in content
    assert 'class="enter-hint"' in content
    assert "Komputerek" in content
