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
