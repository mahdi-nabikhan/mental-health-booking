from rest_framework.permissions import BasePermission
from accounts.models import Therapist


class IsTherapist(BasePermission):
    message = "Only therapists can manage FAQs."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and Therapist.objects.filter(user=request.user).exists()
        )