from django.db import models

from accounts.models import Patient, Therapist


class AppointmentSlot(models.Model):
    therapist = models.ForeignKey(
        Therapist,
        on_delete=models.CASCADE,
        related_name="appointment_slots",
    )

    date = models.DateField()
    time = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.therapist} - {self.date} {self.time}"


class Appointment(models.Model):

    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    slot = models.OneToOneField(
        AppointmentSlot,
        on_delete=models.CASCADE,
        related_name="appointment",
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

    def __str__(self):
        return f"{self.patient} - {self.slot}"