from django.test import TestCase
from web.models import Exercise, Workout
from accounts.models import CustomUser
from django.utils import timezone


class WorkoutTestCase(TestCase):
    def setUp(self):
        Exercise.objects.create(name=Exercise.PUSHUP)
        Exercise.objects.create(name=Exercise.FLAPPINGCROSS)
        CustomUser.objects.create(username='tom')

    def test_workout_is_created_successfully(self):
        """Create a workout with an Exercise and CustomUser"""
        push_up = Exercise.objects.get(name=Exercise.PUSHUP)
        exerciser = CustomUser.objects.get(username='tom')

        Workout.objects.create(datetime_performed=timezone.now(),
                               num_sets=3,
                               num_reps=10,
                               performed_by=exerciser,
                               exercise_performed=push_up)

        actual = Workout.objects.get(performed_by=exerciser)
        self.assertEqual(10, actual.num_reps)


class TestWorkoutViews(TestCase):
    def setUp(self):
        self.exercise = Exercise.objects.create(name=Exercise.PUSHUP)
        Exercise.objects.create(name=Exercise.FLAPPINGCROSS)
        user = CustomUser.objects.create(username='tom')
        user.set_password('123456')
        user.save()

        self.workout = Workout.objects.create(
            datetime_performed=timezone.now(),
            num_sets=3,
            num_reps=10,
            performed_by=user,
            exercise_performed=self.exercise)

    def test_workout_can_be_GET(self):
        """login and get a users single workout"""
        self.client.login(username='tom', password='123456')
        response = self.client.get('/workouts/',
                                   HTTP_ACCEPT='application/json')

        self.assertEqual(200,
                         response.status_code)
        self.assertEqual(1,
                         len(response.data))
        self.assertEqual(self.workout.performed_by.username,
                         response.data[0]["performed_by"]["username"])
        self.assertEqual(self.workout.num_sets,
                         response.data[0]["num_sets"])
        self.assertEqual(self.workout.num_reps,
                         response.data[0]["num_reps"])

    def test_workout_can_be_POST(self):
        """login and post a workout to a user"""
        self.client.login(username='tom', password='123456')
        the_post_data = {"exercise_performed": {"name": "Push-up"},
                         "datetime_performed": "2023-01-04T04:20:27Z",
                         "num_sets": 2,
                         "num_reps": 10}
        response = self.client.post(path='/workouts/',
                                    data=the_post_data,
                                    content_type='application/json')

        self.assertEqual(201,
                         response.status_code)
        self.assertEqual(2,
                         response.data["num_sets"])
        self.assertEqual(10,
                         response.data["num_reps"])
        self.assertEqual('Push-up',
                         response.data["exercise_performed"]["name"])
        self.assertEqual('tom',
                         response.data["performed_by"]["username"])
        self.assertEqual('2023-01-04T04:20:27Z',
                         response.data["datetime_performed"])
