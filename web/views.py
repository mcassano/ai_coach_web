from rest_framework import viewsets
from rest_framework import permissions
from web.serializers import WorkoutSerializer, ExerciseSerializer
from web.models import Workout, Exercise
from accounts.models import CustomUserAPIKey
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def workout_controller(request):
    key = request.META["HTTP_AUTHORIZATION"].split()[1]
    associated_user = CustomUserAPIKey.objects.get_from_key(key).user

    if request.method == 'GET':
        workouts = Workout.objects\
            .filter(performed_by=associated_user)\
            .order_by('datetime_performed')
        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WorkoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=associated_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]
