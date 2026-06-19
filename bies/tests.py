from django.test import TestCase
from django.urls import resolve, reverse

from bies.models import Swieto, ZrodloBibliograficzne
from bies.views import wyraj_detail, wyraj_lista


def make_swieto(**kwargs):
    defaults = {
        "slug": "test-swieto",
        "tytul_pl": "Testowe Święto",
        "tytul_en": "Test Feast",
        "kolejnosc": 1,
    }
    defaults.update(kwargs)
    return Swieto.objects.create(**defaults)


# ── Model: Swieto ────────────────────────────────

class SwietoModelTests(TestCase):

    def test_str_returns_tytul_pl(self):
        self.assertEqual(str(make_swieto()), "Testowe Święto")

    def test_slug_autofill(self):
        s = Swieto.objects.create(tytul_pl="Jare Gody", tytul_en="Jare Gody")
        self.assertEqual(s.slug, "jare-gody")

    def test_slug_not_overwritten(self):
        s = make_swieto(slug="moj-slug", tytul_pl="Coś")
        self.assertEqual(s.slug, "moj-slug")

    def test_get_tytul_pl(self):
        self.assertEqual(make_swieto().get_tytul("pl"), "Testowe Święto")

    def test_get_tytul_en(self):
        self.assertEqual(make_swieto().get_tytul("en"), "Test Feast")

    def test_get_duchy_list_pl(self):
        s = make_swieto(duchy_pl="Jaryło, Marzanna, Wiosna")
        self.assertEqual(s.get_duchy_list("pl"), ["Jaryło", "Marzanna", "Wiosna"])

    def test_get_duchy_list_empty(self):
        self.assertEqual(make_swieto().get_duchy_list("pl"), [])

    def test_get_duchy_list_strips_spaces(self):
        s = make_swieto(duchy_pl=" Weles ,  Mokosz ")
        self.assertEqual(s.get_duchy_list("pl"), ["Weles", "Mokosz"])

    def test_default_ordering(self):
        make_swieto(slug="b", tytul_pl="B", kolejnosc=2)
        make_swieto(slug="a", tytul_pl="A", kolejnosc=1)
        self.assertEqual(
            list(Swieto.objects.values_list("slug", flat=True)),
            ["a", "b"],
        )

    def test_get_next(self):
        s1 = make_swieto(slug="s1", kolejnosc=1)
        s2 = make_swieto(slug="s2", kolejnosc=2)
        self.assertEqual(s1.get_next(), s2)

    def test_get_prev(self):
        s1 = make_swieto(slug="s1", kolejnosc=1)
        s2 = make_swieto(slug="s2", kolejnosc=2)
        self.assertEqual(s2.get_prev(), s1)

    def test_get_next_returns_none_for_last(self):
        s = make_swieto(kolejnosc=99)
        self.assertIsNone(s.get_next())

    def test_get_prev_returns_none_for_first(self):
        s = make_swieto(kolejnosc=1)
        self.assertIsNone(s.get_prev())

    def test_kolo_kat_default(self):
        self.assertEqual(make_swieto().kolo_kat, 0)

    def test_kolo_kolor_default(self):
        self.assertEqual(make_swieto().kolo_kolor, "#c4922a")


# ── Model: ZrodloBibliograficzne ─────────────────

class ZrodloModelTests(TestCase):

    def setUp(self):
        self.swieto = make_swieto()

    def test_str_with_autor(self):
        z = ZrodloBibliograficzne.objects.create(
            swieto=self.swieto, autor="Oskar Kolberg", tytul="Pieśni ludu"
        )
        self.assertIn("Oskar Kolberg", str(z))

    def test_str_without_autor(self):
        z = ZrodloBibliograficzne.objects.create(
            swieto=self.swieto, tytul="Wikipedia — Gaik"
        )
        self.assertEqual(str(z), "Wikipedia — Gaik")

    def test_cascade_delete(self):
        ZrodloBibliograficzne.objects.create(swieto=self.swieto, tytul="Coś")
        self.swieto.delete()
        self.assertEqual(ZrodloBibliograficzne.objects.count(), 0)


# ── Widok: wyraj_lista ───────────────────────────

class WyrajListaViewTests(TestCase):

    def test_returns_200(self):
        self.assertEqual(
            self.client.get(reverse("bies:wyraj-lista")).status_code, 200
        )

    def test_url_resolves(self):
        self.assertEqual(resolve("/wyraj/").func, wyraj_lista)

    def test_template_used(self):
        self.assertTemplateUsed(
            self.client.get(reverse("bies:wyraj-lista")),
            "bies/wyraj/lista.html",
        )

    def test_context_swieta(self):
        make_swieto()
        r = self.client.get(reverse("bies:wyraj-lista"))
        self.assertIn("swieta", r.context)

    def test_context_kolo_data_is_json(self):
        import json
        make_swieto(kolo_kat=90, kolo_kolor="#aabbcc")
        r = self.client.get(reverse("bies:wyraj-lista"))
        data = json.loads(r.context["kolo_data"])
        self.assertEqual(data[0]["kat"], 90)
        self.assertEqual(data[0]["kolor"], "#aabbcc")

    def test_empty_lista_200(self):
        self.assertEqual(
            self.client.get(reverse("bies:wyraj-lista")).status_code, 200
        )


# ── Widok: wyraj_detail ──────────────────────────

class WyrajDetailViewTests(TestCase):

    def setUp(self):
        self.s1 = make_swieto(slug="gaik",  kolejnosc=1, tytul_pl="Gaik")
        self.s2 = make_swieto(slug="jare",  kolejnosc=2, tytul_pl="Jare Gody")
        self.s3 = make_swieto(slug="trzeci",kolejnosc=3, tytul_pl="Trzecie")

    def test_returns_200(self):
        self.assertEqual(
            self.client.get(reverse("bies:wyraj-detail", args=["gaik"])).status_code, 200
        )

    def test_returns_404(self):
        self.assertEqual(
            self.client.get(reverse("bies:wyraj-detail", args=["nie-ma"])).status_code, 404
        )

    def test_template_used(self):
        self.assertTemplateUsed(
            self.client.get(reverse("bies:wyraj-detail", args=["gaik"])),
            "bies/wyraj/detail.html",
        )

    def test_context_swieto(self):
        r = self.client.get(reverse("bies:wyraj-detail", args=["gaik"]))
        self.assertEqual(r.context["swieto"], self.s1)

    def test_context_prev_next(self):
        r = self.client.get(reverse("bies:wyraj-detail", args=["jare"]))
        self.assertEqual(r.context["prev"], self.s1)
        self.assertEqual(r.context["next"], self.s3)

    def test_first_has_no_prev(self):
        r = self.client.get(reverse("bies:wyraj-detail", args=["gaik"]))
        self.assertIsNone(r.context["prev"])

    def test_last_has_no_next(self):
        r = self.client.get(reverse("bies:wyraj-detail", args=["trzeci"]))
        self.assertIsNone(r.context["next"])

    def test_duchy_in_response(self):
        self.s1.duchy_pl = "Jaryło, Marzanna"
        self.s1.save()
        r = self.client.get(reverse("bies:wyraj-detail", args=["gaik"]))
        self.assertContains(r, "Jaryło")
        self.assertContains(r, "Marzanna")


# ── URL patterns ─────────────────────────────────

class UrlTests(TestCase):

    def test_lista_url(self):
        self.assertEqual(reverse("bies:wyraj-lista"), "/wyraj/")

    def test_detail_url(self):
        self.assertEqual(
            reverse("bies:wyraj-detail", args=["szczodre-gody"]),
            "/wyraj/szczodre-gody/",
        )
