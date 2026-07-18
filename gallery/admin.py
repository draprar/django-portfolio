from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Gallery, InstagramPost, InstagramPostImage


class InstagramPostImageInline(admin.TabularInline):
    """
    Lets an admin attach one or several photos to a single InstagramPost
    directly from the post's admin page.
    """

    model = InstagramPostImage
    extra = 1
    fields = ["image", "order", "preview"]
    readonly_fields = ["preview"]

    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html('<img src="{}" style="height: 80px; border-radius: 6px;" />', obj.image.url)
        return "-"

    preview.short_description = "Preview"


@admin.register(InstagramPost)
class InstagramPostAdmin(admin.ModelAdmin):
    list_display = ["__str__", "category", "location", "created_at"]
    list_filter = ["category"]
    ordering = ["-created_at"]
    inlines = [InstagramPostImageInline]


admin.site.register(Category)
admin.site.register(Gallery)