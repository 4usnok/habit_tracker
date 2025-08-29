from django.contrib import admin
from django.urls import path, include
from habits.views import telegram_webhook  # Импортируйте вашу view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("habits/", include("habits.urls", namespace="habits")),
    path("users/", include("users.urls", namespace="users")),
    path('telegram-webhook/', telegram_webhook, name='telegram_webhook'),
]
