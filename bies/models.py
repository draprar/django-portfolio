from django.db import models
from django.utils.text import slugify


class Swieto(models.Model):
    """
    One Slavic Wheel of the Year festival.
    Content is stored bilingually (PL + EN) directly in model fields.
    """

    # --- identifier and ordering ---
    slug = models.SlugField(
        max_length=80,
        unique=True,
        help_text="URL part, e.g. 'gaik', 'jare-gody'. Auto-filled if empty.",
    )
    kolejnosc = models.PositiveSmallIntegerField(
        default=0,
        help_text="Ordering on list and position on the Wheel of the Year (1–12, ascending).",
    )

    # --- title ---
    tytul_pl = models.CharField(max_length=120, verbose_name="Title (PL)")
    tytul_en = models.CharField(max_length=120, verbose_name="Title (EN)")

    # --- subtitle / celebration time ---
    podtytul_pl = models.CharField(max_length=220, blank=True, verbose_name="Subtitle (PL)")
    podtytul_en = models.CharField(max_length=220, blank=True, verbose_name="Subtitle (EN)")

    # --- SEO meta description ---
    meta_opis_pl = models.CharField(max_length=300, blank=True, verbose_name="Meta description (PL)")
    meta_opis_en = models.CharField(max_length=300, blank=True, verbose_name="Meta description (EN)")

    # --- image ---
    obraz = models.ImageField(
        upload_to="bies/swieta/",
        blank=True,
        null=True,
        verbose_name="Image",
        help_text="Recommended format: PNG or JPG, min. 1200×800 px.",
    )

    # --- video (card + hero background) ---
    wideo = models.FileField(
        upload_to="bies/swieta/video/",
        blank=True,
        null=True,
        verbose_name="Video (MP4)",
        help_text="MP4, recommended max 10 MB. Used as card thumbnail and hero background.",
    )

    # --- Wheel of the Year: node angle (0° = top, clockwise direction) ---
    kolo_kat = models.SmallIntegerField(
        default=0,
        verbose_name="Wheel angle (degrees)",
        help_text=(
            "Festival position on the circle. 0° = top (winter solstice), "
            "then clockwise. E.g. spring equinox ≈ 90°."
        ),
    )

    # Node accent color — hex, e.g. '#c4922a'
    kolo_kolor = models.CharField(
        max_length=20,
        default="#c4922a",
        verbose_name="Wheel node color",
        help_text="Hex color, e.g. '#a3c47a' for spring, '#c4922a' for golden tones.",
    )

    # --- Calendar day of the festival (1–365) ---
    # Used by the Wheel of the Year JS to highlight the festival closest to
    # today's date. Count from Jan 1 = 1. For festivals straddling multiple
    # days use the central/most important day (e.g. Noc Kupały ≈ Jun 23 = 174).
    dzien_roku = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Day of year (1–365)",
        help_text=(
            "Approximate calendar day of this festival (Jan 1 = 1, Dec 31 = 365). "
            "Used to auto-highlight the nearest feast on the Wheel of the Year. "
            "E.g. Noc Kupały ≈ Jun 23 → 174, Szczodre Gody ≈ Dec 21 → 355."
        ),
    )

    # --- spirits and deities (comma-separated text) ---
    duchy_pl = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Spirits / deities (PL)",
        help_text="E.g. 'Jaryło, Marzanna, Wiosna'. Comma-separated.",
    )
    duchy_en = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Spirits / deities (EN)",
        help_text="E.g. 'Jaryło, Marzanna, Spring'. Comma-separated.",
    )

    # --- section: About ---
    o_swiecie_pl = models.TextField(verbose_name="About (PL)", blank=True)
    o_swiecie_en = models.TextField(verbose_name="About (EN)", blank=True)

    # --- section: Rituals ---
    obrzedy_pl = models.TextField(verbose_name="Rituals (PL)", blank=True)
    obrzedy_en = models.TextField(verbose_name="Rituals (EN)", blank=True)

    # --- section: Symbolism ---
    symbolika_pl = models.TextField(verbose_name="Symbolism (PL)", blank=True)
    symbolika_en = models.TextField(verbose_name="Symbolism (EN)", blank=True)

    # --- system timestamps ---
    utworzone = models.DateTimeField(auto_now_add=True)
    zaktualizowane = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Festival"
        verbose_name_plural = "Festivals"
        ordering = ["kolejnosc", "tytul_pl"]

    def __str__(self):
        return self.tytul_pl

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.tytul_pl)
        super().save(*args, **kwargs)

    # --- language getters ---
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

    def get_duchy_list(self, lang="pl"):
        """Returns spirits as a list of strings (comma-separated)."""
        raw = self.duchy_en if lang == "en" else self.duchy_pl
        return [d.strip() for d in raw.split(",") if d.strip()]

    # --- navigation prev/next ---
    def get_next(self):
        return (
            Swieto.objects.filter(kolejnosc__gt=self.kolejnosc)
            .order_by("kolejnosc")
            .first()
        )

    def get_prev(self):
        return (
            Swieto.objects.filter(kolejnosc__lt=self.kolejnosc)
            .order_by("-kolejnosc")
            .first()
        )


class ZrodloBibliograficzne(models.Model):
    """Bibliographic source linked to a festival."""

    swieto = models.ForeignKey(
        Swieto,
        on_delete=models.CASCADE,
        related_name="zrodla",
        verbose_name="Festival",
    )
    kolejnosc = models.PositiveSmallIntegerField(default=0)

    autor = models.CharField(max_length=200, blank=True, verbose_name="Author")
    tytul = models.CharField(max_length=400, verbose_name="Work title")
    wydawca_rok = models.CharField(max_length=200, blank=True, verbose_name="Publisher / year")
    url = models.URLField(blank=True, verbose_name="Link (optional)")
    url_etykieta = models.CharField(max_length=200, blank=True, verbose_name="Link label")

    class Meta:
        verbose_name = "Bibliographic source"
        verbose_name_plural = "Bibliographic sources"
        ordering = ["kolejnosc"]

    def __str__(self):
        autor = f"{self.autor}, " if self.autor else ""
        return f"{autor}{self.tytul}"