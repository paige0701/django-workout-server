from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from user import views
from rest_framework.authtoken import views as auth_views

urlpatterns = [
    path('users', views.user_list),
    path('create/', views.create.as_view()),
    path('token/', auth_views.obtain_auth_token),
    path('kakao/login/', csrf_exempt(views.KakaoSignInView.as_view())),
    path('kakao/login/finish/', views.KakaoLogin.as_view()),
    path('google/login/', csrf_exempt(views.GoogleSignInView.as_view())),
    path('google/login/finish/', views.GoogleLogin.as_view()),
    path('logout/', views.logout_view),
    path('', include('dj_rest_auth.urls')),
]
