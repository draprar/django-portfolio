from django.test import TestCase
from django.urls import resolve, reverse

from bies.models import Swieto, ZrodloBibliograficzne
from bies.views import wyraj_detail, wyraj_lista


# Helpers
def make_swieto(**kwargs):
    """Tworzy minimalne święto do testów."""
    defaults = {
        "slug": "test-swieto",
        "tytul_pl": "Testowe Święto",
        "tytul_en": "Test Feast",
        "kolejnosc": 1,
    }
    defaults.update(kwargs)
    return Swieto.objects.create(**defaults)

# Model: Swieto
class SwietoModelTests(TestCase):

    def test_str_returns_tytul_pl(self):
        s = make_swieto()
        self.assertEqual(str(s), "Testowe Święto")

    def test_slug_autofill_from_tytul_pl(self):
        """Slug generuje się automatycznie, jeśli nie podano."""
        s = Swieto.objects.create(tytul_pl="Jare Gody", tytul_en="Jare Gody")
        self.assertEqual(s.slug, "jare-gody")

    def test_slug_not_overwritten_if_provided(self):
        s = make_swieto(slug="moj-slug", tytul_pl="Coś")
        self.assertEqual(s.slug, "moj-slug")

    def test_get_tytul_pl(self):
        s = make_swieto()
        self.assertEqual(s.get_tytul("pl"), "Testowe Święto")

    def test_get_tytul_en(self):
        s = make_swieto()
        self.assertEqual(s.get_tytul("en"), "Test Feast")

    def test_get_podtytul_pl(self):
        s = make_swieto(podtytul_pl="wiosną", podtytul_en="in spring")
        self.assertEqual(s.get_podtytul("pl"), "wiosną")

    def test_get_podtytul_en(self):
        s = make_swieto(podtytul_pl="wiosną", podtytul_en="in spring")
        self.assertEqual(s.get_podtytul("en"), "in spring")

    def test_default_ordering_by_kolejnosc(self):
        make_swieto(slug="b", tytul_pl="B", kolejnosc=2)
        make_swieto(slug="a", tytul_pl="A", kolejnosc=1)
        slugs = list(Swieto.objects.values_list("slug", flat=True))
        self.assertEqual(slugs, ["a", "b"])

    def test_utworzone_auto_set(self):
        s = make_swieto()
        self.assertIsNotNone(s.utworzone)

    def test_zaktualizowane_auto_set(self):
        s = make_swieto()
        self.assertIsNotNone(s.zaktualizowane)


# ---------------------------------------------------------------------------
# Model: ZrodloBibliograficzne
# ---------------------------------------------------------------------------

class ZrodloModelTests(TestCase):

    def setUp(self):
        self.swieto = make_swieto()

    def test_str_with_autor(self):
        z = ZrodloBibliograficzne.objects.create(
            swieto=self.swieto,
            autor="Oskar Kolberg",
            tytul="Pieśni ludu",
        )
        self.assertIn("Oskar Kolberg", str(z))
        self.assertIn("Pieśni ludu", str(z))

    def test_str_without_autor(self):
        z = ZrodloBibliograficzne.objects.create(
            swieto=self.swieto,
            tytul="Wikipedia — Gaik",
        )
        self.assertEqual(str(z), "Wikipedia — Gaik")

    def test_related_name_zrodla(self):
        ZrodloBibliograficzne.objects.create(
            swieto=self.swieto, tytul="Źródło A", kolejnosc=1
        )
        ZrodloBibliograficzne.objects.create(
            swieto=self.swieto, tytul="Źródło B", kolejnosc=2
        )
        self.assertEqual(self.swieto.zrodla.count(), 2)

    def test_ordering_by_kolejnosc(self):
        ZrodloBibliograficzne.objects.create(
            swieto=self.swieto, tytul="B", kolejnosc=2
        )
        ZrodloBibliograficzne.objects.create(
            swieto=self.swieto, tytul="A", kolejnosc=1
        )
        tytuly = list(
            self.swieto.zrodla.values_list("tytul", flat=True)
        )
        self.assertEqual(tytuly, ["A", "B"])

    def test_cascade_delete(self):
        ZrodloBibliograficzne.objects.create(
            swieto=self.swieto, tytul="Coś"
        )
        self.swieto.delete()
        self.assertEqual(ZrodloBibliograficzne.objects.count(), 0)


# ---------------------------------------------------------------------------
# Widok: wyraj_lista
# ---------------------------------------------------------------------------

class WyrajListaViewTests(TestCase):

    def test_returns_200(self):
        response = self.client.get(reverse("bies:wyraj-lista"))
        self.assertEqual(response.status_code, 200)

    def test_url_resolves_to_correct_view(self):
        match = resolve("/wyraj/")
        self.assertEqual(match.func, wyraj_lista)

    def test_template_used(self):
        response = self.client.get(reverse("bies:wyraj-lista"))
        self.assertTemplateUsed(response, "bies/wyraj/lista.html")

    def test_context_contains_swieta(self):
        make_swieto()
        response = self.client.get(reverse("bies:wyraj-lista"))
        self.assertIn("swieta", response.context)

    def test_empty_lista_returns_200(self):
        """Lista działa też gdy baza jest pusta."""
        response = self.client.get(reverse("bies:wyraj-lista"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["swieta"]), [])

    def test_lista_shows_all_swieta(self):
        make_swieto(slug="a", tytul_pl="A")
        make_swieto(slug="b", tytul_pl="B")
        response = self.client.get(reverse("bies:wyraj-lista"))
        self.assertEqual(response.context["swieta"].count(), 2)


# ---------------------------------------------------------------------------
# Widok: wyraj_detail
# ---------------------------------------------------------------------------

class WyrajDetailViewTests(TestCase):

    def setUp(self):
        self.swieto = make_swieto(
            slug="gaik",
            o_swiecie_pl="Treść PL",
            o_swiecie_en="Content EN",
        )

    def test_returns_200_for_existing_slug(self):
        response = self.client.get(reverse("bies:wyraj-detail", args=["gaik"]))
        self.assertEqual(response.status_code, 200)

    def test_returns_404_for_nonexistent_slug(self):
        response = self.client.get(reverse("bies:wyraj-detail", args=["nie-istnieje"]))
        self.assertEqual(response.status_code, 404)

    def test_url_resolves_to_correct_view(self):
        match = resolve("/wyraj/gaik/")
        self.assertEqual(match.func, wyraj_detail)

    def test_template_used(self):
        response = self.client.get(reverse("bies:wyraj-detail", args=["gaik"]))
        self.assertTemplateUsed(response, "bies/wyraj/detail.html")

    def test_context_contains_swieto(self):
        response = self.client.get(reverse("bies:wyraj-detail", args=["gaik"]))
        self.assertIn("swieto", response.context)
        self.assertEqual(response.context["swieto"], self.swieto)

    def test_tytul_pl_in_response(self):
        response = self.client.get(reverse("bies:wyraj-detail", args=["gaik"]))
        self.assertContains(response, "Testowe Święto")

    def test_zrodla_in_context(self):
        ZrodloBibliograficzne.objects.create(
            swieto=self.swieto, tytul="Oskar Kolberg", kolejnosc=1
        )
        response = self.client.get(reverse("bies:wyraj-detail", args=["gaik"]))
        self.assertContains(response, "Oskar Kolberg")


# ---------------------------------------------------------------------------
# URL patterns
# ---------------------------------------------------------------------------

class UrlTests(TestCase):

    def test_lista_url(self):
        url = reverse("bies:wyraj-lista")
        self.assertEqual(url, "/wyraj/")

    def test_detail_url_with_slug(self):
        url = reverse("bies:wyraj-detail", args=["szczodre-gody"])
        self.assertEqual(url, "/wyraj/szczodre-gody/")

    def test_detail_url_with_dashes(self):
        url = reverse("bies:wyraj-detail", args=["smigus-dyngus"])
        self.assertEqual(url, "/wyraj/smigus-dyngus/")
