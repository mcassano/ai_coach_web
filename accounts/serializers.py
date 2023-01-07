from accounts.models import CustomUser
from rest_framework import serializers


class CustomUserSerializer(serializers.Serializer):
    username = serializers.CharField()

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance
