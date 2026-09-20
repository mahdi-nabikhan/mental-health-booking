from rest_framework import serializers
from accounts import models
from accounts.api.v1 import serializers as accounts_serializers
from booking import models




class AppointmentSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppointmentSlot
        fields = "__all__"
        read_only_fields = ['therapist']
        
    def create(self, validated_data):
        validated_data['therapist'] = models.Therapist.objects.get(user=self.context['request'].user)
        return models.AppointmentSlot.objects.create(**validated_data)
    
    
    def to_representation(self, instance):
        res= super().to_representation(instance)
        res['therapist'] = accounts_serializers.TherapistSerializers(instance.therapist).data
        return res
        
        
        
        
        
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.Appointment
        fields = "__all__"
        read_only_fields = ['slot','patient','status']
    
    def create(self, validated_data):
        validated_data['patient'] = models.Patient.objects.get(user=self.context['request'].user)
        validated_data['slot'] =  models.AppointmentSlot.objects.get(pk=self.context['pk'])
        return models.Appointment.objects.create(**validated_data)
    
    
    
    def to_representation(self, instance):
        res= super().to_representation(instance)
        res['slot'] = AppointmentSlotSerializer(instance.slot).data
        res['patient'] = accounts_serializers.PatientSerializers(instance.patient).data
        return res

    
    
    
class AllAppointmentSlotSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    appointment = serializers.SerializerMethodField()

    class Meta:
        model = models.AppointmentSlot
        fields = [
            "id",
            "date",
            "time",
            "therapist",
            "status",
            "appointment",
        ]

    def get_status(self, obj):
        if not hasattr(obj, "appointment"):
            return "available"

        return obj.appointment.status

    def get_appointment(self, obj):
        if not hasattr(obj, "appointment"):
            return None

        appointment = obj.appointment

        return {
            "id": appointment.id,
            "patient": {
                "id": appointment.patient.id,
                "first_name": appointment.patient.first_name,
                "last_name": appointment.patient.last_name,
                "phone_number": appointment.patient.phone_number,
            },
            "reason": appointment.reason,
            "status": appointment.status,
        }