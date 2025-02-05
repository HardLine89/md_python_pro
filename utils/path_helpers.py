import os
from datetime import datetime

from django.utils.text import slugify


def article_cover_path(instance, filename):
    """
    Генерирует путь для сохранения обложки статьи.
    Формат: articles/covers/<article_title>_<datetime>/<filename>
    """
    # Генерируем имя папки на основе заголовка статьи и текущей даты
    folder_name = f"{slugify(instance.title)}_{datetime.now().strftime('%Y%m%d')}"
    # Возвращаем полный путь
    return os.path.join("articles/covers", folder_name, filename)


def profile_avatar_path(instance, filename):
    """
    Генерирует путь для сохранения аватарки пользователя.
    Формат: users/avatars/<username>_<datetime>/filename
    """
    # Генерируем имя папки на основе username и текущей даты
    folder_name = (
        f"{slugify(instance.user.username)}_{datetime.now().strftime('%Y%m%d')}"
    )
    # Возвращаем полный путь
    return os.path.join("users/avatars", folder_name, filename)
