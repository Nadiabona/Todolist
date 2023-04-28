from typing import Any

from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.permissions import IsAuthenticated

from todolist.core.models import User
from todolist.core.serializers import (
    CreateUserSerializer, ProfileSerializer, LoginSerializer, UpdatePasswordSerializer)

@method_decorator (csrf_exempt, name='dispatch')
class SignUpView(GenericAPIView):
    serializer_class = CreateUserSerializer
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: Serializer = self.get_serializer(data=request.data)
        # то, что прислали нам в запросе
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(**serializer.data)  # чтобы в дату попал пароль, мы в сериализаторе говорим, чтоы readonly = False

        return Response(ProfileSerializer(user).data, status=status.HTTP_201_CREATED)

@method_decorator (csrf_exempt, name='dispatch')
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

@method_decorator (csrf_exempt, name='dispatch')
class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request: Request, *args, **kwargs) -> Response:
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

@method_decorator (csrf_exempt, name='dispatch')
class UpdatePasswordView(GenericAPIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response: #не patch, потому что нам надо обновить сущность полностью
        serializer: Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: User = request.user

        if not user.check_password(serializer.validated_data['old_password']):
            raise AuthenticationFailed('The rassword is not correct')

        user.set_password(serializer.validated_data['new_password'])
        user.save(update_fields = ['password'])

        return Response(serializer.data)





