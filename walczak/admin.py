from django.contrib import admin
from django.db.models import Count

from walczak.models import (
    Archetype,
    Choice,
    Fact,
    HumorChoice,
    HumorQuestion,
    IPIPItem,
    IPIPScale,
    OptionWeight,
    PreferenceOption,
    PreferenceQuestion,
    Question,
    Source,
    Study,
    Style,
    StyleRelation,
    StyleType,
    Tag,
    TrainingProfile,
)


class SourceInline(admin.TabularInline):
    model = Source
    extra = 0
    fields = ("sort_order", "author", "title", "url", "source_type", "role", "quality", "license")
    ordering = ("sort_order",)


class TrainingProfileInline(admin.StackedInline):
    model = TrainingProfile
    extra = 0


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
    autocomplete_fields = ("style", "extra_style")


class PreferenceOptionInline(admin.TabularInline):
    model = PreferenceOption
    extra = 0


class WeightInline(admin.TabularInline):
    model = OptionWeight
    extra = 0


class HumorChoiceInline(admin.TabularInline):
    model = HumorChoice
    extra = 0


class IPIPItemInline(admin.TabularInline):
    model = IPIPItem
    extra = 0


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ("name_pl", "catalog_set", "family", "matcher_enabled", "is_umbrella", "source_count", "active")
    list_filter = ("catalog_set", "family", "style_types", "tags", "matcher_enabled", "is_umbrella", "competition_status", "active")
    search_fields = ("name_pl", "name_en", "slug")
    prepopulated_fields = {"slug": ("name_en",)}
    filter_horizontal = ("style_types", "tags")
    inlines = [TrainingProfileInline, SourceInline]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(source_total=Count("sources"))

    @admin.display(description="Sources", ordering="source_total")
    def source_count(self, obj: Style) -> int:
        return int(obj.source_total)


@admin.register(StyleType)
class StyleTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name_pl", "name_en")
    search_fields = ("code", "name_pl")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("slug", "name_pl", "name_en")
    search_fields = ("slug", "name_pl")


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("title", "style", "role", "quality", "source_type")
    list_filter = ("role", "quality", "source_type")
    search_fields = ("title", "url", "style__slug")


@admin.register(StyleRelation)
class StyleRelationAdmin(admin.ModelAdmin):
    list_display = ("from_style", "kind", "to_style")
    list_filter = ("kind",)
    autocomplete_fields = ("from_style", "to_style")
    filter_horizontal = ("sources",)


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ("text_pl", "is_legend")
    list_filter = ("is_legend",)
    filter_horizontal = ("styles", "sources")


@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "sample_size", "study_type", "evidence")
    list_filter = ("evidence",)
    filter_horizontal = ("styles", "sources")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text_pl", "sort_order", "active")
    list_filter = ("active",)
    inlines = [ChoiceInline]


@admin.register(PreferenceQuestion)
class PreferenceQuestionAdmin(admin.ModelAdmin):
    list_display = ("text_pl", "kind", "dimension", "sort_order", "active")
    list_filter = ("kind", "active")
    inlines = [PreferenceOptionInline]


@admin.register(PreferenceOption)
class PreferenceOptionAdmin(admin.ModelAdmin):
    list_display = ("text_pl", "question")
    inlines = [WeightInline]


@admin.register(IPIPScale)
class IPIPScaleAdmin(admin.ModelAdmin):
    list_display = ("code", "name_pl", "name_en")
    inlines = [IPIPItemInline]


@admin.register(Archetype)
class ArchetypeAdmin(admin.ModelAdmin):
    list_display = ("name_pl", "slug")
    search_fields = ("slug", "name_pl")
    filter_horizontal = ("styles",)


@admin.register(HumorQuestion)
class HumorQuestionAdmin(admin.ModelAdmin):
    list_display = ("text_pl", "sort_order", "active")
    list_filter = ("active",)
    inlines = [HumorChoiceInline]
