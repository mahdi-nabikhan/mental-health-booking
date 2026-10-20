
from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "published_at",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "created_at",
        "published_at",
    )

    search_fields = (
        "title",
        "description",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_per_page = 20

    fieldsets = (
        ("اطلاعات مقاله", {
            "fields": ("title", "description", "image"),
        }),
        ("وضعیت انتشار", {
            "fields": ("status", "published_at"),
        }),
        ("اطلاعات زمانی", {
            "fields": ("created_at", "updated_at"),
        }),
    )
