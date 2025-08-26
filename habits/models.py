from django.db import models
from datetime import timedelta

from location_field.models.plain import PlainLocationField

from users.models import Users


class Habits(models.Model):
    """Модель 'Привычки'"""

    user = models.ForeignKey(
        Users,
        max_length=30,
        help_text="Выберите пользователя",
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    place = models.CharField(
        max_length=255,
        help_text='Введите название места',
        verbose_name="Место"
    )
    map = PlainLocationField(
        based_fields=['city'],
        zoom=7,
        verbose_name="Карта и координаты"
    )
    time = models.DateTimeField(
        max_length=30,
        help_text="Укажите время",
        verbose_name="Время"
    )
    action = models.CharField(
        max_length=30,
        help_text="Укажите действие",
        verbose_name="Действие"
    )
    sign_of_a_pleasant_habit = models.BooleanField(
        help_text="Укажите, является ли данная привычка приятной",
        verbose_name="Приятная привычка"
    )
    related_habit = models.CharField(
        max_length=200,
        verbose_name="Связанная привычка",
        help_text="Название связанной приятной привычки",
        null=True,
        blank=True
    )
    periodicity = models.DurationField(
        help_text="Укажите период времени в формате ЧЧ:ММ:СС",
        verbose_name="Период",
        default=timedelta(hours=00, minutes=00, seconds=00)
    )
    reward = models.TextField(
        max_length=300,
        help_text="Напишите какое вознаграждение после выполнения",
        null=True,
        blank=True,
        verbose_name="Вознаграждение"
    )
    time_to_complete = models.DurationField(
        help_text="Укажите время на выполнение привычки в формате ЧЧ:ММ:СС",
        verbose_name="Время на выполнение",
        default=timedelta(hours=00, minutes=00, seconds=00)
    )
    sign_of_publicity = models.BooleanField(
        help_text="Укажите, нужно ли опубликовать привычку",
        verbose_name="Опубликовать"
    )

    def __str__(self):
        return self.action

    class Meta:
        ordering = [
            "action",
            "related_habit",
            "user",
            "place",
            "time"
        ]
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
