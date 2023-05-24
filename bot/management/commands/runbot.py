from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient, logger
from bot.tg.schemas import Message


class Command(BaseCommand):
    """Основная логика работы бота"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()

    def handle(self, *args, **options):
        offset = 0

        logger.info('Bot start handling')
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)


    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(chat_id=msg.chat.id)
        # self.tg_client.send_message(chat_id=msg.chat.id, text=msg.text)

        #Смотрим ест ли пользователь в базе и зарегигтрирован ли он
        if tg_user.user: #если польователь из чата связан с нашим пользователем (он уже есть в базе)
            self.handle_authorized_user(tg_user, msg)
        else: #отправяляем ему верификационный код
            self.handle_unauthorized_user(tg_user, msg)

        def handle_authorized_user(self, tg_user: TgUser, msg: Message):
            """Обрабатывает запросы авторизованного пользователя"""
            self.tg_client.send_message(chat_id=msg.chat.id, text=f'Hello {tg_user.user.username}')

        def handle_unauthorized_user(self, tg_user: TgUser, msg: Message):
            """Высылает верификационный код не авторизованному пользователю и записывает его в базу"""
            code = tg_user.generate_verification_code()
            tg_user.verification_code = code
            tg_user.save()

            self.tg_client.send_message(chat_id=msg.chat.id, text=f'Hello! Verification code: {code}')

