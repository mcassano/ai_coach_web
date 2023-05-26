from django.test import TestCase
from web.models import Exercise, ExerciseSet
from accounts.models import CustomUser, CustomUserAPIKey
from django.utils import timezone


class ExerciseSetTestCase(TestCase):
    def setUp(self):
        Exercise.objects.create(name=Exercise.PUSHUP)
        Exercise.objects.create(name=Exercise.FLAPPINGCROSS)
        CustomUser.objects.create(username='tom')

    def test_exerciseset_is_created_successfully(self):
        """Create an exerciseset with an Exercise and CustomUser"""
        push_up = Exercise.objects.get(name=Exercise.PUSHUP)
        exerciser = CustomUser.objects.get(username='tom')

        ExerciseSet.objects.create(datetime_performed=timezone.now(),
                                   num_reps=10,
                                   num_target_reps=10,
                                   performed_by=exerciser,
                                   exercise_performed=push_up,
                                   duration_seconds=34,
                                   duration_target_seconds=0)

        actual = ExerciseSet.objects.get(performed_by=exerciser)
        self.assertEqual(10, actual.num_reps)
        self.assertEqual(34, actual.duration_seconds)


class TestExerciseSetViews(TestCase):
    def setUp(self):
        self.exercise = Exercise.objects.create(name=Exercise.PUSHUP)
        Exercise.objects.create(name=Exercise.FLAPPINGCROSS)
        user = CustomUser.objects.create(username='tom')
        user.set_password('123456')
        user.save()
        key_name, self.api_key = CustomUserAPIKey.objects.create_key(name='tests', user=user)

        self.exercise_set = ExerciseSet.objects.create(
            datetime_performed=timezone.now(),
            num_reps=10,
            num_target_reps =10,
            performed_by=user,
            exercise_performed=self.exercise,
            duration_seconds=50,
            duration_target_seconds=0)

    def test_exercise_set_can_be_GET(self):
        """get a users single exercise set"""
        response = self.client.get('/exercise-sets/',
                                   HTTP_AUTHORIZATION=f'Api-Key {self.api_key}',
                                   HTTP_ACCEPT='application/json')

        self.assertEqual(200,
                         response.status_code)
        self.assertEqual(1,
                         len(response.data))
        self.assertEqual(self.exercise_set.performed_by.username,
                         response.data[0]["performed_by"]["username"])
        self.assertEqual(self.exercise_set.num_reps,
                         response.data[0]["num_reps"])
        self.assertEqual(self.exercise_set.num_target_reps,
                         response.data[0]["num_target_reps"])
        self.assertEqual(self.exercise_set.duration_seconds,
                         response.data[0]["duration_seconds"])
        self.assertEqual(self.exercise_set.duration_target_seconds,
                         response.data[0]["duration_target_seconds"])

    def test_exercise_set_can_be_POST(self):
        """post an exercise set to a user"""
        the_post_data = {"exercise_performed": {"name": "Push-up"},
                         "datetime_performed": "2023-01-04T04:20:27Z",
                         "num_reps": 10,
                         "num_target_reps": 10,
                         "duration_seconds": 12,
                         "duration_target_seconds": 0}
        response = self.client.post(path='/exercise-sets/',
                                    data=the_post_data,
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=f'Api-Key {self.api_key}')

        self.assertEqual(201,
                         response.status_code)
        self.assertEqual(10,
                         response.data["num_reps"])
        self.assertEqual(10,
                         response.data["num_target_reps"])
        self.assertEqual('Push-up',
                         response.data["exercise_performed"]["name"])
        self.assertEqual('tom',
                         response.data["performed_by"]["username"])
        self.assertEqual('2023-01-04T04:20:27Z',
                         response.data["datetime_performed"])
        self.assertEqual(12,
                         response.data["duration_seconds"])
        self.assertEqual(0,
                         response.data["duration_target_seconds"])
