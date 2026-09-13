from django.contrib import admin

from .models import AppointmentSlot, Appointment


@admin.register(AppointmentSlot)
class AppointmentSlotAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "therapist",
        "date",
        "time",
        "created_at",
    )

    list_filter = (
        "date",
        "therapist",
    )

    search_fields = (
        "therapist__first_name",
        "therapist__last_name",
        "therapist__user__email",
    )

    ordering = (
        "date",
        "time",
    )

    list_select_related = ("therapist",)

    readonly_fields = ("created_at",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "therapist",
        "date",
        "time",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "slot__date",
        "slot__therapist",
    )

    search_fields = (
        "patient__first_name",
        "patient__last_name",
        "patient__user__email",
        "slot__therapist__first_name",
        "slot__therapist__last_name",
        "slot__therapist__user__email",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "patient",
        "slot",
        "slot__therapist",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    @admin.display(description="Therapist")
    def therapist(self, obj):
        return obj.slot.therapist

    @admin.display(description="Date")
    def date(self, obj):
        return obj.slot.date

    @admin.display(description="Time")
    def time(self, obj):
        return obj.slot.time