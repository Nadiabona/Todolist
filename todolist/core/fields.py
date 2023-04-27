from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from typing import Any


# у нас пароль будет сразу в несокльких ручках - поэтому пропишем его здесь
class PasswordField(serializers.CharField):
    def __init__(self, **kwargs: Any) -> None:
        kwargs["style"] = {
            "style": "password"
        }  # мы тут давем html стиль, чтобы пароль был скрытым при вводе
        kwargs.setdefault("write_only", True)
        super().__init__(**kwargs)
        self.validators.append(validate_password)
