from rest_framework import viewsets
from rest_framework import permissions
from web.serializers import WorkoutSerializer, ExerciseSerializer
from web.models import Workout, Exercise


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all().order_by('-datetime_performed')
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]
