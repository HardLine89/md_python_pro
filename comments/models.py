from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from utils.mixins import DateMixin


class Comment(DateMixin, models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    text = models.TextField(
        max_length=300, blank=True, verbose_name="Текст комментария"
    )
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name="Тип контента"
    )
    object_id = models.UUIDField(verbose_name="UUID объекта")
    content_object = GenericForeignKey()
    parent = models.ForeignKey(
        "self",
        related_name="children",
        blank=True,
        null=True,
        db_index=True,
        on_delete=models.CASCADE,
        verbose_name="Родитель",
    )

    def __str__(self):
        return f"{self.author} - {self.content_type} - {self.content_object}"

    class Meta:
        verbose_name = "Коммент"
        verbose_name_plural = "Комменты"
