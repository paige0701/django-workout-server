from django.urls import path
from user import views
from rest_framework.authtoken import views as auth_views

urlpatterns = [
    path('users', views.user_list),
    path('create/', views.create.as_view()),
    path('token/', auth_views.obtain_auth_token),
    path('kakao/login/', views.kakao_login_view),
    path('kakao/login/finish/', views.KakaoLogin.as_view()),
]
