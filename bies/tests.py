from django.test import TestCase
from django.urls import resolve, reverse

from bies.views import index


class BiesViewTests(TestCase):
    def test_index_view_returns_200(self):
        response = self.client.get(reverse("bies_index"))
        self.assertEqual(response.status_code, 200)

    def test_index_url_resolves_to_index_view(self):
        match = resolve(reverse("bies_index"))
        self.assertEqual(match.func, index)
