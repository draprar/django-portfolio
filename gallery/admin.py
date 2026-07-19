from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Gallery, InstagramPost, InstagramPostMedia


class InstagramPostMediaInline(admin.TabularInline):
    """
    Lets an admin attach one or several photos/reels to a single
    InstagramPost directly from the post's admin page.
    """

    model = InstagramPostMedia
    extra = 1
    fields = ["image", "video", "order", "preview"]
    readonly_fields = ["preview"]

    def preview(self, obj):
        if obj.pk and obj.video:
            return format_html(
                '<video src="{}" muted style="height: 80px; border-radius: 6px;"></video>', obj.video.url
            )
        if obj.pk and obj.image:
            return format_html('<img src="{}" style="height: 80px; border-radius: 6px;" />', obj.image.url)
        return "-"

    preview.short_description = "Preview"


@admin.register(InstagramPost)
class InstagramPostAdmin(admin.ModelAdmin):
    list_display = ["__str__", "category", "location", "created_at"]
    list_filter = ["category"]
    ordering = ["-created_at"]
    inlines = [InstagramPostMediaInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "order"]
    list_editable = ["order"]
    ordering = ["order", "title"]


admin.site.register(Gallery)