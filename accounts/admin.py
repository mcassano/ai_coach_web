from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, CustomUserAPIKey
from rest_framework_api_key.admin import APIKeyModelAdmin


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username",]


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(CustomUserAPIKey)
class CustomUserAPIKeyModelAdmin(APIKeyModelAdmin):
    pass
