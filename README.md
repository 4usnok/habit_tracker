# SPA веб-приложения: трекер привычек

Приложение для работы с Telegram и рассылками напоминаний

SPA веб-приложение, где бэкенд-сервер возвращает клиенту JSON-структуры. 
LMS-система, в которой каждый желающий может размещать свои полезные материалы или курсы.

# Инструкция по установке и использованию разработанного функционала приложения
1. Клонируйте репозиторий:
```
git clone https://github.com/4usnok/Project_5_Habit_tracker.git
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
# Содержание проекта
## Приложение `habits`
1. `models.py`:
* Модель привычки -> `Habit`
2. `pagination.py`:
* Пагинация с количеством элементов на страницу 5 -> `HabitPagination`
3. `permissions.py`:
* Пользовательское разрешение, разрешающее владельцу только доступ -> `IsOwner`
4. `serializers.py`:
* Сериализатор для валидации КРУД -> `HabitValidSerializer`
* Сериализатор для привычки -> `HabitSerializer`
5. `services.py`:
* Преобразования сообщения -> `send_tg_message`
6. `tasks.py`:
* Для post-запроса в ТГ -> `get_info`
7. `validators.py`:
* Валидатор для проверки, что заполнено только одно из полей -> `RewardOrRelatedHabitValidator`
* Валидатор для проверки, что время выполнения должно быть не больше 120 секунд -> `FillTimeValidator`
* Валидатор для проверки, попадание в связанные привычки только привычек с признаком приятной привычки -> 
`PleasantHabitInRelatedHabitValidator`
* Валидатор для проверки, что у приятной привычки не может быть вознаграждения или связанной привычки ->
`PleasantHabitValidator`
* Валидатор для проверки, что нельзя выполнять привычку реже, чем 1 раз в 7 дней -> 
`NumberOfHabitsCompletedValidator`
8. `views.py`:
* Пагинация -> `MyView`
* Просмотр списка привычек владельца -> `ListPrivateAPIViewPermissions`
* Просмотр публичного списка владельца -> `ListPublicAPIViewPermissions`
* Создание постов -> `CreateAPIViewPermissions`
* Пользователь имеет право просматривать только свои посты -> `RetrieveAPIViewPermissions`
* Пользователь имеет право редактировать только свои посты -> `UpdateAPIViewPermissions`
* Пользователь имеет право удалять только свои посты -> `DestroyAPIViewPermissions`
9. `tests.py`:
* Файл для тестов

## Приложение `users`
Приложение предназначенное для работы с пользователями
1. `models.py`:
* Модель пользователя `User`
2. `serializers.py`:
* Сериализатор для модели `User` -> `RegistrationSerializer`
* Сериализатор для работы с токеном -> `MyTokenObtainPairSerializer`
3. `views.py`:
* `CreateUser` -> Создание/регистрация пользователя
* `UsersListAPIView` -> Просмотр списка пользователей
* `RetrieveUserAPIView` -> Просмотр конкретного пользователя
* `MyTokenObtainPairView` -> Получение JWT-токена
* `my_protected_view` -> Валидация авторизации
4. Содержит `tests.py`:
* Файл для тестов

## Прочие файлы
1. `telegram_bot.py` -> содержит функционал для работы с телеграм-ботом
2. `requirements.txt` -> список зависимостей
3. `README.md` -> описание проекта
4. `env.sample.txt` -> Заполняется в первую очередь(предназначен для заполнений host, port, пароля от бд, названия бд и тд.)
5. `redis` -> директория с брокером redis

# Работа с программой
1. Чтобы осуществить работу с телеграм ботом, необходимо выполнить следующие шаги:
* Запустить redis-сервер: `./redis-server.exe`
* Запустить worker: `celery -A config worker -l INFO`
* Запуск бота происходит из корня проекта: `python telegram_bot.py`
2. Запуск сервера осуществляется командой: `python manage.py runserver`

# Полезные команды
* Запуск сервера: `python manage.py runserver`,
* Создание суперюзера(админка): `python manage.py createsuperuser`,
* Создание миграций: `python manage.py makemigrations`,
* Сохранение миграций: `python manage.py migrate`,
* Откат всех миграций: `python manage.py migrate name_migration`, где `name_migration` -> название миграции.
* Создание фикстуры для модели пользователей `User`: `python -Xutf8 manage.py dumpdata users.User --output users_fixture.json --indent 4`
* Создание фикстуры для модели платежей `Payments`: `python -Xutf8 manage.py dumpdata users.Payments --output payments_fixture.json --indent 4`
* Создания файла с покрытием `.coverage`: `coverage run --source='.' manage.py test`
* Посмотреть покрытие unit-тестами: `coverage report`
* Запуск обработчика очереди (worker) для получения задач и их выполнения: `celery -A config worker -l INFO`
* Запуск redis-server: `./redis-server.exe`
* Запуск redis-cli: `./redis-cli.exe`