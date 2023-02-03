from web.models import ExerciseSet, Exercise
from rest_framework import serializers
from accounts.serializers import CustomUserSerializer


class ExerciseSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):
        return Exercise.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class ExerciseSetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    datetime_performed = serializers.DateTimeField()
    measurement = serializers.DecimalField(max_digits=6, decimal_places=2)
    exercise_performed = ExerciseSerializer()
    performed_by = CustomUserSerializer(read_only=True)

    def create(self, validated_data):
        exercise_name = validated_data["exercise_performed"]["name"]
        exercise = Exercise.objects.get(name=exercise_name)
        exercise_set = ExerciseSet(datetime_performed=validated_data["datetime_performed"],
                              measurement=validated_data["measurement"],
                              exercise_performed=exercise,
                              performed_by=validated_data["user"]
                              )
        exercise_set.save()
        return exercise_set

    def update(self, instance, validated_data):
        instance.datetime_performed = validated_data.get('datetime_performed', instance.datetime_performed)
        instance.measurement = validated_data.get('measurement', instance.measurement)
        instance.save()
        return instance
