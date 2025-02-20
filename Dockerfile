# Используем базовый образ Python
FROM python:3.12.7-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app
# Устанавливаем рабочую директорию в контейнере
WORKDIR /app
COPY . /app
# Устанавливаем зависимости для компиляции
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && apt-get clean

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы проекта
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости проекта
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi


# Открываем порт приложения
EXPOSE 8080