from pathlib import Path
from typing import List, Dict
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

    GOOGLE_CLIENT_ID: str = Field(env="GOOGLE_CLIENT_ID", default="")
    GOOGLE_CLIENT_SECRET: str = Field(env="GOOGLE_CLIENT_SECRET", default="")
    GOOGLE_CLIENT_KEY: str = Field(env="GOOGLE_CLIENT_KEY", default="")

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
        "jazzmin",
        "taggit",
        "martor",
        "django_htmx",
        "crispy_forms",
        "crispy_bootstrap4",
        "allauth",
        "allauth.account",
        "allauth.socialaccount",
        "allauth.socialaccount.providers.google",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "blog",
        "utils",
        "ratings",
        "comments",
        "users",
    ]

    MIDDLEWARE: List[str] = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "allauth.account.middleware.AccountMiddleware",
        "django_htmx.middleware.HtmxMiddleware",
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
                    "django.template.context_processors.request",
                ],
            },
        }
    ]

    LANGUAGE_CODE: str = "ru-ru"

    TIME_ZONE: str = "Asia/Bishkek"

    USE_I18N: bool = True

    USE_TZ: bool = True

    STATIC_URL: str = "static/"
    # STATICFILES_DIRS: List[PosixPath] = [BASE_DIR / "static"]
    STATIC_ROOT: Path = BASE_DIR / "static"

    MEDIA_URL: str = "media/"
    MEDIA_ROOT: Path = BASE_DIR / "media"

    DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"

    AUTH_USER_MODEL: str = "auth.User"

    ACCOUNT_AUTHENTICATION_METHOD: str = "email"
    ACCOUNT_EMAIL_REQUIRED: bool = True
    ACCOUNT_UNIQUE_EMAIL: bool = True
    ACCOUNT_USERNAME_REQUIRED: bool = False
    ACCOUNT_USER_MODEL_USERNAME_FIELD: str | None = None

    AUTHENTICATION_BACKENDS: List[str] = [
        "django.contrib.auth.backends.ModelBackend",
        "allauth.account.auth_backends.AuthenticationBackend",
    ]

    CRISPY_ALLOWED_TEMPLATE_PACKS: str = "bootstrap4"

    CRISPY_TEMPLATE_PACK: str = "bootstrap4"

    @property
    def SOCIALACCOUNT_PROVIDERS(self) -> dict:
        return {
            "google": {
                "APP": {
                    "client_id": self.GOOGLE_CLIENT_ID,
                    "secret": self.GOOGLE_CLIENT_SECRET,
                    "key": self.GOOGLE_CLIENT_KEY,
                }
            },
        }

    MARTOR_THEME: str = "bootstrap"

    # Markdown extensions (default)
    MARTOR_MARKDOWN_EXTENSIONS: List[str] = [
        "markdown.extensions.extra",
        "markdown.extensions.nl2br",
        "markdown.extensions.smarty",
        "markdown.extensions.fenced_code",
        "markdown.extensions.sane_lists",
        # Custom markdown extensions.
        "martor.extensions.urlize",
        "martor.extensions.mention",  # to parse markdown mention
        "martor.extensions.emoji",  # to parse markdown emoji
        "martor.extensions.escape_html",  # to handle the XSS vulnerabilities
        "martor.extensions.mdx_add_id",  # to parse id like {#this_is_id}
    ]

    MARTOR_TOOLBAR_BUTTONS: List[str] = [
        "bold",
        "italic",
        "horizontal",
        "heading",
        "pre-code",
        "blockquote",
        "unordered-list",
        "ordered-list",
        "link",
        "image-link",
        "image-upload",
        "emoji",
        "direct-mention",
        "toggle-maximize",
        "help",
    ]

    MARTOR_ENABLE_CONFIGS: Dict[str, str] = {
        "emoji": "true",  # to enable/disable emoji icons.
        "imgur": "true",  # to enable/disable imgur/custom uploader.
        "mention": "false",  # to enable/disable mention
        "jquery": "true",  # to include/revoke jquery (require for admin default django)
        "living": "false",  # to enable/disable live updates in preview
        "spellcheck": "false",  # to enable/disable spellcheck in form textareas
        "hljs": "true",  # to enable/disable hljs highlighting in preview
    }

    MARTOR_ENABLE_ADMIN_CSS: bool = False

    MARTOR_ENABLE_LABEL: bool = True

    MARTOR_UPLOAD_URL: str = "/media/articles/content"

    TAGGIT_CASE_INSENSITIVE: bool = True

    JAZZMIN_SETTINGS: dict = {
        "site_title": "Python DM Pro",
        "site_header": "Python DM Pro",
        "site_brand": "Python DM Pro",
        "show_ui_builder": False,
        "user_avatar": "users.profile.avatar",
        "icons": {
            "auth": "fas fa-users-cog",
            "auth.user": "fas fa-user",
            "users.profile": "fas fa-user",
            "auth.Group": "fas fa-users",
            "blog": "fas fa-book",
            "blog.category": "fas fa-folder",
            "blog.article": "fa-solid fa-newspaper",
            "ratings.likedislike": "fa-solid fa-thumbs-up",
            "taggit.tag": "fas fa-tag",
            "comments.comment": "fa-solid fa-comment",
            "account.emailaddress": "fa-solid fa-envelope",
            "socialaccount.socialaccount": "fa-solid fa-user",
            "socialaccount.socialapp": "fa-solid fa-code",
            "socialaccount.socialtoken": "fa-solid fa-key",
        },
        "order_with_respect_to": [
            "blog",
            "blog.category",
            "blog.article",
            "comments.comment",
            "ratings.likedislike",
            "taggit.tag",
            "auth",
            "account.emailaddress",
            "socialaccount.socialaccount",
            "socialaccount.socialapp",
            "socialaccount.socialtoken",
        ],
        # Links to put along the top menu
        "topmenu_links": [
            # Url that gets reversed (Permissions can be added)
            {
                "name": "Главная",
                "url": "admin:index",
                "permissions": ["auth.view_user"],
            },
            # external url that opens in a new window (Permissions can be added)
            {
                "name": "Support",
                "url": "https://github.com/farridav/django-jazzmin/issues",
                "new_window": True,
            },
            # model admin to link to (Permissions checked against model)
            {"model": "auth.User"},
            # App with dropdown menu to all its models pages (Permissions checked against models)
            {"app": "blog"},
            {"app": "ratings"},
            {"app": "comments"},
        ],
        "site_logo": "admin_logo.png",
    }

    JAZZMIN_UI_TWEAKS: dict = {
        "navbar_small_text": True,
        "brand_small_text": True,
        "navbar": "navbar-dark",
        "sidebar_nav_compact_style": True,
        "theme": "flatly",
        # "dark_mode_theme": "darkly",
    }

    X_FRAME_OPTIONS: str = "SAMEORIGIN"


class Settings(DjangoSettings):
    PROJECT_NAME: str = "DM Pro"
    SENTRY_DSN: str | None = None
    TELEGRAM_BOT_TOKEN: SecretStr | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


config = Settings()
