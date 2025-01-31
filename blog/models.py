import uuid
from django.db import models
from martor.models import MartorField
from taggit.managers import TaggableManager

from utils.mixins import DateMixin, SlugifyMixin


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
    tags = TaggableManager(verbose_name="Теги")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_at"]
