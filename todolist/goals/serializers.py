from __future__ import annotations

from datetime import date
from django.utils import timezone
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework import serializers

from todolist.core.serializers import ProfileSerializer
from todolist.goals.models import GoalCategory, Goal
from todolist.goals.admin import GoalComment

class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    #в джанго в дефолт хидден юзер можно забирать только не в методаз put patch
    #'поле, которое не видит юзер, видим мы, чтобы удобно было работать с контекстом запроса

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user", "is_deleted")
        fields = "__all__"

class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    #в джанго в дефолт хидден юзер можно забирать только не в методаз put patch
    #'поле, которое не видит юзер, видим мы, чтобы удобно было работать с контекстом запроса

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user", "is_deleted")
        fields = "__all__"

class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value: GoalCategory):
        if value.is_deleted:
            raise ValidationError('Category not found')

        if self.context['request'].user.id != value.user_id:
         #то есть если категория, в которой мы создаем цель не принадлежит текущему пользователю
            raise PermissionDenied
        return value #0десь мы можем отвалидировать любое поле

    def validate_due_date(self, value: date | None) -> date | None:
        if value and value < timezone.now().date():
            raise ValidationError('Failed to set due date ib the past')
        return value

class GoalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value: GoalCategory):
        if value.is_deleted:
            raise ValidationError('Category not found')

        if self.context['request'].user.id != value.user_id:
         #то есть если категория, в которой мы создаем цель не принадлежит текущему пользователю
            raise PermissionDenied
        return value #0десь мы можем отвалидировать любое поле

class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = '__all__'

    def validate_goal(self, value: Goal):
        if value.status == Goal.Status.archived:
            raise ValidationError('Goal not found')
        if self.context['request'].user.id != value.user_id:
            raise PermissionDenied
        return value

class GoalCommentSerializer(GoalCommentCreateSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalComment
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'
