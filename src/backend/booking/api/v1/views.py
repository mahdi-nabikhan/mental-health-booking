from rest_framework import generics,status,response

from django.utils import timezone
from rest_framework import generics

from .serializers import *
from booking import models
from .paginations import *

class ListCreateAppointmentSlotApiView(generics.GenericAPIView):
    serializer_class = AppointmentSlotSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        return models.AppointmentSlot.objects.filter(appointment__isnull=True).order_by("date","time","id",)

    def get(self, request):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)

        serializer = self.serializer_class(
            page,
            many=True,
            context={"request": request},
        )

        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )

        if serializer.is_valid():
            serializer.save()

            return response.Response(
                {"message": "Appointment Slot successfully created"},
                status=status.HTTP_200_OK,
            )

        return response.Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
        
        
class RetriveDeleteUpdateAppointmentSlotApiView(generics.GenericAPIView):
    serializer_class = AppointmentSlotSerializer

    def get_object(self, pk):
        try:
            return models.AppointmentSlot.objects.get(
                therapist__user=self.request.user,
                pk=pk,
            )
        except models.AppointmentSlot.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk)

        if obj is None:
            return response.Response(
                {"message": "Can't find any appointment slot with this id."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(
            instance=obj,
            context={"request": request},
        )

        return response.Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        obj = self.get_object(pk)

        if obj is None:
            return response.Response(
                {"message": "Can't find any appointment slot with this id."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(
            instance=obj,
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        obj = self.get_object(pk)

        if obj is None:
            return response.Response(
                {"message": "Can't find any appointment slot with this id."},
                status=status.HTTP_404_NOT_FOUND,
            )

        obj.delete()

        return response.Response(
            {"message": "Appointment slot deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
        
        
        
class AppointmentListApiView(generics.GenericAPIView):
    serializer_class = AppointmentSerializer

    def get(self, request):
        appointments = models.Appointment.objects.filter(
            patient__user=request.user
        )

        serializer = self.serializer_class(
            appointments,
            many=True,
            context={"request": request},
        )

        return response.Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request, pk):
        serializer = self.serializer_class(
            data=request.data,
            context={
                "request": request,
                "pk": pk,
            },
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
        
        
        
class RetrieveUpdateDeleteAppointmentApiView(generics.GenericAPIView):
    serializer_class = AppointmentSerializer

    def get_object(self, pk):
        try:
            return models.Appointment.objects.get(
                patient__user=self.request.user,
                pk=pk,
            )
        except models.Appointment.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk)

        if obj is None:
            return response.Response(
                {"message": "Appointment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(
            instance=obj,
            context={"request": request},
        )

        return response.Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        obj = self.get_object(pk)

        if obj is None:
            return response.Response(
                {"message": "Appointment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(
            instance=obj,
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        obj = self.get_object(pk)

        if obj is None:
            return response.Response(
                {"message": "Appointment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        obj.delete()

        return response.Response(
            {"message": "Appointment deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
    
            
            

class TodayAppointmentApiView(generics.GenericAPIView):
    serializer_class = AppointmentSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        return (
            models.Appointment.objects
            .filter(
                slot__date=timezone.localdate(),
                slot__therapist__user=self.request.user,
            )
            .select_related(
                "slot",
                "slot__therapist",
                "patient",
            )
            .order_by(
                "slot__time",
                "id",
            )
        )

    def get(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        serializer = self.serializer_class(
            page,
            many=True,
            context={"request": request},
        )

        return self.get_paginated_response(serializer.data)