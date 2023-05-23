from django.core.management import BaseCommand
from bot.tg.client import TgClient, logger



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
                #чтобы бот отвечал - пишем в какой чат отправить - id берем из messsage
                self.tg_client.send_message(chat_id=item.message.chat.id, text=item.message.text )


