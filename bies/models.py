from django.db import models
from django.utils.text import slugify

from core.storages_backends import get_bies_storage


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
        storage=get_bies_storage,
        blank=True,
        null=True,
        verbose_name="Image",
        help_text="Recommended format: PNG or JPG, min. 1200×800 px.",
    )

    # --- video (card + hero background) ---
    wideo = models.FileField(
        upload_to="bies/swieta/video/",
        storage=get_bies_storage,
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
            "E.g. Noc Kupały ≈ Jun 23 → 174, Szczodre Gody ≈ Dec 21 → 355. "
            "If 'Day of year — end' below is set, this is the START of a range."
        ),
    )

    # --- Optional END day, for festivals spanning a whole range (e.g. all of
    # January) instead of a single date. Leave blank for single-day feasts —
    # everything keeps working exactly as before. When set, ANY day inside
    # [dzien_roku, dzien_roku_koniec] (inclusive) auto-selects this festival
    # directly, before the "closest single day" fallback is even considered.
    # A range where the end is SMALLER than the start (e.g. 355 → 10) is
    # treated as wrapping over New Year's Eve.
    dzien_roku_koniec = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Day of year — end (optional)",
        help_text=(
            "Only for festivals spanning a range of days, e.g. all of January "
            "= 1 to 31. Leave BLANK for ordinary single-day festivals — do not "
            "fill this in unless the festival really covers a whole period."
        ),
    )

    # --- spirits and deities (comma-separated text) ---
    duchy_pl = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Spirits / deities (PL) — legacy",
        help_text=(
            "DEPRECATED fallback, comma-separated plain text. "
            "Prefer linking a proper 'Bostwo' record below instead — that gives "
            "a portrait, a storytelling description and a trivia box on the page."
        ),
    )
    duchy_en = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Spirits / deities (EN) — legacy",
        help_text="DEPRECATED fallback — see PL field.",
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


class Bostwo(models.Model):
    """
    A patron spirit / deity (one per month, in current usage) linked to
    one or more festivals. Replaces the old free-text 'duchy_pl/en' fields
    with a real record that can carry a portrait, a storytelling
    description, and a trivia note.
    """

    swieto = models.OneToOneField(
        Swieto,
        on_delete=models.CASCADE,
        related_name="bostwo",
        blank=True,
        null=True,
        verbose_name="Festival / month",
        help_text="The one festival (month) this patron watches over.",
    )

    kolejnosc = models.PositiveSmallIntegerField(
        default=0,
        help_text="Display order, e.g. 1–12 following the months of the year.",
    )

    imie_pl = models.CharField(max_length=80, verbose_name="Name (PL)")
    imie_en = models.CharField(max_length=80, verbose_name="Name (EN)")

    epitet_pl = models.CharField(
        max_length=160, blank=True, verbose_name="Epithet / tagline (PL)",
        help_text="Short line under the name, e.g. 'Pan przełomu i cieni'.",
    )
    epitet_en = models.CharField(
        max_length=160, blank=True, verbose_name="Epithet / tagline (EN)",
    )

    opis_pl = models.TextField(
        verbose_name="Story (PL)",
        help_text="Longer, narrative description — same storytelling tone as festival sections.",
    )
    opis_en = models.TextField(verbose_name="Story (EN)")

    ciekawostka_pl = models.TextField(
        blank=True, verbose_name="Trivia (PL)",
        help_text="Short 'did you know' aside shown in its own box in the panel.",
    )
    ciekawostka_en = models.TextField(blank=True, verbose_name="Trivia (EN)")

    obraz = models.ImageField(
        upload_to="bies/bostwa/",
        storage=get_bies_storage,
        blank=True,
        null=True,
        verbose_name="Portrait",
    )

    class Meta:
        verbose_name = "Patron / deity"
        verbose_name_plural = "Patrons / deities"
        ordering = ["kolejnosc", "imie_pl"]

    def __str__(self):
        return self.imie_pl

    def get_imie(self, lang="pl"):
        return self.imie_en if lang == "en" else self.imie_pl

    def get_epitet(self, lang="pl"):
        return self.epitet_en if lang == "en" else self.epitet_pl

    def get_opis(self, lang="pl"):
        return self.opis_en if lang == "en" else self.opis_pl

    def get_ciekawostka(self, lang="pl"):
        return self.ciekawostka_en if lang == "en" else self.ciekawostka_pl


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