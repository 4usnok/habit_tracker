from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    """Модель `Пользователи`"""

    email = models.EmailField(
        unique=True,
        max_length=255,
        verbose_name='Email',
        help_text="Введите email пользователя"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["email"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
