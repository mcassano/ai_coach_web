from web.models import Workout, Exercise
from rest_framework import serializers
from accounts.serializers import CustomUserSerializer
from django.utils import timezone


class ExerciseSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):
        return Exercise.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class WorkoutSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    datetime_performed = serializers.DateTimeField()
    num_sets = serializers.IntegerField()
    num_reps = serializers.IntegerField()
    exercise_performed = ExerciseSerializer()
    performed_by = CustomUserSerializer(read_only=True)

    def create(self, validated_data):
        exercise_name = validated_data["exercise_performed"]["name"]
        exercise = Exercise.objects.get(name=exercise_name)
        workout = Workout(datetime_performed=validated_data["datetime_performed"],
                          num_sets=validated_data["num_sets"],
                          num_reps=validated_data["num_reps"],
                          exercise_performed=exercise,
                          performed_by=validated_data["user"]
                          )
        workout.save()
        return workout

    def update(self, instance, validated_data):
        instance.datetime_performed = validated_data.get('datetime_performed', instance.datetime_performed)
        instance.num_sets = validated_data.get('num_sets', instance.num_sets)
        instance.num_reps = validated_data.get('num_reps', instance.num_reps)
        instance.save()
        return instance



