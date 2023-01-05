from django.test import TestCase
from web.models import Exercise, Workout
from accounts.models import CustomUser
from django.utils import timezone


class WorkoutTestCase(TestCase):
    def setUp(self):
        Exercise.objects.create(name=Exercise.PUSHUP)
        Exercise.objects.create(name=Exercise.FLAPPINGCROSS)
        CustomUser.objects.create(username="tom")

    def test_workout_is_created_successfully(self):
        """Create a workout with an Exercise and CustomUser"""
        push_up = Exercise.objects.get(name=Exercise.PUSHUP)
        exerciser = CustomUser.objects.get(username="tom")

        workout = Workout.objects.create(datetime_performed=timezone.now(),
                                         num_sets=3,
                                         num_reps=10,
                                         performed_by=exerciser,
                                         exercise_performed=push_up)

        actual = Workout.objects.get(performed_by=exerciser)
        self.assertEqual(10, actual.num_reps)
