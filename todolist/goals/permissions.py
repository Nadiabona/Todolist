from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.request import Request

from todolist.goals.models import Goal, GoalCategory, GoalComment, Board, BoardParticipant


class BoardPermission(IsAuthenticated):
    #check access rights to Board
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: Board) -> bool:
        _filters: dict[str, Any] = {'user_id': request.user.id, 'board_id': obj.id}
        #если метод не safe то фильтруем еще и по роли
        if request.method not in SAFE_METHODS: #то есть если это get
            _filters['role'] = BoardParticipant.Role.owner
        #и плюс смотрим, есть ли он в таблице board participants
        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCategoryPermission(IsAuthenticated):
    #Category acces rights check
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: GoalCategory) -> bool:
        _filters: dict[str, Any] = {'user_id': request.user.id, 'board_id': obj.board_id}
        # если метод не safe то фильтруем еще и по роли
        if request.method not in SAFE_METHODS:  # то есть если это get
            _filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        # и плюс смотрим, есть ли он в таблице board participants
        return BoardParticipant.objects.filter(**_filters).exists()


class GoalPermission(IsAuthenticated):
    #Goal access rights permisson
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: Goal) -> bool:
        _filters: dict[str, Any] = {'user_id': request.user.id, 'board_id': obj.category.board_id}
        if request.method not in SAFE_METHODS:
            _filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]

        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCommentPermission(IsAuthenticated):
    def has_object_permission(
        self,
        request: Request,
        view: GenericAPIView,
        obj: GoalComment
) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
#