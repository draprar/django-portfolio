from django.db import models
from django.utils.text import slugify


class Swieto(models.Model):
    """
    Jedno słowiańskie święto z Koła Roku.
    Treść przechowywana dwujęzycznie (PL + EN) bezpośrednio w polach modelu.
    Obrazek zarządzany przez panel admina.
    """

    # --- identyfikator i kolejność ---
    slug = models.SlugField(
        max_length=80,
        unique=True,
        help_text="Część URL-a, np. 'gaik', 'jare-gody'. Wypełnia się automatycznie.",
    )
    kolejnosc = models.PositiveSmallIntegerField(
        default=0,
        help_text="Kolejność wyświetlania na liście (rosnąco).",
    )

    # --- tytuł ---
    tytul_pl = models.CharField(max_length=120, verbose_name="Tytuł (PL)")
    tytul_en = models.CharField(max_length=120, verbose_name="Tytuł (EN)")

    # --- podtytuł / czas obchodów ---
    podtytul_pl = models.CharField(
        max_length=220, blank=True, verbose_name="Podtytuł (PL)"
    )
    podtytul_en = models.CharField(
        max_length=220, blank=True, verbose_name="Podtytuł (EN)"
    )

    # --- meta description dla SEO ---
    meta_opis_pl = models.CharField(
        max_length=300, blank=True, verbose_name="Meta opis (PL)"
    )
    meta_opis_en = models.CharField(
        max_length=300, blank=True, verbose_name="Meta opis (EN)"
    )

    # --- obrazek ---
    obraz = models.ImageField(
        upload_to="bies/swieta/",
        blank=True,
        null=True,
        verbose_name="Obrazek",
        help_text="Zalecany format: PNG lub JPG, min. 1200×800 px.",
    )

    # --- sekcja: O święcie ---
    o_swiecie_pl = models.TextField(verbose_name="O święcie (PL)", blank=True)
    o_swiecie_en = models.TextField(verbose_name="O święcie (EN)", blank=True)

    # --- sekcja: Obrzędy ---
    obrzedy_pl = models.TextField(verbose_name="Obrzędy (PL)", blank=True)
    obrzedy_en = models.TextField(verbose_name="Obrzędy (EN)", blank=True)

    # --- sekcja: Symbolika ---
    symbolika_pl = models.TextField(verbose_name="Symbolika (PL)", blank=True)
    symbolika_en = models.TextField(verbose_name="Symbolika (EN)", blank=True)

    # --- daty systemowe ---
    utworzone = models.DateTimeField(auto_now_add=True)
    zaktualizowane = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Święto"
        verbose_name_plural = "Święta"
        ordering = ["kolejnosc", "tytul_pl"]

    def __str__(self):
        return self.tytul_pl

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.tytul_pl)
        super().save(*args, **kwargs)

    def get_tytul(self, lang="pl"):
        return self.tytul_en if lang == "en" else self.tytul_pl

    def get_podtytul(self, lang="pl"):
        return self.podtytul_en if lang == "en" else self.podtytul_pl

    def get_o_swiecie(self, lang="pl"):
        return self.o_swiecie_en if lang == "en" else self.o_swiecie_pl

    def get_obrzedy(self, lang="pl"):
        return self.obrzedy_en if lang == "en" else self.obrzedy_pl

    def get_symbolike(self, lang="pl"):
        return self.symbolika_en if lang == "en" else self.symbolika_pl


class ZrodloBibliograficzne(models.Model):
    """
    Źródło powiązane ze świętem — autor, tytuł, rok, link.
    Jeden wiersz w bazie = jeden punktor na liście źródeł.
    """

    swieto = models.ForeignKey(
        Swieto,
        on_delete=models.CASCADE,
        related_name="zrodla",
        verbose_name="Święto",
    )
    kolejnosc = models.PositiveSmallIntegerField(
        default=0,
        help_text="Kolejność na liście źródeł.",
    )

    autor = models.CharField(
        max_length=200, blank=True, verbose_name="Autor",
        help_text="Np. 'Oskar Kolberg'",
    )
    tytul = models.CharField(
        max_length=400, verbose_name="Tytuł dzieła",
        help_text="Np. 'Pieśni ludu obrzędowe: kogutek, gaik, okrężne'",
    )
    wydawca_rok = models.CharField(
        max_length=200, blank=True, verbose_name="Wydawca / rok",
        help_text="Np. 'WAM, 2003' lub '(1848)'",
    )
    url = models.URLField(
        blank=True, verbose_name="Link (opcjonalnie)",
        help_text="Np. link do Wikipedii lub skanów.",
    )
    # Etykieta linka — tylko gdy url jest wypełniony
    url_etykieta = models.CharField(
        max_length=200, blank=True, verbose_name="Etykieta linka",
        help_text="Np. 'Wikipedia — Gaik'. Wypełnij tylko jeśli podano URL.",
    )

    class Meta:
        verbose_name = "Źródło bibliograficzne"
        verbose_name_plural = "Źródła bibliograficzne"
        ordering = ["kolejnosc"]

    def __str__(self):
        autor = f"{self.autor}, " if self.autor else ""
        return f"{autor}{self.tytul}"
