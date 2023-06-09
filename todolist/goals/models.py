from django.db import models

from todolist.core.models import User

class BaseModel(models.Model):
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now_add=True)

    #мы полем auto_now_add=True заменили вот этот кусок кода

    #def save(self, *args, **kwargs):
     #   if not self.id:  # Когда объект только создается, у него еще нет id
      #      self.created = timezone.now()  # проставляем дату создания
       # self.updated = timezone.now()  # проставляем дату обновления
        #return super().save(*args, **kwargs)

    class Meta:
        abstract = True #делаем класс абстрактным он тогда не создает таблиц в базе данных

class Board(BaseModel):

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    def __str__(self):
        return self.title


class BoardParticipant(BaseModel):
    class Meta:
        unique_together = ("board", "user")#сочетание уникальное, чтобы на одной и той же доске пользователь не смог иметь несоклько ролей
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    board = models.ForeignKey(Board,verbose_name="Доска", on_delete=models.PROTECT, related_name="participants")#доска связана с участниками
    user = models.ForeignKey(User,verbose_name="Пользователь",on_delete=models.PROTECT, related_name="participants")
    role = models.PositiveSmallIntegerField(verbose_name="Роль", choices=Role.choices, default=Role.owner)

    editable_roles: list[tuple[int, str]] = Role.choices[1:] #список кортежей типа [1, Читатель]
    #все роли, которые мы можем изменять в сериализаторе
     #убираем из списко,запрещаем владельцу давать роль владельца

class GoalCategory(BaseModel):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    #для связи доски с категориями добавляем сюда доску
    board = models.ForeignKey(Board,  on_delete=models.PROTECT,related_name="categories", null=True)

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    def __str__(self) -> str:
        return self.title

class Goal(BaseModel):
    class Status(models.IntegerChoices):
        to_do = 1,'К выполнению'
        in_progress = 2, 'В процессе'
        done = 3, 'Выполнено'
        archived = 4, 'Архив'

    class Priority(models.IntegerChoices):
        low = 1, 'Низкий'
        medium = 2, 'Средний'
        high = 3, 'Высокий'
        critical = 4, 'Критичный'

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(GoalCategory, on_delete=models.PROTECT, related_name='goals')
    due_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete = models.PROTECT, related_name = 'goals')
    status = models.PositiveSmallIntegerField(choices=Status.choices, default = Status.to_do)
    priority = models.PositiveSmallIntegerField(choices = Priority.choices, default = Priority.medium)

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    def __str__(self):
        return self.title

class GoalComment(BaseModel):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comments')
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    def __str__(self) -> str:
        return self.text



