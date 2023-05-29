from typing import Callable

import pytest
from django.urls import reverse
from rest_framework import status

from todolist.goals.models import BoardParticipant


@pytest.fixture()
def goal_create_data(faker) -> Callable:
    def _wrapper(**kwargs) -> dict:
        data = {'title': faker.sentence(2)}
        data |= kwargs
        return data

    return _wrapper


@pytest.mark.django_db()
class TestGoalCreateView:
    url = reverse('goals:create-goal')

    def test_auth_required(self, client, goal_create_data):
        """Ошибка создания цели неавторизованным пользователем"""
        response = client.post(self.url, data=goal_create_data())

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_goal_auth_user(self, user, board, auth_client, goal_category, goal_create_data):
        """Авторизованный пользователь может создавать категорию"""
        BoardParticipant.objects.create(board=board, user=user)

        response = auth_client.post(self.url, data=goal_create_data(category=goal_category.id))

        assert response.status_code == status.HTTP_201_CREATED
