from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from todolist.fields import PasswordField
from todolist.core.models import User
from todolist.fields import PasswordField


# это мы будем отдавать
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = ("id", "username", "first_name", "last_name", "email")


class CreateUserSerializer(serializers.ModelSerializer):
    # допполя которых нет у модели пользователя
    password = PasswordField(required=True, write_only=False)
    password_repeat = PasswordField(required=True)

    class Meta:
        # эти поля мы будем отдавать
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password_repeat",
        )

    def validate(self, attrs: dict) -> dict:
        if attrs["password"] != attrs["password_repeat"]:
            raise ValidationError("Passwords do not match")
        return attrs


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
    )
    password = PasswordField(required=True)


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = PasswordField(required=True)
    new_password = PasswordField(required=True)
