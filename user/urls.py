from django.urls import path
from user import views

urlpatterns = [
    path('users', views.user_list),
    path('create/', views.create.as_view())
]
