import os
from pathlib import Path, PosixPath
from typing import List, Dict
from machina import MACHINA_MAIN_TEMPLATE_DIR, MACHINA_MAIN_STATIC_DIR
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
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

    REDIS_HOST: str = Field(env="REDIS_HOST", default="redis")
    REDIS_PORT: str = Field(env="REDIS_PORT", default="6379")
    REDIS_NUM_DB: str = Field(env="REDIS_NUM_DB", default="0")

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
        "taggit",
        "martor",
        "mdeditor",
        "django_htmx",
        "crispy_forms",
        "crispy_bootstrap4",
        "allauth",
        "allauth.account",
        "allauth.socialaccount",
        "allauth.socialaccount.providers.google",
        "unfold",
        "unfold.contrib.filters",
        "unfold.contrib.forms",
        "unfold.contrib.import_export",
        "unfold.contrib.guardian",
        "unfold.contrib.simple_history",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "mptt",
        "haystack",
        "widget_tweaks",
        # Machina apps:
        "machina",
        "machina.apps.forum",
        "machina.apps.forum_conversation",
        "machina.apps.forum_conversation.forum_attachments",
        "machina.apps.forum_conversation.forum_polls",
        "machina.apps.forum_feeds",
        "machina.apps.forum_moderation",
        "machina.apps.forum_search",
        "machina.apps.forum_tracking",
        "machina.apps.forum_member",
        "machina.apps.forum_permission",
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
        "machina.apps.forum_permission.middleware.ForumPermissionMiddleware",
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
            "DIRS": ["templates", "templates/machina", os.path.join(BASE_DIR, "templates/admin/"), MACHINA_MAIN_TEMPLATE_DIR,],
            # "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                    "django.template.context_processors.request",
                    "machina.core.context_processors.metadata",
                    "utils.context_processors.common_context",
                    "utils.context_processors.forum_context",
                ],
                "loaders": [
                    "django.template.loaders.filesystem.Loader",
                    "django.template.loaders.app_directories.Loader",
                ]
            },
        }
    ]
    CACHES: dict = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        },
        'machina_attachments': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/tmp',
        },
    }

    HAYSTACK_CONNECTIONS: dict = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    }
    MACHINA_PROFILE_AVATARS_ENABLED: bool = False
    MACHINA_FORUM_NAME: str = "Форум MDPython.pro"
    MACHINA_MARKUP_LANGUAGE: tuple = ('markdown2.markdown', {'safe_mode': True, 'extras': {'break-on-newline': True, 'fenced-code-blocks': None}})
    # SESSION_ENGINE: str = "django.contrib.sessions.backends.cache"
    # SESSION_CACHE_ALIAS: str = "default"
    # SESSION_COOKIE_SECURE: bool = True
    # CSRF_COOKIE_SECURE: bool = True
    # # Параметры для управления сессиями
    # SESSION_COOKIE_NAME: str = "sessionid"  # Имя cookie для сессии
    SESSION_COOKIE_AGE: int = 60 * 60 * 24 * 7  # Время жизни сессии в секундах (7days)
    # SESSION_EXPIRE_AT_BROWSER_CLOSE: bool = False  # Сессия сохраняется даже после закрытия браузера
    # SESSION_SAVE_EVERY_REQUEST: bool = True  # Сохранять сессии при каждом запросе

    LANGUAGE_CODE: str = "ru-ru"

    TIME_ZONE: str = "Asia/Bishkek"

    USE_I18N: bool = True

    USE_TZ: bool = True

    STATIC_URL: str = "static/"
    STATICFILES_DIRS: tuple = (
        MACHINA_MAIN_STATIC_DIR,
    )
    STATIC_ROOT: Path = BASE_DIR / "static"

    MEDIA_URL: str = "media/"
    MEDIA_ROOT: Path = BASE_DIR / "media"

    DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"

    AUTH_USER_MODEL: str = "auth.User"

    ACCOUNT_AUTHENTICATION_METHOD: str = "email"
    ACCOUNT_EMAIL_REQUIRED: bool = True
    ACCOUNT_UNIQUE_EMAIL: bool = True
    ACCOUNT_USERNAME_REQUIRED: bool = True
    ACCOUNT_USER_MODEL_USERNAME_FIELD: str | None = "username"

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

    TAGGIT_CASE_INSENSITIVE: bool = False

    MARTOR_MARKDOWN_SAFE_MODE: bool = False

    MDEDITOR_CONFIGS: dict = {
        "default": {
            "width": "100% ",  # Custom edit box width
            "height": 1000,  # Custom edit box height
            "toolbar": ["undo", "redo", "|",
                        "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                        "h1", "h2", "h3", "h5", "h6", "|",
                        "list-ul", "list-ol", "hr", "|",
                        "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table",
                        "datetime", "iframe",
                        "emoji", "html-entities", "pagebreak", "goto-line", "|",
                        "help", "info",
                        "||", "preview", "watch", "fullscreen"], # custom edit box toolbar
            "upload_image_formats": [
                "jpg",
                "jpeg",
                "gif",
                "png",
                "bmp",
                "webp",
            ],  # image upload format type
            "image_folder": "/media/articles/content",  # image save the folder name
            "theme": "dark",  # edit box theme, dark / default
            "preview_theme": "dark",  # Preview area theme, dark / default
            "editor_theme": "dark",  # edit area theme, pastel-on-dark / default
            "toolbar_autofixed": True,  # Whether the toolbar capitals
            "search_replace": True,  # Whether to open the search for replacement
            "emoji": True,  # whether to open the expression function
            "tex": True,  # whether to open the tex chart function
            "flow_chart": True,  # whether to open the flow chart function
            "sequence": True,  # Whether to open the sequence diagram function
            "watch": True,  # Live preview
            "lineWrapping": False,  # lineWrapping
            "lineNumbers": False,  # lineNumbers
            "language": "en",  # zh / en / es
        }
    }

    UNFOLD: dict = {
        "SITE_TITLE": "MDPython.pro",
        "SITE_HEADER": "Статьи",
        "SITE_SUBHEADER": "python",
        "SITE_DROPDOWN": [
            {
                "icon": "code",
                "title": _("MDPython.pro"),
                "link": "https://mdpython.pro",
            },
            # ...
        ],
        "SITE_URL": "/",
        # "SITE_ICON": lambda request: static("icon.svg"),  # both modes, optimise for 32px height
        "SITE_ICON": {
            "light": lambda request: static("favicon.png"),  # light mode
            "dark": lambda request: static("favicon.png"),  # dark mode
        },
        # "SITE_LOGO": lambda request: static("logo.svg"),  # both modes, optimise for 32px height
        "SITE_LOGO": {
            "light": lambda request: static("logo.png"),  # light mode
            "dark": lambda request: static("logo.png"),  # dark mode
        },
        "SITE_SYMBOL": "code",  # symbol from icon set
        "SITE_FAVICONS": [
            {
                "rel": "icon",
                "sizes": "32x32",
                "type": "image/svg+xml",
                "href": lambda request: static("favicon.png"),
            },
        ],
        "EXTENSIONS": {
            "modeltranslation": {
                "flags": {
                    "en": "🇬🇧",
                    "ru": "ru",
                },
            },
        },
        "SHOW_HISTORY": True,  # show/hide "History" button, default: True
        "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
        "SHOW_BACK_BUTTON": False,
        "SIDEBAR": {
            "show_search": True,  # Search in applications and models names
            "show_all_applications": False,  # Dropdown with all applications and models
            "navigation": [
                {
                    "title": _("Управление сайтом"),
                    "separator": False,
                    "items": [
                        {
                            "title": _("Главная"),
                            "icon": "home",
                            "link": reverse_lazy("admin:index"),
                        },
                    ],
                },
                {
                    "title": _("Блог"),
                    "separator": True,  # Top border
                    "collapsible": False,  # Collapsible group of links
                    "items": [
                        {
                            "title": _("Статьи"),
                            "icon": "article",  # Supported icon set: https://fonts.google.com/icons
                            "link": reverse_lazy("admin:blog_article_changelist"),
                            # "permission": lambda request: request.user.is_superuser,
                        },
                        {
                            "title": _("Категории"),
                            "icon": "category",
                            "link": reverse_lazy("admin:blog_category_changelist"),
                        },
                        {
                            "title": _("Теги"),
                            "icon": "bookmark",
                            "link": reverse_lazy("admin:taggit_tag_changelist"),
                        },
                    ],
                },
                {
                    "title": _("Комментарии, оценки"),
                    "separator": True,  # Top border
                    "collapsible": False,  # Collapsible group of links
                    "items": [
                        {
                            "title": _("Комментарии"),
                            "icon": "chat_bubble",
                            "link": reverse_lazy("admin:comments_comment_changelist"),
                        },
                        {
                            "title": _("Оценки"),
                            "icon": "star",
                            "link": reverse_lazy(
                                "admin:ratings_likedislike_changelist"
                            ),
                        },
                    ],
                },
                {
                    "title": _("Пользователи и группы"),
                    "separator": True,  # Top border
                    "collapsible": False,  # Collapsible group of links
                    "items": [
                        {
                            "title": _("Пользователи"),
                            "icon": "people",
                            "link": reverse_lazy("admin:auth_user_changelist"),
                        },
                        {
                            "title": _("Группы"),
                            "icon": "groups",
                            "link": reverse_lazy("admin:auth_group_changelist"),
                        },
                        {
                            "title": _("Профили"),
                            "icon": "account_box",
                            "link": reverse_lazy("admin:users_profile_changelist"),
                        },
                        {
                            "title": _("Аккаунты"),
                            "icon": "manage_accounts",
                            "link": reverse_lazy(
                                "admin:account_emailaddress_changelist"
                            ),
                        },
                        {
                            "title": _("Аккаунты в социальных сетях"),
                            "icon": "share",
                            "link": reverse_lazy(
                                "admin:socialaccount_socialaccount_changelist"
                            ),
                        },
                        {
                            "title": _("Социальные приложения"),
                            "icon": "login",
                            "link": reverse_lazy(
                                "admin:socialaccount_socialapp_changelist"
                            ),
                        },
                        {
                            "title": _("Токены социальных приложений"),
                            "icon": "token",
                            "link": reverse_lazy(
                                "admin:socialaccount_socialtoken_changelist"
                            ),
                        },
                    ],
                },
                {
                    "title": _("Форум"),
                    "separator": True,
                    "collapsible": False,
                    "items": [
                        {
                            "title": _("Ответы"),
                            "icon": "post",
                            "link": reverse_lazy("admin:forum_conversation_post_changelist"),
                        },
                        {
                            "title": _("Темы"),
                            "icon": "topic",
                            "link": reverse_lazy("admin:forum_conversation_topic_changelist"),
                        },
                        {
                            "title": _("Вложения"),
                            "icon": "attachment",
                            "link": reverse_lazy("admin:forum_attachments_attachment_changelist"),
                        },
                        {
                            "title": _("Варианты опроса темы"),
                            "icon": "ballot",
                            "link": reverse_lazy("admin:forum_polls_topicpolloption_changelist"),
                        },
                        {
                            "title": _("Голосования опроса темы"),
                            "icon": "how_to_vote",
                            "link": reverse_lazy("admin:forum_polls_topicpollvote_changelist"),
                        },
                        {
                            "title": _("Опросы темы"),
                            "icon": "where_to_vote",
                            "link": reverse_lazy("admin:forum_polls_topicpoll_changelist"),
                        },
                        {
                            "title": _("Отслеживания темы"),
                            "icon": "eye_tracking",
                            "link": reverse_lazy("admin:forum_tracking_topicreadtrack_changelist"),
                        },
                        {
                            "title": _("Отслеживания форума"),
                            "icon": "visibility",
                            "link": reverse_lazy("admin:forum_tracking_forumreadtrack_changelist"),
                        },
                        {
                            "title": _("Разрешения группы форума"),
                            "icon": "groups",
                            "link": reverse_lazy("admin:forum_permission_groupforumpermission_changelist"),
                        },
                        {
                            "title": _("Разрешения форума"),
                            "icon": "folder_managed",
                            "link": reverse_lazy("admin:forum_permission_forumpermission_changelist"),
                        },
                        {
                            "title": _("Форумные профили"),
                            "icon": "person_add",
                            "link": reverse_lazy("admin:forum_member_forumprofile_changelist"),
                        },
                        {
                            "title": _("Форумы"),
                            "icon": "forum",
                            "link": reverse_lazy("admin:forum_forum_changelist"),
                        },

                    ]
                 },
            ],
        },
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
