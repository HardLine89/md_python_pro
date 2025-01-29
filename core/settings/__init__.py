from .config import config  # Импортируем Pydantic-класс

for key, value in config.__dict__.items():
    if not key.startswith("_"):  # Исключаем приватные атрибуты
        globals()[key] = value
