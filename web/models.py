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

    SECOND = 'Second'
    CYCLE = 'Cycle'
    MEASUREMENT_TYPE_CHOICES = [
        (SECOND, SECOND),
        (CYCLE, CYCLE),
    ]

    name = models.CharField(
        max_length=30,
        choices=EXERCISE_CHOICES,
        default=PUSHUP,
    )

    measurement_type = models.CharField(
        max_length=30,
        choices=MEASUREMENT_TYPE_CHOICES,
        default=CYCLE,
    )

    def __str__(self):
        return self.name


class ExerciseSet(models.Model):
    datetime_performed = models.DateTimeField()
    measurement = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    performed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exercise_performed = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return (f'{self.performed_by} did '
                f'{self.exercise_performed.name} '
                f'{self.measurement} {self.exercise_performed.measurement_type} on '
                f'{self.datetime_performed}')
