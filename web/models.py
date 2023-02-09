from django.db import models
from accounts.models import CustomUser


class Exercise(models.Model):
    PUSHUP = 'Push-up'
    FLAPPINGCROSS = 'Flapping-Cross'
    PLANK = 'Plank'

    EXERCISE_CHOICES = [
        (PUSHUP, PUSHUP),
        (FLAPPINGCROSS, FLAPPINGCROSS),
        (PLANK, PLANK)
    ]
    name = models.CharField(
        max_length=30,
        choices=EXERCISE_CHOICES,
        default=PUSHUP,
    )

    def __str__(self):
        return self.name


class ExerciseSet(models.Model):
    datetime_performed = models.DateTimeField()
    num_reps = models.IntegerField()
    performed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exercise_performed = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    duration_seconds = models.IntegerField()

    def __str__(self):
        return (f'{self.performed_by} did '
                f'{self.exercise_performed.name} '
                f'{self.num_reps} time(s) for '
                f'{self.duration_seconds} seconds on '
                f'{self.datetime_performed}')
