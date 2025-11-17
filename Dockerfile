# Базовый образ
FROM python:3.13-slim

# Установка системных пакетов для зависимостей
RUN apt-get update && apt-get install -y \
# Инструменты для PostgreSQL
libpq-dev \
# Компилятор
gcc \
# Заголовочные файлы Python
python3-dev \
# Очистка кэша
&& rm -rf /var/lib/apt/lists/*

# Установка poetry
RUN pip install "poetry==1.8.2"

# Выбор рабочей директории
WORKDIR /app

# Копирование зависимостей
COPY pyproject.toml poetry.lock* ./
# Изоляция виртуального окружения и установка зависимостей
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Копирование остальных файлов в контейнер
COPY . .

# Открытие порта 8000 для взаимодействия с приложением
EXPOSE 8000

# Команды для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
