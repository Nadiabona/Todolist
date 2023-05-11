from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import filters
from todolist.goals.filters import GoalDateFilter
from todolist.goals.models import GoalCategory, Goal
from todolist.goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, \
    GoalSerializer

class GoalCategoryCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated] #категорию может создавать только аудентифицированный пользователь
    serializer_class = GoalCategoryCreateSerializer

class GoalCategoryListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    filter_backends = [ filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ('title', 'created')
    ordering = ['title']
    search_field = ['title']

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(user=self.request.user, is_deleted=False)

class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory) -> None:
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted', ))
            #если удалили категорию, надо удалить цели
            #транасакционно - это чтобы если вторая операция прошла, а первая нет, чтобы она тоже откатилась
            #о есть либо выполнялись обе либо никакая
            instance.goals.update(status=Goal.Status.archieved)

class GoalCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]  # категорию может создавать только аудентифицированный пользователь
    serializer_class = GoalCreateSerializer

class GoalListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = GoalDateFilter
    ordering_fields = ('title', 'created')
    ordering = ['title']
    search_field = ['title', 'description']

    def get_queryset(self):
        return(
            Goal.objects.seleсt_related('user').filter(
                user=self.request.user, category__is_deleted=False)
            )

class GoalView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer

    def get_queryset(self):
        return(
            Goal.objects.seleсt_related('user').filter(user=self.request.user, category__is_deleted=False)
            ).exclude(status=Goal.Status.archieved)


    def perform_destroy(self, instance: Goal):
        instance.status = Goal.status.archived
        instance.save(update_fields= ('status',))



