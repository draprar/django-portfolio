from django.contrib import admin
from django.utils.html import format_html

from .models import Swieto, ZrodloBibliograficzne


class ZrodloInline(admin.TabularInline):
    model = ZrodloBibliograficzne
    extra = 1
    fields = ("kolejnosc", "autor", "tytul", "wydawca_rok", "url", "url_etykieta")
    ordering = ("kolejnosc",)


@admin.register(Swieto)
class SwietoAdmin(admin.ModelAdmin):
    list_display   = ("tytul_pl", "tytul_en", "slug", "kolejnosc", "kolo_kat", "podglad_obrazka", "zaktualizowane")
    list_editable  = ("kolejnosc", "kolo_kat")
    prepopulated_fields = {"slug": ("tytul_pl",)}
    search_fields  = ("tytul_pl", "tytul_en", "slug")
    ordering       = ("kolejnosc", "tytul_pl")
    readonly_fields = ("podglad_obrazka", "utworzone", "zaktualizowane")
    inlines        = [ZrodloInline]

    fieldsets = (
        ("Identyfikator", {
            "fields": ("slug", "kolejnosc"),
        }),
        ("Tytuł i podtytuł", {
            "fields": (
                ("tytul_pl", "tytul_en"),
                ("podtytul_pl", "podtytul_en"),
            ),
        }),
        ("Koło Roku", {
            "fields": (("kolo_kat", "kolo_kolor"),),
            "description": (
                "kolo_kat: 0° = szczyt (przesilenie zimowe), dalej zgodnie z ruchem wskazówek. "
                "Równonoc wiosenna ≈ 90°, przesilenie letnie ≈ 180°, równonoc jesienna ≈ 270°."
            ),
        }),
        ("Duchy i bóstwa", {
            "fields": (("duchy_pl", "duchy_en"),),
            "description": "Oddzielone przecinkami, np. 'Jaryło, Marzanna, Wiosna'.",
        }),
        ("SEO", {
            "classes": ("collapse",),
            "fields": (("meta_opis_pl", "meta_opis_en"),),
        }),
        ("Obrazek", {
            "fields": ("obraz", "podglad_obrazka"),
        }),
        ("O święcie", {
            "fields": ("o_swiecie_pl", "o_swiecie_en"),
        }),
        ("Obrzędy", {
            "fields": ("obrzedy_pl", "obrzedy_en"),
        }),
        ("Symbolika", {
            "fields": ("symbolika_pl", "symbolika_en"),
        }),
        ("Daty systemowe", {
            "classes": ("collapse",),
            "fields": ("utworzone", "zaktualizowane"),
        }),
    )

    @admin.display(description="Podgląd")
    def podglad_obrazka(self, obj):
        if obj.obraz:
            return format_html(
                '<img src="{}" style="max-height:80px;max-width:160px;'
                'object-fit:cover;border-radius:5px;"/>',
                obj.obraz.url,
            )
        return "—"
