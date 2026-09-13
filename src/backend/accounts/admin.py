from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Therapist, Patient


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_verified",
        "created_date",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "is_verified",
    )

    search_fields = ("email",)
    ordering = ("-created_date",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "last_login",
                    "created_date",
                    "updated_date",
                )
            },
        ),
    )

    readonly_fields = (
        "last_login",
        "created_date",
        "updated_date",
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
    )


@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "user",
        "phone_number",
    )

    search_fields = (
        "first_name",
        "last_name",
        "phone_number",
        "user__email",
    )

    list_select_related = ("user",)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "user",
        "phone_number",
    )

    search_fields = (
        "first_name",
        "last_name",
        "phone_number",
        "user__email",
    )

    list_select_related = ("user",)