from django.urls import path

app_name = 'api/v1'
from .views import (
    JwtLoginApiView,
    TherapistRegisterApiView,
    PatientRegisterApiView,
    PatientListApiView,
    TherapistPanelPatientDetailApiView,
    PatientDetailApiView,
    TherapistDetailApiView,
    ChangePasswordApiView,
    JwtRefreshApiView,
    JwtLogoutApiView
)


urlpatterns = [
    # Authentication
    path(
        'login/',
        JwtLoginApiView.as_view(),
        name='login'
    ),

    # Register
    path(
        'therapist/register/',
        TherapistRegisterApiView.as_view(),
        name='therapist-register'
    ),
    path(
        'patient/register/',
        PatientRegisterApiView.as_view(),
        name='patient-register'
    ),

    # Patients
    path(
        'patients/',
        PatientListApiView.as_view(),
        name='patient-list'
    ),
    path(
        'therapist/patients/<int:pk>/',
        TherapistPanelPatientDetailApiView.as_view(),
        name='therapist-patient-detail'
    ),
    path(
        'patient/profile/',
        PatientDetailApiView.as_view(),
        name='patient-profile'
    ),

    # Therapist
    path(
        'therapist/profile/',
        TherapistDetailApiView.as_view(),
        name='therapist-profile'
    ),

    # Account
    path(
        'change-password/',
        ChangePasswordApiView.as_view(),
        name='change-password'
    ),
    path(
        "refresh/",
        JwtRefreshApiView.as_view(),
        name="jwt-refresh",
    ),
    path( "logout/", JwtLogoutApiView.as_view(), name="logout", ),
]