from django.db import models
from accounts.models import Patient, Therapist
from django.db import models
from django.db.models import Q


class AppointmentSlot(models.Model):
    therapist = models.ForeignKey(
        Therapist,
        on_delete=models.CASCADE,
        related_name="appointment_slots",
    )
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["therapist", "date", "time"],
                name="unique_therapist_slot",
            )
        ]


class Appointment(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    slot = models.ForeignKey(
        AppointmentSlot,
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["slot"],
                condition=~Q(status="cancelled"),
                name="unique_active_appointment_per_slot",
            )
        ]

