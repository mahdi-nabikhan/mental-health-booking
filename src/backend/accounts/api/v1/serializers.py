from ...models import User,Therapist,Patient
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class UserRegisterSerializer(serializers.ModelSerializer):
    confrim_password = serializers.CharField(write_only =True)
    class Meta :
        model = User
        fields = ['email','password',"confrim_password"]
        extra_kwargs = {
            'password' : {'write_only':True}
        }
        
        
    def validate(self, attrs):
        password  = attrs.get('password')
        confrim_password = attrs.get('confrim_password')
        if password !=  confrim_password :
            msg = _("password most be match")
            raise serializers.ValidationError(msg , code="invalid password")
        try:
            validate_password(password=password)
        
        
        except ValidationError as e:
            raise serializers.ValidationError({'password':e.message})
        return attrs
    
    
    def create(self, validated_data):
        validated_data.pop('confrim_password')
        return User.objects.create_user(**validated_data)
    

class TherapistRegisterSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = Therapist
        fields = [
            "user",
            "first_name",
            "last_name",
            "phone_number",
        ]

    def validate(self, attrs):
        password = attrs["user"]["password"]

        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({
                "user": {
                    "password": e.messages
                }
            })

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop("user")

        user = User.objects.create_user(
            **user_data
        )
        user_data.pop("confrim_password")
        return Therapist.objects.create(
            user=user,
            **validated_data
        )
        
class PatientRegisterSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = Patient
        fields = [
            "user",
            "first_name",
            "last_name",
            "phone_number",
        ]

    def validate(self, attrs):
        password = attrs["user"]["password"]

        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({
                "user": {
                    "password": e.messages
                }
            })

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop("user")

        user = User.objects.create_user(
            **user_data
        )

        return Patient.objects.create(
            user=user,
            **validated_data
        )
    




    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError(
                "Old password is incorrect."
            )

        return value

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if new_password != confirm_password:
            raise serializers.ValidationError({
                "confirm_password": "Passwords must match."
            })

        try:
            validate_password(new_password, self.context["request"].user)
        except ValidationError as e:
            raise serializers.ValidationError({
                "new_password": e.messages
            })

        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])

        return user
    
    
    

class UserSerializers (serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ['email',"id"]
        
        
        
class TherapistSerializers(serializers.ModelSerializer):
    class Meta :
        model = Therapist
        fields = "__all__"
        read_only_fields = ['user',"id"]
        
        
    def to_representation(self, instance):
        res =  super().to_representation(instance)
        res['user'] =  UserSerializers(instance.user).data
        return res
    
    
    
class PatientSerializers(serializers.ModelSerializer):
    class Meta :
        model = Patient
        fields = "__all__"
        read_only_fields = ['user',"id"]
        
        
    def to_representation(self, instance):
        res =  super().to_representation(instance)
        res['user'] =  UserSerializers(instance.user).data
        return res
    
    
    
    
class CustomObtainPairTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        res = super().validate(attrs)
        res['email'] = self.user.email
        res["user_id"] = self.user.id
        return res