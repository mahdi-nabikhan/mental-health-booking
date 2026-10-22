from django.urls import path

from .views import (
    FAQListAPIView,
    FAQCreateAPIView,
    FAQDetailAPIView,
)

app_name = "faq"

urlpatterns = [
    path("", FAQListAPIView.as_view(), name="faq-list"),
    path("create/", FAQCreateAPIView.as_view(), name="faq-create"),
    path("<int:pk>/", FAQDetailAPIView.as_view(), name="faq-detail"),
]