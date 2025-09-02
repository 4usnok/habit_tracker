from datetime import timedelta

from django.db import models
from location_field.models.plain import PlainLocationField

from users.models import User


class Habit(models.Model):
    """Модель 'Привычка'"""

    owner = models.ForeignKey(
        User,
        help_text="Владелец объекта",
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="owners_habit",  # Уникальное имя для обратной связи FK
    )
    user = models.ForeignKey(
        User,
        help_text="Выберите пользователя",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="users_habit",  # Уникальное имя для обратной связи FK
    )
    place = models.CharField(
        max_length=255, verbose_name="Место", help_text="Введите название места"
    )
    map = PlainLocationField(
        based_fields=["place"],
        zoom=7,
        null=True,
        blank=True,
        verbose_name="Карта и координаты",
    )
    time = models.TimeField(
        max_length=30, help_text="Укажите время", verbose_name="Время"
    )
    action = models.CharField(
        max_length=30, help_text="Укажите действие", verbose_name="Действие"
    )
    sign_of_a_pleasant_habit = models.BooleanField(
        help_text="Укажите, является ли данная привычка приятной",
        verbose_name="Приятная привычка",
    )
    related_habit = models.ForeignKey(
        "self",
        verbose_name="Связанная привычка",
        help_text="Название связанной приятной привычки",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    periodicity = models.DurationField(
        help_text="Укажите период времени в формате ЧЧ:ММ:СС",
        verbose_name="Период",
        default=timedelta(hours=00, minutes=00, seconds=00),
    )
    reward = models.TextField(
        max_length=300,
        help_text="Напишите какое вознаграждение после выполнения",
        null=True,
        blank=True,
        verbose_name="Вознаграждение",
    )
    time_to_complete = models.DurationField(
        help_text="Укажите время на выполнение привычки в формате ЧЧ:ММ:СС",
        verbose_name="Время на выполнение",
        default=timedelta(hours=00, minutes=00, seconds=00),
    )
    sign_of_publicity = models.BooleanField(
        help_text="Укажите, нужно ли опубликовать привычку", verbose_name="Опубликовать"
    )

    def __str__(self):
        return self.action

    class Meta:
        ordering = ["action", "place", "time"]
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
