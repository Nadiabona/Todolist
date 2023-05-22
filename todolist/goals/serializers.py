from __future__ import annotations

from datetime import date

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework import serializers

from todolist.core.models import User
from todolist.core.serializers import ProfileSerializer
from todolist.goals.models import GoalCategory, Goal, Board, BoardParticipant
from todolist.goals.admin import GoalComment

class BoardSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated", "is_deleted")
        fields = "__all__"

class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.editable_roles)
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all())

    #добавляем валидатор на то, что юзер не может изменить себе роль
    def valiadate_user(self, user: User) ->  User:
        if self.context['request']== user:
            raise ValidationError('Role change is not allowed')
        return user

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")

class BoardWithParticipantsSerializer(BoardSerializer):
    participants = BoardParticipantSerializer(many=True)

    #дальше нам надо написать обновление списка пользователей доски, будем просто всех удалять кроме владельца и добавлять навый
    #в описании проедложен вариант сложнее

    def update(self, instance:Board, validated_data: dict) -> Board:
        request = self.context['request']
        # удаляем всех участников кроме владельца
        with transaction.atomic():
            BoardParticipant.objects.filter(board=instance).exclude(user=requests.user).delete()
            BoardParticipant.objects.bulk_create(
                [
                    BoardParticipant(user=participant['user'], role=participant['role'], board=instance)
                    for participant in validated_data.get('participants', [])
                ],
                ignore_conflicts=True,
            )

              # если title в запросе)
            if title := validated_data.get('title'):
                instance.title = title
            instance.save()
        return instance


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    #в джанго в дефолт хидден юзер можно забирать только не в методаз put patch
    #'поле, которое не видит юзер, видим мы, чтобы удобно было работать с контекстом запроса

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "is_deleted")

        def validate_board(self, board : Board)-> Board:
            #не стерта ли доска
            if board.is_deleted:
                raise ValidationError('Board is deleted')
            #проверяем, что пользователь имеет право создавать категорию на доске
            if not BoardParticipant.objects.filter(
                    board_id = board.id,
                    user_id = self.context['request'].user.id,
                    role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer, ]
             ).exists():
                raise PermissionDenied

            return board



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

        if not BoardParticipant.objects.filter(
                board_id=value.board.id,
                user_id=self.context['request'].user.id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exists():
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
        read_only_fields = ("id", "created", "updated", "user")

    def validate_goal(self, value: Goal):
        if value.status == Goal.Status.archived:
            raise ValidationError('Goal not found')
        if not BoardParticipant.objects.filter(
                board_id=value.category.board_id,
               #user_id=self.context['request'].user_id,
                user=self.context["request"].user,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],

        ).exists():
            raise PermissionDenied
        return value

class GoalCommentSerializer(GoalCommentCreateSerializer):
    user = ProfileSerializer(read_only=True)
    #goal= serializers.PrimaryKeyRelatedField(queryset=Goal.objects.all())

    class Meta:
        model = GoalComment
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'
