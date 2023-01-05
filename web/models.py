from django.db import models
from accounts.models import CustomUser


class Exercise(models.Model):
    PUSHUP = 'Push-up'
    FLAPPINGCROSS = 'Flapping-Cross'
    EXERCISE_CHOICES = [
        (PUSHUP, PUSHUP),
        (FLAPPINGCROSS, FLAPPINGCROSS),
    ]
    name = models.CharField(
        max_length=30,
        choices=EXERCISE_CHOICES,
        default=PUSHUP,
    )

    def __str__(self):
        return self.name


class Workout(models.Model):
    datetime_performed = models.DateTimeField()
    num_sets = models.IntegerField()
    num_reps = models.IntegerField()
    performed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exercise_performed = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.performed_by} did ' \
               f'{self.exercise_performed.name} ' \
               f'{self.num_sets}X{self.num_reps} on ' \
               f'{self.datetime_performed}'