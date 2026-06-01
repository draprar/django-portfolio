from django.contrib import admin
from django.utils.html import format_html

from .models import Contact, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title_en", "title_pl", "github_url", "live_url", "created_at", "admin_image_preview")
    search_fields = ("title_en", "title_pl")
    readonly_fields = ("admin_image_preview",)

    @admin.display(description="Preview")
    def admin_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px; max-width:200px; object-fit:contain;"/>', obj.image.url
            )
        return "-"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "submitted_at", "message_preview")
    list_filter = ("submitted_at",)
    search_fields = ("name", "email")
    readonly_fields = ("name", "email", "message", "submitted_at")
    date_hierarchy = "submitted_at"

    @admin.display(description="Message Preview", empty_value="-")
    def message_preview(self, obj):
        # Display first 100 characters of the message
        return obj.message[:100] + "..." if len(obj.message) > 100 else obj.message

    def has_add_permission(self, request):
        # Prevent manual addition—only form submissions should create Contact records
        return False

    def has_delete_permission(self, request, obj=None):
        # Allow deletion only for admins
        return request.user.is_superuser
