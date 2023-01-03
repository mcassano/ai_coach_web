from django.db import models
from django.contrib.auth.models import User


class Exercise(models.Model):
    PUSHUP = 'Push-up'
    FLAPPINGCROSS = 'Flapping-Cross'
    EXERCISE_CHOICES = [
        (PUSHUP, PUSHUP),
        (FLAPPINGCROSS, FLAPPINGCROSS),
    ]
    exercise = models.CharField(
        max_length=30,
        choices=EXERCISE_CHOICES,
        default=PUSHUP,
    )

    def __str__(self):
        return self.exercise


class Workout(models.Model):
    datetime_performed = models.DateTimeField()
    num_sets = models.IntegerField()
    num_reps = models.IntegerField()
    performed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_performed = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.performed_by} did {self.exercise_performed.exercise} {self.num_sets}X{self.num_reps} on {self.datetime_performed}'