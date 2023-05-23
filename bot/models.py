from django.db import models

from todolist.core.models import User


class TgUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    #может быть нуль если юзер в телеге не связан с приложением
    verification_code = models.CharField(max_length=100, null=True, blank=True, default=None)

    #содадим клиента бота, чтобы мы могли от него принимать и отправлять сообщения
    @staticmethod
    def generate_verification_code() -> str:
        return str(uuid4())
