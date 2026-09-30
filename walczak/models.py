from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from walczak.dimensions import DIMENSIONS

SCORE = [MinValueValidator(0), MaxValueValidator(5)]


class StyleType(models.Model):
    code = models.SlugField(unique=True)
    name_pl = models.CharField(max_length=80)
    name_en = models.CharField(max_length=80)

    class Meta:
        ordering = ["name_pl"]

    def __str__(self) -> str:
        return self.name_pl


class Tag(models.Model):
    slug = models.SlugField(unique=True)
    name_pl = models.CharField(max_length=80)
    name_en = models.CharField(max_length=80)

    class Meta:
        ordering = ["name_pl"]

    def __str__(self) -> str:
        return self.name_pl


class Style(models.Model):
    """One combat style in the catalog. Serious fields stay factual; the joke is separate."""

    FAMILY_CHOICES = [
        ("uderzenia", "Uderzenia"),
        ("chwyty", "Chwyty"),
        ("mieszane", "Mieszane"),
        ("bron", "Broń"),
    ]
    FAMILY_EN = {
        "uderzenia": "Striking",
        "chwyty": "Grappling",
        "mieszane": "Mixed",
        "bron": "Weapons",
    }
    SET_CHOICES = [
        ("core", "Core"),
        ("golden", "Golden"),
    ]
    COMPETITION_CHOICES = [
        ("sport", "Sport competition"),
        ("traditional", "Traditional practice"),
        ("both", "Both"),
        ("none", "Neither"),
        ("historical", "Historical"),
    ]
    WEAPON_CHOICES = [
        ("none", "None"),
        ("optional", "Optional"),
        ("primary", "Primary"),
        ("training", "Training weapon"),
    ]

    slug = models.SlugField(unique=True)
    name_pl = models.CharField(max_length=80, verbose_name="Name (PL)")
    name_en = models.CharField(max_length=80, verbose_name="Name (EN)")
    family = models.CharField(max_length=20, choices=FAMILY_CHOICES)
    catalog_set = models.CharField(max_length=12, choices=SET_CHOICES, default="core")
    origin_pl = models.CharField(max_length=160, blank=True)
    origin_en = models.CharField(max_length=160, blank=True)
    region = models.CharField(max_length=80, blank=True)
    period_pl = models.CharField(max_length=160, blank=True)
    period_en = models.CharField(max_length=160, blank=True)
    competition_status = models.CharField(max_length=20, choices=COMPETITION_CHOICES, default="both")
    weapon_status = models.CharField(max_length=20, choices=WEAPON_CHOICES, default="none")
    sources_disagree = models.BooleanField(default=False)
    is_umbrella = models.BooleanField(default=False)
    matcher_enabled = models.BooleanField(default=True)
    joke_pl = models.CharField(max_length=240, blank=True, verbose_name="Joke (PL)")
    joke_en = models.CharField(max_length=240, blank=True, verbose_name="Joke (EN)")
    summary_pl = models.TextField(verbose_name="Summary (PL)")
    summary_en = models.TextField(verbose_name="Summary (EN)")
    history_pl = models.TextField(blank=True, verbose_name="History (PL)")
    history_en = models.TextField(blank=True, verbose_name="History (EN)")
    practice_pl = models.TextField(blank=True, verbose_name="How it is fought (PL)")
    practice_en = models.TextField(blank=True, verbose_name="How it is fought (EN)")
    sort_order = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(default=True)
    style_types = models.ManyToManyField(StyleType, blank=True, related_name="styles")
    tags = models.ManyToManyField(Tag, blank=True, related_name="styles")

    class Meta:
        ordering = ["sort_order", "name_pl"]
        verbose_name = "Style"
        verbose_name_plural = "Styles"

    def __str__(self) -> str:
        return self.name_pl

    @property
    def family_en(self) -> str:
        return self.FAMILY_EN.get(self.family, self.family)


class Source(models.Model):
    """A bibliographic pointer. The card links out; it does not quote the work."""

    TYPE_CHOICES = [
        ("academic", "Academic"),
        ("federation", "Federation"),
        ("historical", "Historical"),
        ("encyclopedia", "Encyclopedia"),
        ("wikimedia", "Wikimedia"),
        ("wikipedia", "Wikipedia / Wikidata"),
        ("public_domain", "Public domain"),
        ("other", "Other"),
    ]
    ROLE_CHOICES = [
        ("definition", "Definition"),
        ("history", "History"),
        ("rules", "Rules"),
        ("current_practice", "Current practice"),
        ("heritage", "Heritage"),
        ("academic", "Academic"),
        ("psychology", "Psychology"),
        ("image", "Image"),
        ("discovery", "Discovery"),
    ]
    QUALITY_CHOICES = [
        ("institutional", "Institutional"),
        ("academic", "Academic"),
        ("reputable_reference", "Reputable reference"),
        ("secondary", "Secondary"),
        ("discovery_only", "Discovery only"),
    ]

    style = models.ForeignKey(
        Style,
        related_name="sources",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    author = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=300)
    url = models.URLField(blank=True)
    source_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="other")
    role = models.CharField(max_length=24, choices=ROLE_CHOICES, default="definition")
    quality = models.CharField(max_length=24, choices=QUALITY_CHOICES, default="secondary")
    publication_date = models.CharField(max_length=40, blank=True)
    license = models.CharField(max_length=80, blank=True)
    license_url = models.URLField(blank=True)
    attribution = models.CharField(max_length=300, blank=True)
    accessed_at = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Source"
        verbose_name_plural = "Sources"

    def __str__(self) -> str:
        return self.title


class TrainingProfile(models.Model):
    style = models.OneToOneField(Style, related_name="profile", on_delete=models.CASCADE)
    striking = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    grappling = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    clinch = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    throws = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    takedowns = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    ground_fighting = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    submissions = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    punches = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    kicks = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    knees = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    elbows = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    weapons = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    solo_training = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    partner_training = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    contact_level = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    competition_level = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    tradition_level = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    technical_complexity = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    athletic_demand = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    endurance_demand = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    explosiveness = models.PositiveSmallIntegerField(default=0, validators=SCORE)
    equipment_required = models.PositiveSmallIntegerField(default=0, validators=SCORE)

    def as_vector(self) -> dict[str, int]:
        return {name: int(getattr(self, name)) for name in DIMENSIONS}


class StyleRelation(models.Model):
    KIND_CHOICES = [
        ("variant", "Variant"),
        ("umbrella", "Umbrella"),
        ("subset", "Subset"),
        ("related", "Related"),
        ("influenced", "Influenced"),
        ("derived_from", "Derived from"),
        ("historical_precursor", "Historical precursor"),
        ("modern_form", "Modern form"),
    ]

    from_style = models.ForeignKey(Style, related_name="relations_out", on_delete=models.CASCADE)
    to_style = models.ForeignKey(Style, related_name="relations_in", on_delete=models.CASCADE)
    kind = models.CharField(max_length=32, choices=KIND_CHOICES)
    note_pl = models.CharField(max_length=240, blank=True)
    note_en = models.CharField(max_length=240, blank=True)
    sources = models.ManyToManyField(Source, blank=True, related_name="relations")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["from_style", "to_style", "kind"], name="uniq_style_relation"),
        ]

    def __str__(self) -> str:
        return f"{self.from_style_id} {self.kind} {self.to_style_id}"

    def clean(self) -> None:
        if self.pk and not self.sources.exists():
            raise ValidationError("Relacja wymaga źródła.")


class Fact(models.Model):
    text_pl = models.TextField()
    text_en = models.TextField()
    is_legend = models.BooleanField(default=False)
    styles = models.ManyToManyField(Style, blank=True, related_name="facts")
    sources = models.ManyToManyField(Source, blank=True, related_name="facts")

    def __str__(self) -> str:
        return self.text_pl[:80]


class Question(models.Model):
    """Legacy humor-point quiz. Public /quiz/ no longer reads this model."""

    text_pl = models.TextField(verbose_name="Question (PL)")
    text_en = models.TextField(verbose_name="Question (EN)")
    sort_order = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "pk"]
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self) -> str:
        return self.text_pl[:80]


class Choice(models.Model):
    """One answer. Points land on a style, with an optional second style."""

    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    text_pl = models.CharField(max_length=300, verbose_name="Answer (PL)")
    text_en = models.CharField(max_length=300, verbose_name="Answer (EN)")
    sort_order = models.PositiveSmallIntegerField(default=0)
    style = models.ForeignKey(Style, related_name="choices", on_delete=models.PROTECT)
    points = models.PositiveSmallIntegerField(default=1)
    extra_style = models.ForeignKey(
        Style,
        related_name="extra_choices",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    extra_points = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "pk"]
        verbose_name = "Choice"
        verbose_name_plural = "Choices"

    def __str__(self) -> str:
        return self.text_pl[:80]

    def clean(self) -> None:
        if self.extra_style_id and self.extra_style_id == self.style_id:
            raise ValidationError("The extra style must be a different style.")
        if not self.extra_style_id:
            self.extra_points = 0


class PreferenceQuestion(models.Model):
    KIND_CHOICES = [
        ("scale", "Scale 1–5"),
        ("ab", "A or B"),
        ("situation", "Situation"),
        ("multi", "Several options"),
    ]

    text_pl = models.TextField()
    text_en = models.TextField()
    kind = models.CharField(max_length=16, choices=KIND_CHOICES)
    dimension = models.CharField(max_length=32, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "pk"]

    def __str__(self) -> str:
        return self.text_pl[:80]


class PreferenceOption(models.Model):
    question = models.ForeignKey(PreferenceQuestion, related_name="options", on_delete=models.CASCADE)
    text_pl = models.CharField(max_length=240)
    text_en = models.CharField(max_length=240)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "pk"]

    def __str__(self) -> str:
        return self.text_pl[:80]


class OptionWeight(models.Model):
    option = models.ForeignKey(PreferenceOption, related_name="weights", on_delete=models.CASCADE)
    dimension = models.CharField(max_length=32)
    weight = models.SmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["option", "dimension"], name="uniq_option_dimension"),
        ]


class IPIPScale(models.Model):
    code = models.SlugField(unique=True)
    name_pl = models.CharField(max_length=80)
    name_en = models.CharField(max_length=80)

    def __str__(self) -> str:
        return self.name_en


class IPIPItem(models.Model):
    scale = models.ForeignKey(IPIPScale, related_name="items", on_delete=models.CASCADE)
    text_en = models.TextField()
    text_pl = models.TextField()
    reverse = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)
    attribution = models.CharField(max_length=240, default="IPIP public-domain item. Polish wording is a project translation.")

    class Meta:
        ordering = ["sort_order", "pk"]

    def __str__(self) -> str:
        return self.text_en[:80]


class Study(models.Model):
    EVIDENCE_CHOICES = [
        ("strong", "Strong"),
        ("moderate", "Moderate"),
        ("limited", "Limited"),
        ("unclear", "Unclear"),
    ]

    title = models.CharField(max_length=240)
    year = models.CharField(max_length=20, blank=True)
    sample_size = models.CharField(max_length=40, blank=True)
    study_type = models.CharField(max_length=80, blank=True)
    styles = models.ManyToManyField(Style, related_name="studies")
    population = models.CharField(max_length=240, blank=True)
    design = models.CharField(max_length=240, blank=True)
    finding_pl = models.TextField(blank=True)
    finding_en = models.TextField(blank=True)
    limitation_pl = models.TextField(blank=True)
    limitation_en = models.TextField(blank=True)
    evidence = models.CharField(max_length=16, choices=EVIDENCE_CHOICES, default="unclear")
    sources = models.ManyToManyField(Source, blank=True, related_name="studies")

    def __str__(self) -> str:
        return self.title


class Archetype(models.Model):
    slug = models.SlugField(unique=True)
    name_pl = models.CharField(max_length=120)
    name_en = models.CharField(max_length=120)
    description_pl = models.TextField()
    description_en = models.TextField()
    styles = models.ManyToManyField(Style, blank=True, related_name="archetypes")

    def __str__(self) -> str:
        return self.name_pl


class HumorQuestion(models.Model):
    text_pl = models.TextField()
    text_en = models.TextField()
    sort_order = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "pk"]

    def __str__(self) -> str:
        return self.text_pl[:80]


class HumorChoice(models.Model):
    question = models.ForeignKey(HumorQuestion, related_name="choices", on_delete=models.CASCADE)
    text_pl = models.CharField(max_length=240)
    text_en = models.CharField(max_length=240)
    sort_order = models.PositiveSmallIntegerField(default=0)
    archetype = models.ForeignKey(Archetype, related_name="choices", on_delete=models.CASCADE)
    points = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["sort_order", "pk"]
