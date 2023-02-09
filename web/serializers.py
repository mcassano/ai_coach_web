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
    num_reps = serializers.IntegerField()
    exercise_performed = ExerciseSerializer()
    performed_by = CustomUserSerializer(read_only=True)
    duration_seconds = serializers.IntegerField()

    def create(self, validated_data):
        exercise_name = validated_data["exercise_performed"]["name"]
        exercise = Exercise.objects.get(name=exercise_name)
        exercise_set = ExerciseSet(datetime_performed=validated_data["datetime_performed"],
                              num_reps=validated_data["num_reps"],
                              exercise_performed=exercise,
                              performed_by=validated_data["user"],
                              duration_seconds=validated_data["duration_seconds"]
                              )
        exercise_set.save()
        return exercise_set

    def update(self, instance, validated_data):
        instance.datetime_performed = validated_data.get('datetime_performed', instance.datetime_performed)
        instance.num_reps = validated_data.get('num_reps', instance.num_reps)
        instance.duration_seconds = validated_data.get('duration_seconds', instance.duration_seconds)
        instance.save()
        return instance
