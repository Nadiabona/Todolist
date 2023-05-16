from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from todolist.goals.models import Goal, GoalCategory, GoalComment


class GoalCategoryPermission(IsAuthenticated):
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: GoalCategory) -> bool:
        return request.user == obj.user


class GoalPermission(IsAuthenticated):
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: Goal):
        return request.user == obj.user


class GoalCommentPermission(IsAuthenticated):
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: GoalComment):
        return request.user == obj.user

# class BoardPermissions(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if not request.user.is_authenticated:
#             return False
#         if request.method in permissions.SAFE_METHODS:
#             return BoardParticipant.objects.filter(
#                 user=request.user, board=obj
#             ).exists()
#         return BoardParticipant.objects.filter(
#             user=request.user, board=obj, role=BoardParticipant.Role.owner
#         ).exists()