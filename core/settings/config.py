from pathlib import Path
from typing import List, ClassVar, Dict

from django.conf import global_settings
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class DjangoSettings(BaseSettings):
    DB_NAME: str = Field(env="DB_NAME", default="postgres")
    DB_USER: str = Field(env="DB_USER", default="admin")
    DB_PASS: str = Field(env="DB_PASS", default="120666")
    DB_HOST: str = Field(env="DB_HOST", default="localhost")
    DB_PORT: int = Field(env="DB_PORT", default=5432)

    SECRET_KEY: str
    DEBUG: bool = True
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    @property
    def DATABASES(self) -> Dict[str, Dict[str, str | int]]:
        """Динамически вычисляемый словарь DATABASES."""
        return {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": self.DB_NAME,
                "USER": self.DB_USER,
                "PASSWORD": self.DB_PASS,
                "HOST": self.DB_HOST,
                "PORT": self.DB_PORT,
            }
        }

    INSTALLED_APPS: List[str] = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]

    MIDDLEWARE: List[str] = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF: str = "core.urls"
    WSGI_APPLICATION: str = "core.wsgi.application"

    AUTH_PASSWORD_VALIDATORS: List[dict] = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    TEMPLATES: List[dict] = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": ["templates"],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        }
    ]

    LANGUAGE_CODE: str = "ru-ru"

    TIME_ZONE: str = "Asia/Bishkek"

    USE_I18N: bool = True

    USE_TZ: bool = True

    STATIC_URL: str = "static/"

    DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"


class Settings(DjangoSettings):
    PROJECT_NAME: str = "DM Pro"
    SENTRY_DSN: str | None = None
    TELEGRAM_BOT_TOKEN: SecretStr | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


config = Settings()
