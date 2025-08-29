from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from habits.views import telegram_webhook

urlpatterns = [
    path("admin/", admin.site.urls),
    path("habits/", include("habits.urls", namespace="habits")),
    path("users/", include("users.urls", namespace="users")),
    path('webhook/telegram/', csrf_exempt(telegram_webhook), name='telegram_webhook'),
]
