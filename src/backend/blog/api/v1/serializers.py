from rest_framework import serializers
from blog import models as blog_models
from accounts import models as account_models
from accounts.api.v1 import serializers as account_serializers


class BlogCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = blog_models.Blog
        fields = '__all__'
        read_only_fields = ['owner']

    def create(self, validated_data):
        validated_data['owner'] = account_models.Therapist.objects.get(
            user=self.context['request'].user
        )
        return super().create(validated_data)


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = blog_models.Blog
        fields = '__all__'
        read_only_fields = ['owner']

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['owner'] = account_serializers.TherapistSerializers(
            instance.owner
        ).data
        return res


class BlogStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = blog_models.Blog
        fields = ['status']