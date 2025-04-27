import jwt
import requests
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from . import serializers
from users.models import User
from config import settings


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PrivateUser(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError("Password needed")
        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)  # type: ignore
            user.save()  # type: ignore
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):
    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, username):
        user = self.get_user(username)
        serializer = serializers.TinyUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError


class SignUp(APIView):
    def post(self, request):
        serialzer = serializers.SignUpSerializer(data=request.data)
        if serialzer.is_valid():
            user = User.objects.create(
                username=request.data["username"],
                name=request.data["name"],
                email=request.data["email"],
            )
            user.set_password(raw_password=request.data["password"])
            user.save()
            login(request, user)
            return Response({"ok": "success"}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serialzer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "Welcome"})
        else:
            return Response({"error": "Wrong username or password"})


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "Bye bye"})


class JWTLogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "Wrong username or password"})


class GithubLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id={settings.GH_ID}&client_secret={settings.GH_SECRET}",
                headers={"Accept": "application/json"},
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://api.github.com/user",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            print(access_token)
            user_data = user_data.json()
            # [x] print(user_data)
            print(user_data)
            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            user_emails = user_emails.json()
            # [x] print(user_emails)
            print(user_emails)
            # [x]check email is verified
            verified_user_emails = [
                email for email in user_emails if email.get("verified", True)
            ]
            # [x] print(verified_user_emails)
            print(verified_user_emails)
            if len(verified_user_emails) == 0:
                raise ParseError("No verified email found")
            try:
                user = User.objects.get(username=f"github_{user_data.get('id')}")
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                # * check if name exists, other option: raise ParseError
                # checked_name = user_data.get("name")
                # print(checked_name)
                # if checked_name == None:
                #     checked_name = "Add your name"
                # print(checked_name)
                user = User.objects.create(
                    username=f"github_{user_data.get('id')}",
                    email=user_emails[0].get("email"),
                    name=user_data.get("login"),
                    avatar=user_data.get("avatar_url"),
                )
                print("before password")
                # no need password because this user only log in through github
                # can use '.has_usable_password' to check
                user.set_unusable_password()
                user.save()
                print("user created")
                login(request, user)
                print("user log in yes")
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class KakaoLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                f"https://kauth.kakao.com/oauth/token",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
                },
                data={
                    "grant_type": "authorization_code",
                    "client_id": settings.KAKAO_ID,
                    "redirect_uri": "https://sueweetstay.com/social/kakao",
                    "code": code,
                },
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            user_data = user_data.json()
            # set id as username because nickname is not unique
            username = f"kakao_{user_data.get('id')}"
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                user = User.objects.get(username=username)
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                # email is not available for this login but just add checking code for practice
                checked_email = profile.get("email")
                if checked_email == None:
                    checked_email = "Add@your.email"
                user = User.objects.create(
                    username=username,
                    email=checked_email,
                    name=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                )
                # no need password because this user only log in through github
                # can use '.has_usable_password' to check
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
