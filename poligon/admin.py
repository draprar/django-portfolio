from django.contrib import admin

from .models import (
    ChoiceOption,
    Exercise,
    LearnerState,
    PlacementAttempt,
    ProductEvent,
    Review,
    StudyEvent,
    Submission,
    VocabularyItem,
)


class ChoiceOptionInline(admin.TabularInline):
    model = ChoiceOption
    extra = 1
    fields = ("sort_order", "text_pl", "text_en", "is_correct")
    ordering = ("sort_order",)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = (
        "title_en",
        "skill",
        "level",
        "scenario",
        "publication_status",
        "quality_status",
        "exercise_type",
        "catalog_role",
        "active",
    )
    list_filter = ("publication_status", "quality_status", "skill", "level", "scenario", "exercise_type", "active")
    search_fields = ("title_pl", "title_en", "prompt_pl", "prompt_en", "category_pl", "category_en")
    prepopulated_fields = {"slug": ("title_en",)}
    inlines = [ChoiceOptionInline]
    fieldsets = (
        (
            "Identifier",
            {
                "fields": (
                    "slug",
                    "skill",
                    "level",
                    "scenario",
                    "subskill",
                    "competency",
                    "exercise_type",
                    "expected_minutes",
                    "active",
                )
            },
        ),
        (
            "Publication",
            {
                "fields": (
                    "publication_status",
                    "quality_status",
                    "learning_objective",
                    "success_criteria",
                    "review_status",
                    "reviewed_by",
                    "reviewed_at",
                    "source_type",
                    "delivery",
                )
            },
        ),
        (
            "Provenance",
            {
                "fields": (
                    "original_content",
                    "source_note",
                    "content_source",
                    "source_url",
                    "source_license",
                    "retrieved_at",
                    "attribution_en",
                    "attribution_pl",
                )
            },
        ),
        (
            "🇵🇱 Polska wersja",
            {
                "fields": (
                    "title_pl",
                    "category_pl",
                    "instructions_pl",
                    "prompt_pl",
                    "content_pl",
                    "explanation_pl",
                )
            },
        ),
        (
            "🇬🇧 English version",
            {
                "fields": (
                    "title_en",
                    "category_en",
                    "instructions_en",
                    "prompt_en",
                    "content_en",
                    "explanation_en",
                ),
                "description": "Leave blank only if the Polish text is enough for this field.",
            },
        ),
    )


@admin.register(VocabularyItem)
class VocabularyItemAdmin(admin.ModelAdmin):
    list_display = ("term", "translation", "content_source", "category_en", "level", "publication_status", "active")
    list_filter = ("publication_status", "content_source", "level", "active")
    search_fields = ("term", "translation", "explanation_pl", "explanation_en")
    fieldsets = (
        ("Card", {"fields": ("term", "translation", "level", "publication_status", "active")}),
        ("🇵🇱 Polska wersja", {"fields": ("category_pl", "explanation_pl", "example_pl", "attribution_pl")}),
        ("🇬🇧 English version", {"fields": ("category_en", "explanation_en", "example_en", "attribution_en")}),
        (
            "Provenance",
            {"fields": ("content_source", "source_url", "source_license", "retrieved_at")},
        ),
    )


@admin.register(LearnerState)
class LearnerStateAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "practice_level", "target_profile", "daily_minutes", "target_date", "updated_at")
    list_filter = ("practice_level",)
    search_fields = ("user__username", "target_profile")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("learner", "exercise", "score", "completed_at")
    list_filter = ("exercise__skill",)
    search_fields = ("learner__user__username", "answer_text")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("learner", "item", "due_at", "interval_days", "ease", "last_grade")
    search_fields = ("learner__user__username", "item__term")


@admin.register(PlacementAttempt)
class PlacementAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "learner",
        "suggested_level",
        "correct_count",
        "question_count",
        "algorithm_version",
        "created_at",
    )
    list_filter = ("algorithm_version", "suggested_level")


@admin.register(ProductEvent)
class ProductEventAdmin(admin.ModelAdmin):
    list_display = ("name", "learner", "created_at")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(StudyEvent)
class StudyEventAdmin(admin.ModelAdmin):
    list_display = ("learner", "skill", "minutes", "note", "created_at")
    list_filter = ("skill",)
    search_fields = ("learner__user__username", "note")
