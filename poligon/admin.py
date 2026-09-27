from django.contrib import admin

from .models import ChoiceOption, Exercise, LearnerState, Review, StudyEvent, Submission, VocabularyItem


class ChoiceOptionInline(admin.TabularInline):
    model = ChoiceOption
    extra = 1
    fields = ("sort_order", "text_pl", "text_en", "is_correct")
    ordering = ("sort_order",)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("title_pl", "title_en", "skill", "level", "content_source", "exercise_type", "active")
    list_filter = ("skill", "level", "content_source", "exercise_type", "active")
    search_fields = ("title_pl", "title_en", "prompt_pl", "prompt_en", "category_pl", "category_en")
    prepopulated_fields = {"slug": ("title_en",)}
    inlines = [ChoiceOptionInline]
    fieldsets = (
        ("Identifier", {"fields": ("slug", "skill", "level", "exercise_type", "expected_minutes", "active")}),
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
            {"fields": ("title_pl", "category_pl", "instructions_pl", "prompt_pl", "content_pl")},
        ),
        (
            "🇬🇧 English version",
            {
                "fields": ("title_en", "category_en", "instructions_en", "prompt_en", "content_en"),
                "description": "Leave blank only if the Polish text is enough for this field.",
            },
        ),
    )


@admin.register(VocabularyItem)
class VocabularyItemAdmin(admin.ModelAdmin):
    list_display = ("term", "translation", "content_source", "category_en", "level", "active")
    list_filter = ("content_source", "level", "active")
    search_fields = ("term", "translation", "explanation_pl", "explanation_en")
    fieldsets = (
        ("Card", {"fields": ("term", "translation", "level", "active")}),
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
    search_fields = ("user__username", "guest_token", "target_profile")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("learner", "exercise", "score", "completed_at")
    list_filter = ("exercise__skill",)
    search_fields = ("learner__user__username", "answer_text")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("learner", "item", "due_at", "interval_days", "ease", "last_grade")
    search_fields = ("learner__user__username", "item__term")


@admin.register(StudyEvent)
class StudyEventAdmin(admin.ModelAdmin):
    list_display = ("learner", "skill", "minutes", "note", "created_at")
    list_filter = ("skill",)
    search_fields = ("learner__user__username", "note")
