from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title_pl', 'title_en', 'author', 'published_date')
    list_filter = ('published_date',)
    search_fields = ('title_pl', 'title_en', 'text_pl', 'text_en')
    fieldsets = (
        (None, {
            'fields': ('author', 'created_date', 'published_date')
        }),
        ('🇵🇱 Polska wersja', {
            'fields': ('title_pl', 'text_pl')
        }),
        ('🇬🇧 English version', {
            'fields': ('title_en', 'text_en'),
            'description': 'Pozostaw puste — wyświetli się PL jako fallback.'
        }),
    )