from typing import Callable
from unittest.mock import ANY
import pytest
from django.urls import reverse
from rest_framework import status

from todolist.goals.models import GoalCategory, BoardParticipant


@pytest.fixture()
def category_create_data(faker) -> Callable:
    def _wrapper(**kwargs) -> dict:
        data = {'title': faker.sentence(2)}
        data |= kwargs
        return data

    return _wrapper


@pytest.mark.django_db()
class TestCategoryCreateView:
    url = reverse('goals:create-category')

    def test_auth_required(self, client, category_create_data):
        """Ошибка создания категории неавторизованным пользователем"""
        response = client.post(self.url, data=category_create_data())

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_category_auth_user(self, user, board, auth_client, category_create_data):
        """Авторизованный пользователь может создавать категорию"""
        BoardParticipant.objects.create(board=board, user=user)

        response = auth_client.post(self.url, data=category_create_data(board=board.id))

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == self._serialize_category_response(is_deleted=False)
    #
    def test_failed_to_create_deleted_category(self, auth_client, board, user, category_create_data):
        """Нельзя создавать категорию со значением is_deleted=True."""
        BoardParticipant.objects.create(board=board, user=user)

        response = auth_client.post(self.url, data=category_create_data(board=board.id, is_deleted=True))

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()==self._serialize_category_response(is_deleted=False)
        assert GoalCategory.objects.last().is_deleted is False

    def _serialize_category_response(self, **kwargs) -> dict:
        """Проверяем, что у нас весь request составлен корректно"""
        data = {'id': ANY, 'created': ANY, 'updated': ANY, 'title': ANY, 'board': ANY, 'is_deleted': False}
        data |= kwargs
        return data

