from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from web import views

router = routers.DefaultRouter()
router.register(r'exercises', views.ExerciseViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.simple.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('exercise-sets/', views.exercise_set_controller),
]
