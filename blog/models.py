import uuid

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from martor.models import MartorField
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

from comments.models import Comment
from ratings.models import LikeDislike
from utils.mixins import DateMixin, SlugifyMixin
from utils.path_helpers import article_cover_path


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    # If you only inherit GenericUUIDTaggedItemBase, you need to define
    # a tag field. e.g.
    # tag = models.ForeignKey(Tag, related_name="uuid_tagged_items", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


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

    def get_absolute_url(self):
        return reverse("blog:category_list", kwargs={"slug": self.slug})

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
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
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
        default="articles/default.png",
    )
    views = models.PositiveIntegerField(verbose_name="Просмотры", default=0)
    comments = GenericRelation(
        Comment, verbose_name="Комментарии", related_query_name="articles"
    )
    votes = GenericRelation(
        LikeDislike, verbose_name="Оценки", related_query_name="articles"
    )

    def get_absolute_url(self):
        return reverse("blog:article_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.title} - {self.category}"

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_at"]
