import requests
from allauth.socialaccount.models import SocialAccount
from django.views import View
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

BASE_URL = 'http://www.p1aner.xyz:80/'
KAKAO_CALLBACK_URI = 'api/v1/authentication/kakao/login/finish/'
GOOGLE_CALLBACK_URI = 'api/v1/authentication/google/login/finish/'


# Create your views here.
class create(CreateAPIView):
    model = User
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer


def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def logout_view(request):
    data = JSONParser().parse(request)
    refresh_token = data["refresh_token"]
    token = RefreshToken(refresh_token)
    token.blacklist()
    return JsonResponse({'msg': 'Successfully logged out'}, safe=False)


class KakaoSignInView(View):
    def post(self, request):
        try:
            data = JSONParser().parse(request)
            access_token = data['access_token']
            url = "https://kapi.kakao.com/v2/user/me"
            header = {
                'Authorization': 'Bearer {}'.format(access_token)
            }
            response = requests.get(url, headers=header).json()
            kakao_account = response.get("kakao_account")
            email = kakao_account.get("email", None)

            if email is None:
                return JsonResponse({'err_msg': 'Please allow email access'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(email=email)
                social_user = SocialAccount.objects.get(user=user)
                if social_user is None:
                    return JsonResponse({'err_msg': 'email exists but not social user'},
                                        status=status.HTTP_400_BAD_REQUEST)
                if social_user.provider != 'kakao':
                    return JsonResponse({'err_msg': 'User already exists with Google'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    # ????????? Google??? ????????? ??????
                data = {'access_token': access_token}
                accept = requests.post(
                    f"{BASE_URL}{KAKAO_CALLBACK_URI}", data=data)
                accept_status = accept.status_code
                if accept_status != 200:
                    return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
                accept_json = accept.json()
                accept_json.pop('user', None)
                return JsonResponse(accept_json)
            except User.DoesNotExist:
                data = {'access_token': access_token}
                accept = requests.post(
                    f"{BASE_URL}{KAKAO_CALLBACK_URI}", data=data)
                accept_status = accept.status_code
                if accept_status != 200:
                    return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
                accept_json = accept.json()
                accept_json.pop('user', None)
                return JsonResponse(accept_json)
        except:
            return JsonResponse({'message': 'TOKEN_INVALID'}, status=401)


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI

class GoogleSignInView(View):

    def post(self, request):
        data = JSONParser().parse(request)
        access_token = data['access_token']
        email = data['email']
        # access_token = request.headers['Authorization'].split('Bearer ')[1]
        if email is None:
            # email ????????? ?????? ???????????? ????????? ??????????????? ?????????
            pass

        try:
            user = User.objects.get(email=email)
            social_user = SocialAccount.objects.get(user=user)
            if social_user is None:
                return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
            if social_user.provider != 'google':
                return JsonResponse({'err_msg': 'User already registered with Kakao'},
                                    status=status.HTTP_400_BAD_REQUEST)
                # ????????? Google??? ????????? ??????
            data = {'access_token': access_token}
            accept = requests.post(
                f"{BASE_URL}{GOOGLE_CALLBACK_URI}", data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
            accept_json = accept.json()
            accept_json.pop('user', None)
            return JsonResponse(accept_json)
        except User.DoesNotExist:
            data = {'access_token': access_token}
            accept = requests.post(
                f"{BASE_URL}{GOOGLE_CALLBACK_URI}", data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
            accept_json = accept.json()
            accept_json.pop('user', None)
            return JsonResponse(accept_json)


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = GOOGLE_CALLBACK_URI
