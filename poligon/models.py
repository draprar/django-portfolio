from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class LearnerState(models.Model):
    """One learner's plan and progress.

    Only an account gets a row here. Practising without one leaves nothing
    behind: the level lives in the session and goes away with the visit.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="poligon_state",
    )
    practice_level = models.PositiveSmallIntegerField(
        default=2,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    target_profile = models.CharField(max_length=8, default="2222")
    target_date = models.DateField(null=True, blank=True)
    daily_minutes = models.PositiveIntegerField(default=35)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Learner state"
        verbose_name_plural = "Learner states"

    def __str__(self) -> str:
        return f"{self.user.username} / {self.target_profile}"


class Exercise(models.Model):
    SKILLS = [
        ("L", "Listening"),
        ("S", "Speaking"),
        ("R", "Reading"),
        ("W", "Writing"),
    ]
    TYPES = [
        ("mcq", "Multiple choice"),
        ("listening", "Listening"),
        ("speaking", "Speaking"),
        ("writing", "Writing"),
    ]
    SOURCES = [
        ("original", "Original"),
        ("wiktionary", "Wiktionary"),
        ("wikipedia", "Wikipedia"),
        ("tatoeba", "Tatoeba"),
        ("wikidata", "Wikidata"),
    ]

    slug = models.SlugField(unique=True)
    skill = models.CharField(max_length=1, choices=SKILLS)
    level = models.PositiveSmallIntegerField(default=2)
    exercise_type = models.CharField(max_length=20, choices=TYPES)
    expected_minutes = models.PositiveSmallIntegerField(default=7)
    original_content = models.BooleanField(default=True)
    source_note = models.CharField(max_length=220, default="Original Poligon content")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    title_pl = models.CharField(max_length=180, verbose_name=_("Title (PL)"))
    title_en = models.CharField(max_length=180, verbose_name=_("Title (EN)"))
    instructions_pl = models.TextField(verbose_name=_("Instructions (PL)"))
    instructions_en = models.TextField(verbose_name=_("Instructions (EN)"))
    prompt_pl = models.TextField(verbose_name=_("Prompt (PL)"))
    prompt_en = models.TextField(verbose_name=_("Prompt (EN)"))
    content_pl = models.TextField(blank=True, verbose_name=_("Content (PL)"))
    content_en = models.TextField(blank=True, verbose_name=_("Content (EN)"))
    category_pl = models.CharField(max_length=80, blank=True, verbose_name=_("Category (PL)"))
    category_en = models.CharField(max_length=80, blank=True, verbose_name=_("Category (EN)"))
    explanation_pl = models.TextField(blank=True, verbose_name=_("Why (PL)"))
    explanation_en = models.TextField(blank=True, verbose_name=_("Why (EN)"))
    content_source = models.CharField(max_length=20, choices=SOURCES, default="original")
    source_url = models.URLField(blank=True)
    source_license = models.CharField(max_length=80, blank=True)
    retrieved_at = models.DateField(null=True, blank=True)
    attribution_en = models.CharField(max_length=300, blank=True)
    attribution_pl = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = "Exercise"
        verbose_name_plural = "Exercises"
        ordering = ["id"]

    def __str__(self) -> str:
        return self.title_en

    def get_title(self, lang: str = "pl") -> str:
        return self.title_en if lang == "en" else self.title_pl

    def get_instructions(self, lang: str = "pl") -> str:
        return self.instructions_en if lang == "en" else self.instructions_pl

    def get_prompt(self, lang: str = "pl") -> str:
        return self.prompt_en if lang == "en" else self.prompt_pl

    def get_content(self, lang: str = "pl") -> str:
        return self.content_en if lang == "en" else self.content_pl

    def get_category(self, lang: str = "pl") -> str:
        return self.category_en if lang == "en" else self.category_pl

    def get_explanation(self, lang: str = "pl") -> str:
        return self.explanation_en if lang == "en" else self.explanation_pl


class ChoiceOption(models.Model):
    exercise = models.ForeignKey(Exercise, related_name="options", on_delete=models.CASCADE)
    text_pl = models.CharField(max_length=300, verbose_name=_("Text (PL)"))
    text_en = models.CharField(max_length=300, verbose_name=_("Text (EN)"))
    is_correct = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Choice option"
        verbose_name_plural = "Choice options"

    def __str__(self) -> str:
        return self.text_en

    def get_text(self, lang: str = "pl") -> str:
        return self.text_en if lang == "en" else self.text_pl


class Submission(models.Model):
    learner = models.ForeignKey(LearnerState, on_delete=models.CASCADE, related_name="submissions")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
    selected_option = models.ForeignKey(ChoiceOption, null=True, blank=True, on_delete=models.SET_NULL)
    score = models.FloatField(null=True, blank=True)
    feedback = models.JSONField(default=dict, blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-completed_at"]
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"

    def __str__(self) -> str:
        return f"{self.learner_id} / {self.exercise_id}"


class VocabularyItem(models.Model):
    SOURCES = [
        ("original", "Original"),
        ("wiktionary", "Wiktionary"),
        ("wikipedia", "Wikipedia"),
        ("tatoeba", "Tatoeba"),
        ("wikidata", "Wikidata"),
    ]

    term = models.CharField(max_length=120, unique=True)
    translation = models.CharField(max_length=180)
    explanation_pl = models.TextField(verbose_name=_("Explanation (PL)"))
    explanation_en = models.TextField(verbose_name=_("Explanation (EN)"))
    example_pl = models.TextField(verbose_name=_("Example (PL)"))
    example_en = models.TextField(verbose_name=_("Example (EN)"))
    category_pl = models.CharField(max_length=80, default="ogólny", verbose_name=_("Category (PL)"))
    category_en = models.CharField(max_length=80, default="general", verbose_name=_("Category (EN)"))
    level = models.PositiveSmallIntegerField(default=2)
    active = models.BooleanField(default=True)
    content_source = models.CharField(max_length=20, choices=SOURCES, default="original")
    source_url = models.URLField(blank=True)
    source_license = models.CharField(max_length=80, blank=True)
    retrieved_at = models.DateField(null=True, blank=True)
    attribution_en = models.CharField(max_length=240, blank=True)
    attribution_pl = models.CharField(max_length=240, blank=True)

    class Meta:
        verbose_name = "Vocabulary item"
        verbose_name_plural = "Vocabulary items"
        ordering = ["term"]

    def __str__(self) -> str:
        return self.term

    def get_explanation(self, lang: str = "pl") -> str:
        return self.explanation_en if lang == "en" else self.explanation_pl

    def get_example(self, lang: str = "pl") -> str:
        return self.example_en if lang == "en" else self.example_pl

    def get_category(self, lang: str = "pl") -> str:
        return self.category_en if lang == "en" else self.category_pl


class Review(models.Model):
    learner = models.ForeignKey(LearnerState, on_delete=models.CASCADE, related_name="reviews")
    item = models.ForeignKey(VocabularyItem, on_delete=models.CASCADE)
    due_at = models.DateTimeField()
    interval_days = models.PositiveIntegerField(default=0)
    ease = models.FloatField(default=2.5)
    repetitions = models.PositiveIntegerField(default=0)
    last_grade = models.PositiveSmallIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["learner", "item"], name="poligon_review_learner_item_uniq"),
        ]
        ordering = ["due_at"]
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self) -> str:
        return f"{self.learner_id} / {self.item_id}"


class StudyEvent(models.Model):
    learner = models.ForeignKey(LearnerState, on_delete=models.CASCADE, related_name="events")
    skill = models.CharField(max_length=1)
    minutes = models.PositiveSmallIntegerField(default=0)
    note = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Study event"
        verbose_name_plural = "Study events"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.learner_id} / {self.skill}"
