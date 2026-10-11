import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestRugbyHomeView:
    def setup_method(self):
        self.url = reverse("post_list")

    def test_home_returns_200(self, client):
        response = client.get(self.url)
        assert response.status_code == 200

    def test_no_accordion_or_posts_context(self, client):
        response = client.get(self.url)
        content = response.content.decode()
        assert "posts" not in response.context
        assert "accordion" not in content.lower()
        assert "Rugby 7 czy XV?" in content
        assert "18.09.2010" in content

    def test_meta_title(self, client):
        response = client.get(self.url)
        content = response.content.decode()
        assert "<title>rugby — 7 i XV</title>" in content
        assert "aktualny obraz" not in content.lower()
