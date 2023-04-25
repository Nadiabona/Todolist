from typing import Any

from django.contrib.auth import authenticate, login, logout
from rest_framework import status, serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.permissions import IsAuthenticated

from todolist.core.models import User
from todolist.core.serializers import (
    CreateUserSerializer,
    ProfileSerializer,
    LoginSerializer,
)


class SignUpView(GenericAPIView):
    serializer_class = CreateUserSerializer, ProfileSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: Serializer = self.get_serializer(
            data=request.data
        )  # то, что прислали нам в запросе
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            **serializer.data
        )  # чтобы в дату попал пароль, мы в сериализаторе говорим, чтоы readonly = False

        return Response(ProfileSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: Serializer = self.get_serializer(
            data=request.data
        )  # то, что прислали нам в запросе
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if not user:
            raise AuthenticationFailed

        login(request=request, user=user)

        return Response(ProfileSerializer(user).data)


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request: Request, *args, **kwargs) -> Response:
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
