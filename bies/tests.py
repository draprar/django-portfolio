from django.test import TestCase
from django.urls import resolve, reverse

from bies.views import wyraj_lista


class WyrajViewTests(TestCase):
    def test_lista_returns_200(self):
        response = self.client.get(reverse("bies:wyraj-lista"))
        self.assertEqual(response.status_code, 200)

    def test_lista_url_resolves(self):
        match = resolve("/wyraj/")
        self.assertEqual(match.func, wyraj_lista)

    def test_swietowit_letni_returns_200(self):
        response = self.client.get(reverse("bies:wyraj-swietowit-letni"))
        self.assertEqual(response.status_code, 200)
