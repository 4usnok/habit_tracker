from datetime import timedelta
from urllib.parse import urlparse

import responses
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.test import override_settings

from rest_framework.test import APITestCase

from habits.models import Habit
from habits.serializers import HabitValidSerializer
from habits.services import send_tg_message
from habits.tasks import get_info
from users.models import User


class MyAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com", password="testpassword"
        )
        # Аутентифицируем клиента
        self.client.force_authenticate(user=self.user)

    def test_create_api_view(self):
        """Тестирование создания новых привычек"""
        data = {
            "periodicity": "06:39:39",
            "time_to_complete": 119,
            "sign_of_publicity": True,
            "sign_of_a_pleasant_habit": True,
            "time": "06:39:39",
            "owner": self.user.id,
            "user": self.user.id,
            "action": "test_action",
            "place": "test_place",
        }

        response = self.client.post("/habits/create/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_api_view(self):
        """Тестирование просмотра одной привычки"""
        data = {
            "periodicity": timedelta(
                hours=6, minutes=39, seconds=39
            ),  # timedelta объект
            "time_to_complete": timedelta(seconds=119),  # timedelta объект
            "sign_of_publicity": True,
            "sign_of_a_pleasant_habit": True,
            "time": "06:39:39",
            "owner": self.user,
            "user": self.user,
            "action": "test_action",
            "place": "test_place",
        }
        habit = Habit.objects.create(**data)
        update_data = {"action": "new_action", "place": "new_place"}

        response = self.client.get(
            f"/habits/retrieve/{habit.id}/", data=update_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_api_view(self):
        """Тестирование редактирования одной привычки"""
        data = {
            "periodicity": timedelta(
                hours=6, minutes=39, seconds=39
            ),  # timedelta объект
            "time_to_complete": timedelta(seconds=119),  # timedelta объект
            "sign_of_publicity": True,
            "sign_of_a_pleasant_habit": True,
            "time": "06:39:39",
            "owner": self.user,
            "user": self.user,
            "action": "test_action",
            "place": "test_place",
        }
        habit = Habit.objects.create(**data)

        response = self.client.patch(
            f"/habits/update/{habit.id}/",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_api_view(self):
        """Тестирование удаления привычки"""
        data = {
            "periodicity": timedelta(
                hours=6, minutes=39, seconds=39
            ),  # timedelta объект
            "time_to_complete": timedelta(seconds=119),  # timedelta объект
            "sign_of_publicity": True,
            "sign_of_a_pleasant_habit": True,
            "time": "06:39:39",
            "owner": self.user,
            "user": self.user,
            "action": "test_action",
            "place": "test_place",
        }
        habit = Habit.objects.create(**data)

        response = self.client.delete(f"/habits/destroy/{habit.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_reward_or_related_habit_validator(self):
        """Тестирование валидатора для проверки, что заполнено только одно из полей"""
        data = {
            "periodicity": "06:39:39",
            "time_to_complete": "01:01:01",
            "sign_of_publicity": True,
            "sign_of_a_pleasant_habit": True,
            "time": "06:39:39",
            "owner": self.user,
            "user": self.user,
            "action": "test_action",
            "place": "test_place",
        }
        habit = Habit.objects.create(**data)

        test_data = {
            "periodicity": "01:01:01",
            "time_to_complete": "00:01:00",
            "sign_of_publicity": True,
            "sign_of_a_pleasant_habit": False,
            "time": "06:39:39",
            "owner": self.user.pk,
            "user": self.user.pk,
            "action": "test_action",
            "place": "test_place",
            "reward": "test",
            "related_habit": habit.pk,
        }

        with self.assertRaisesMessage(
            ValidationError,
            "В модели не должно быть заполнено одновременно и поле вознаграждения, "
            "и поле связанной привычки. Можно заполнить только одно из двух полей.",
        ):
            serializer = HabitValidSerializer(data=test_data)
            serializer.is_valid(raise_exception=True)

    def test_create_habit_with_reward_and_related_habit(self):
        """Тестирование создания привычки"""
        data = {
            "periodicity": "06:39:39",
            "time_to_complete": "01:01:01",
            "sign_of_publicity": True,
            "sign_of_a_pleasant_habit": True,
            "time": "06:39:39",
            "owner": self.user,
            "user": self.user,
            "action": "test_action",
            "place": "test_place",
        }
        habit = Habit.objects.create(**data)

        test_data = {
            "periodicity": "01:01:01",
            "time_to_complete": "00:01:00",
            "sign_of_publicity": True,
            "sign_of_a_pleasant_habit": False,
            "time": "06:39:39",
            "owner": self.user.pk,
            "user": self.user.pk,
            "action": "test_action",
            "place": "test_place",
            "reward": "test",
            "related_habit": habit.pk,
        }

        response = self.client.post(
            "/habits/create/",
            data=test_data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["non_field_errors"][0],
            "В модели не должно быть заполнено одновременно"
            " и поле вознаграждения,"
            " и поле связанной привычки. Можно заполнить только"
            " одно из двух полей.",
        )

    @override_settings(BOT_TOKEN="test_token")  # подменяем токен
    @responses.activate
    def test_send_tg_message(self):
        """Тестирование сервисной функции"""
        responses.add(
            responses.POST,
            "https://api.telegram.org/bot/test_token/sendMessage",
            json={"key": "value"},
            status=200,
        )
        send_tg_message(1, "hello")

        # проверка попыток запроса
        assert len(responses.calls) == 1
        request = responses.calls[0].request

        # Проверка результата
        parsed = urlparse(request.url)
        assert parsed.scheme == "https"
        assert parsed.netloc == "api.telegram.org"
        assert parsed.path == "/bot/test_token/sendMessage"

    def test_get_info(self):
        """Тестирование асинхронной задачи"""
        user = User.objects.create(email="test_mail@example.com", tg_chat_id=None)
        result = get_info(user.email)
        assert result == {
            "status": "error",
            "message": "У пользователя нет привычек",
            "email": user.email,
        }
