from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient, logger
from bot.tg.schemas import Message
from todolist.goals.models import Goal, GoalCategory, BoardParticipant

clients = {}

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

        #Смотрим связарн ли этот пользователь с пользователем базы (есть ли он)
        if tg_user.user: #если польователь из чата связан с нашим пользователем (он уже есть в базе)
            self.handle_authorized_user(tg_user, msg)
        else: #отправяляем ему верификационный код
            self.handle_unauthorized_user(tg_user, msg)

    def process_goals(self, tg_user: TgUser, msg: Message):
        qs = Goal.objects.filter(
            category__board__participants__user=tg_user.user,
        ).exclude(status=Goal.Status.archived)

        goals = [f'{goal.id} {goal.title}' for goal in qs]

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text='No goals' if not goals else '\n'.join(goals)
        )

    def handle_authorized_user(self, tg_user: TgUser, msg: Message):
        """Обрабатывает запросы авторизованного пользователя"""
        if msg.text == '/goals':
            self.process_goals(tg_user, msg)

        elif msg.text == '/create':
            self.process_create(tg_user, msg)

        elif msg == '/cancel':
            clients.pop(tg_user.chat_id, None)

        elif tg_user.chat_id in clients:
            callback = clients[tg_user.chat_id]['next_handler']
            callback(tg_user, msg, **clients[tg_user.chat_id]['data'])



    def process_create(self, tg_user: TgUser, msg: Message):

        qs = GoalCategory.objects.filter(
            board__participants__user=tg_user.user,
            board__participants__role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exclude(is_deleted=True)

        categories = [f'{cat.id} {cat.title}' for cat in qs]

        if not categories:
            self.tg_client.send_message(chat_id=msg.chat.id, text='You have no categories')

        else:
            clients[tg_user.chat_id] = {'data': {}, 'next_handler': self.save_category}
            categories = '\n'.join(categories)
            # self.tg_client.send_message(chat_id=msg.chat.id, text=f'Select a category \n.join(categories))
            self.tg_client.send_message(chat_id=msg.chat.id, text=f'Select a category: \n{categories}')


    def save_category(self, tg_user, msg, **kwargs):
        # Проверяем что категория существует
        try:
            category = GoalCategory.objects.get(pk=msg.text)
        except GoalCategory.DoesNotExist:
            self.tg_client.send_message(chat_id=msg.chat.id, text='Category not found')

        else:
            self.tg_client.send_message(chat_id=msg.chat.id, text='Enter title of a new goal')
            clients[tg_user.chat_id]={'data': {'category': category}, 'next_handler': self.create_goal}

    def create_goal(self, tg_user, msg, **kwargs):
        category = kwargs['category']
        Goal.objects.create(title=msg.text, category=category, user=tg_user.user)

        self.tg_client.send_message(chat_id=msg.chat.id, text=f'Goal created')

        clients.pop(tg_user.chat_id, None)


    def handle_unauthorized_user(self, tg_user: TgUser, msg: Message):
        """Высылает верификационный код не авторизованному пользователю и записывает его в базу"""
        code = tg_user.generate_verification_code()
        tg_user.verification_code = code
        tg_user.save()

        self.tg_client.send_message(chat_id=msg.chat.id, text=f'Hello! Verification code: {code}')

