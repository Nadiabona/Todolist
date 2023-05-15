# Generated by Django 4.0.1 on 2023-05-15 11:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0002_goalcomment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goalcomment',
            options={'verbose_name': 'Комментарий к цели', 'verbose_name_plural': 'Комментарии к целям'},
        ),
        migrations.AlterField(
            model_name='goalcomment',
            name='created',
            field=models.DateTimeField(verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='goalcomment',
            name='goal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='goal_comments', to='goals.goal', verbose_name='Цель'),
        ),
        migrations.AlterField(
            model_name='goalcomment',
            name='text',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='goalcomment',
            name='updated',
            field=models.DateTimeField(verbose_name='Дата последнего обновления'),
        ),
        migrations.AlterField(
            model_name='goalcomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='goal_comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]
