from rest_framework import generics
from rest_framework.permissions import AllowAny

from ...models import FAQ
from .serializers import FAQSerializer
from ...permissions import IsTherapist


class FAQListAPIView(generics.ListAPIView):
    queryset = FAQ.objects.all().order_by("-created_at")
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]


class FAQCreateAPIView(generics.CreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsTherapist]


class FAQDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]

        return [IsTherapist()]