import uuid

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from martor.models import MartorField
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

from blog.managers import LikeDislikeManager
from utils.mixins import DateMixin, SlugifyMixin
from utils.path_helpers import article_cover_path


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    # If you only inherit GenericUUIDTaggedItemBase, you need to define
    # a tag field. e.g.
    # tag = models.ForeignKey(Tag, related_name="uuid_tagged_items", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = ((DISLIKE, "Не нравится"), (LIKE, "Нравится"))

    vote = models.SmallIntegerField(verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


class Category(DateMixin, SlugifyMixin, models.Model):
    """
    Модель Категорий
    """

    id = models.UUIDField(
        verbose_name="Идентификатор",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(
        verbose_name="Название", max_length=255, blank=False, null=False
    )
    slug = models.SlugField(
        verbose_name="URL", max_length=255, blank=False, null=False, unique=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["-created_at"]


class Article(DateMixin, SlugifyMixin, models.Model):
    """
    Модель Статей
    """

    id = models.UUIDField(
        verbose_name="Идентификатор",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(
        verbose_name="Заголовок", max_length=255, blank=False, null=False
    )
    slug = models.SlugField(
        verbose_name="URL", max_length=255, blank=False, null=False, unique=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.CASCADE,
        related_name="articles",
    )
    content = MartorField(verbose_name="Содержание", blank=False)
    tags = TaggableManager(verbose_name="Теги", through=UUIDTaggedItem)
    cover = models.ImageField(
        verbose_name="Обложка",
        upload_to=article_cover_path,
        blank=True,
        null=True,
    )
    views = models.PositiveIntegerField(verbose_name="Просмотры", default=0)
    votes = GenericRelation(
        LikeDislike, verbose_name="Оценки", related_query_name="articles"
    )

    def __str__(self):
        return f"{self.title} - {self.category}"

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_at"]
