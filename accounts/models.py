from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_api_key.models import AbstractAPIKey


class CustomUser(AbstractUser):
    pass
    # add additional fields in here

    def __str__(self):
        return self.username


class CustomUserAPIKey(AbstractAPIKey):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )