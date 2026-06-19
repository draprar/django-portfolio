from django.contrib import admin
from django.utils.html import format_html

from .models import Swieto, ZrodloBibliograficzne


class ZrodloInline(admin.TabularInline):
    """
    Źródła bibliograficzne edytowane bezpośrednio na stronie święta.
    """
    model = ZrodloBibliograficzne
    extra = 1
    fields = ("kolejnosc", "autor", "tytul", "wydawca_rok", "url", "url_etykieta")
    ordering = ("kolejnosc",)


@admin.register(Swieto)
class SwietoAdmin(admin.ModelAdmin):
    list_display = (
        "tytul_pl", "tytul_en", "slug", "kolejnosc",
        "podglad_obrazka", "zaktualizowane",
    )
    list_editable = ("kolejnosc",)
    prepopulated_fields = {"slug": ("tytul_pl",)}
    search_fields = ("tytul_pl", "tytul_en", "slug")
    ordering = ("kolejnosc", "tytul_pl")
    readonly_fields = ("podglad_obrazka", "utworzone", "zaktualizowane")

    inlines = [ZrodloInline]

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
                '<img src="{}" style="max-height:90px; max-width:180px;'
                ' object-fit:cover; border-radius:6px;"/>',
                obj.obraz.url,
            )
        return "—"
