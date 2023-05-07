from django.db import models
from django.utils import timezone

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


class GoalCategory(BaseModel):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    def __str__(self) -> str:
        return self.title

