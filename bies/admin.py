from django.contrib import admin
from django.utils.html import format_html

from .models import Swieto, ZrodloBibliograficzne


class ZrodloInline(admin.TabularInline):
    # Inline editor for bibliographic sources inside Swieto admin
    model = ZrodloBibliograficzne
    extra = 1
    fields = ("kolejnosc", "autor", "tytul", "wydawca_rok", "url", "url_etykieta")
    ordering = ("kolejnosc",)


@admin.register(Swieto)
class SwietoAdmin(admin.ModelAdmin):
    # Columns shown in the list view
    list_display = (
        "tytul_pl",
        "tytul_en",
        "slug",
        "kolejnosc",
        "kolo_kat",
        "podglad_obrazka",
        "zaktualizowane",
    )

    # Editable fields directly in list view
    list_editable = ("kolejnosc", "kolo_kat")

    # Auto-generate slug from title (PL)
    prepopulated_fields = {"slug": ("tytul_pl",)}

    # Searchable fields in admin search bar
    search_fields = ("tytul_pl", "tytul_en", "slug")

    # Default ordering in admin list view
    ordering = ("kolejnosc", "tytul_pl")

    # Read-only fields in detail view
    readonly_fields = ("podglad_obrazka", "utworzone", "zaktualizowane")

    # Inline models displayed inside Swieto admin
    inlines = [ZrodloInline]

    # Field grouping in admin form
    fieldsets = (
        ("Identifier", {
            "fields": ("slug", "kolejnosc"),
        }),
        ("Title and Subtitle", {
            "fields": (
                ("tytul_pl", "tytul_en"),
                ("podtytul_pl", "podtytul_en"),
            ),
        }),
        ("Wheel of the Year", {
            "fields": (("kolo_kat", "kolo_kolor"),),
            "description": (
                "kolo_kat: 0° = top (winter solstice), then clockwise. "
                "Spring equinox ≈ 90°, summer solstice ≈ 180°, autumn equinox ≈ 270°."
            ),
        }),
        ("Spirits and Deities", {
            "fields": (("duchy_pl", "duchy_en"),),
            "description": "Comma-separated values, e.g. 'Jaryło, Marzanna, Spring'.",
        }),
        ("SEO", {
            "classes": ("collapse",),
            "fields": (("meta_opis_pl", "meta_opis_en"),),
        }),
        ("Image", {
            "fields": ("obraz", "podglad_obrazka"),
        }),
        ("About", {
            "fields": ("o_swiecie_pl", "o_swiecie_en"),
        }),
        ("Rituals", {
            "fields": ("obrzedy_pl", "obrzedy_en"),
        }),
        ("Symbolism", {
            "fields": ("symbolika_pl", "symbolika_en"),
        }),
        ("System timestamps", {
            "classes": ("collapse",),
            "fields": ("utworzone", "zaktualizowane"),
        }),
    )

    @admin.display(description="Preview")
    def podglad_obrazka(self, obj):
        if obj.obraz:
            return format_html(
                '<img src="{}" style="max-height:80px;max-width:160px;'
                'object-fit:cover;border-radius:5px;"/>',
                obj.obraz.url,
            )
        return "—"
