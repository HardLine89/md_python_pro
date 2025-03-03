from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from ratings.models import LikeDislike
from utils.mixins import DateMixin


class Comment(DateMixin, models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    text = models.TextField(
        max_length=300, blank=True, verbose_name="Текст комментария"
    )
    article = models.ForeignKey(
        "blog.Article",
        on_delete=models.CASCADE,
        verbose_name="Статья",
    )
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        db_index=True,
        on_delete=models.CASCADE,
        verbose_name="Родитель",
    )
    votes = GenericRelation(
        LikeDislike, verbose_name="Оценки", related_query_name="articles"
    )

    def __str__(self):
        return f"{self.author} - {self.article} - {self.text}"

    def likes_count(self):
        content_type = ContentType.objects.get_for_model(Comment)
        return (
            LikeDislike.objects.likes()
            .filter(content_type=content_type, object_id=self.id)
            .count()
        )

    def dislikes_count(self):
        content_type = ContentType.objects.get_for_model(Comment)
        return (
            LikeDislike.objects.dislikes()
            .filter(content_type=content_type, object_id=self.id)
            .count()
        )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Коммент"
        verbose_name_plural = "Комменты"


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_notifications"
    )
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
