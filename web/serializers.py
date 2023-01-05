from web.models import Workout, Exercise
from rest_framework import serializers


class ExerciseSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):
        return Exercise.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class WorkoutSerializer(serializers.Serializer):
    datetime_performed = serializers.DateTimeField()
    num_sets = serializers.IntegerField()
    num_reps = serializers.IntegerField()
    exercise_performed = ExerciseSerializer()

    def create(self, validated_data):
        return Workout.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.datetime_performed = validated_data.get('datetime_performed', instance.datetime_performed)
        instance.num_sets = validated_data.get('num_sets', instance.num_sets)
        instance.num_reps = validated_data.get('num_reps', instance.num_reps)
        instance.save()
        return instance



