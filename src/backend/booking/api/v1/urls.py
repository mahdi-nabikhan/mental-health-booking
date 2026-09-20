from django.urls import path

from . import views
app_name = "v1"

urlpatterns = [
    # Appointment Slots
    path(
        "appointment-slots/",
        views.ListCreateAppointmentSlotApiView.as_view(),
        name="appointment-slot-list-create",
    ),
    path(
        "appointment-slots/<int:pk>/",
        views.RetriveDeleteUpdateAppointmentSlotApiView.as_view(),
        name="appointment-slot-detail",
    ),

    # Appointments
    path(
        "appointments/",
        views.AppointmentListApiView.as_view(),
        name="appointment-list",
    ),
    path(
        "appointments/create/<int:pk>/",
        views.AppointmentListApiView.as_view(),
        name="appointment-create",
    ),
    path(
        "appointments/<int:pk>/",
        views.RetrieveUpdateDeleteAppointmentApiView.as_view(),
        name="appointment-detail",
    ),
    path(
    "appointments/today/",
    views.TodayAppointmentApiView.as_view(),
    name="appointment-today",),
    path(
    "create/appointment-slots/",
    views.CreateAppointmentSlotApiView.as_view(),
    name="appointment-slots",),
    path(
    "therapist/appointment-slots/",
    views.TherapistAppointmentSlotListView.as_view(),
    name="therapist-appointment-slots",
),
]