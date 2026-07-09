from django.contrib import admin
from django.utils.html import format_html

from .models import Bostwo, Swieto, ZrodloBibliograficzne


@admin.register(Bostwo)
class BostwoAdmin(admin.ModelAdmin):
    list_display = ("imie_pl", "imie_en", "kolejnosc", "podglad_portretu", "swieto")
    list_editable = ("kolejnosc",)
    ordering = ("kolejnosc", "imie_pl")
    search_fields = ("imie_pl", "imie_en")
    readonly_fields = ("podglad_portretu",)

    fieldsets = (
        ("Identifier", {"fields": ("kolejnosc", "swieto")}),
        ("Name", {"fields": (("imie_pl", "imie_en"), ("epitet_pl", "epitet_en"))}),
        ("Story", {"fields": ("opis_pl", "opis_en")}),
        ("Trivia", {
            "fields": ("ciekawostka_pl", "ciekawostka_en"),
            "description": "Shown in its own highlighted box in the patron panel. Leave blank to hide it.",
        }),
        ("Portrait", {"fields": ("obraz", "podglad_portretu")}),
    )

    @admin.display(description="Preview")
    def podglad_portretu(self, obj):
        if obj.obraz:
            return format_html(
                '<img src="{}" style="max-height:90px;max-width:90px;'
                'object-fit:cover;border-radius:50%;"/>',
                obj.obraz.url,
            )
        return "—"


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
            "fields": (("kolo_kat", "kolo_kolor"), ("dzien_roku", "dzien_roku_koniec")),
            "description": (
                "kolo_kat: 0° = top (winter solstice), then clockwise. "
                "Spring equinox ≈ 90°, summer solstice ≈ 180°, autumn equinox ≈ 270°. "
                "dzien_roku: calendar day 1–365 (Jan 1 = 1) used to auto-highlight "
                "the nearest feast on the Wheel. E.g. Noc Kupały ≈ Jun 23 → 174. "
                "dzien_roku_koniec: LEAVE BLANK for ordinary single-day feasts. "
                "Only fill it in if this feast spans a whole range of days — e.g. "
                "'all of January' would be dzien_roku=1, dzien_roku_koniec=31. "
                "Any day inside that range will auto-select this feast directly."
            ),
        }),
        ("Spirits and Deities — legacy fallback", {
            "classes": ("collapse",),
            "fields": (("duchy_pl", "duchy_en"),),
            "description": (
                "Old plain-text field, comma-separated. Only used on the page if "
                "no 'Bostwo' record is linked below. To get the portrait + story "
                "panel, add/edit the patron in Patrons / deities and attach this "
                "festival to it there."
            ),
        }),
        ("SEO", {
            "classes": ("collapse",),
            "fields": (("meta_opis_pl", "meta_opis_en"),),
        }),
        ("Image & Video", {
            "fields": (
                "obraz",
                "wideo",
                "podglad_obrazka",
            ),
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