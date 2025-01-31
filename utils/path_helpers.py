import os
from datetime import datetime

from django.utils.text import slugify


def article_cover_path(instance, filename):
    """
    Генерирует путь для сохранения обложки статьи.
    Формат: articles/covers/<article_title>_<datetime>/<filename>
    """
    # Генерируем имя папки на основе заголовка статьи и текущей даты
    folder_name = (
        f"{slugify(instance.title)}_{datetime.now().strftime('%Y%m%d')}"
    )
    # Возвращаем полный путь
    return os.path.join("articles/covers", folder_name, filename)
