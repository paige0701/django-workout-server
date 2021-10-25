from django.urls import path
from . import views

urlpatterns = [
    path('', views.WorkoutListView.as_view()),
    path('<slug:pk>/', views.WorkoutDetailView.as_view())
]
