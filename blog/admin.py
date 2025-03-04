from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from blog.models import Article, Category
from ratings.models import LikeDislike
from unfold.admin import ModelAdmin

@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = (
        "title",
        "category",
        "author",
        "created_at",
        "updated_at",
        "views",
        "votes_info",
    )
    list_filter = ("category", "author")
    search_fields = ("title", "content")
    list_per_page = 10
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = (
        "created_at",
        "updated_at",
        "views",
        "votes_info",
    )
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "title",
                    "slug",
                    "category",
                    "content",
                    "tags",
                    "author",
                    "cover",
                ]
            },
        ),
        (
            "Статистика",
            {
                "fields": [
                    "votes_info",
                    "views",
                ]
            },
        ),
        ("Даты", {"fields": ["created_at", "updated_at"]}),
    ]

    def votes_info(self, obj):
        """
        Возвращает информацию о голосах (лайках/дизлайках) для статьи.
        """
        likes = obj.votes.filter(vote=LikeDislike.LIKE).count()
        dislikes = obj.votes.filter(vote=LikeDislike.DISLIKE).count()

        # Получаем content_type для модели obj
        content_type = ContentType.objects.get_for_model(obj)

        return format_html(
            '<a href="/admin/ratings/likedislike/?content_type__id__exact={}&object_id={}">Лайки: {}, Дизлайки: {}</a>',
            content_type.id,  # Используем ID вместо model name
            obj.id,
            likes,
            dislikes,
        )

    votes_info.short_description = "Голоса"


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title",)
    list_per_page = 10
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    fieldsets = [
        (None, {"fields": ["title", "slug"]}),
        ("Даты", {"fields": ["created_at", "updated_at"]}),
    ]
