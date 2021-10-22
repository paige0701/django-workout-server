from django.urls import path
from . import views

urlpatterns = [
    path('', views.WorkoutView.as_view())
]