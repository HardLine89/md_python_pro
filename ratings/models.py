from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self, obj=None):
        queryset = self.get_queryset()
        if obj:
            content_type = ContentType.objects.get_for_model(obj)
            queryset = queryset.filter(content_type=content_type, object_id=obj.id)
        return queryset.aggregate(Sum("vote")).get("vote__sum") or 0

    def user_vote(self, user, obj):
        content_type = ContentType.objects.get_for_model(obj)
        try:
            vote = self.get_queryset().get(
                user=user, content_type=content_type, object_id=obj.id
            )
            return vote.vote
        except LikeDislike.DoesNotExist:
            return None

    def top_objects(self, model, limit=10):
        content_type = ContentType.objects.get_for_model(model)
        return (
            self.get_queryset()
            .filter(content_type=content_type)
            .values("object_id")
            .annotate(total_rating=Sum("vote"))
            .order_by("-total_rating")[:limit]
        )

    def votes_for_object(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return self.get_queryset().filter(content_type=content_type, object_id=obj.id)

    def remove_vote(self, user, obj):
        content_type = ContentType.objects.get_for_model(obj)
        self.get_queryset().filter(
            user=user, content_type=content_type, object_id=obj.id
        ).delete()

    def has_voted(self, user, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return (
            self.get_queryset()
            .filter(user=user, content_type=content_type, object_id=obj.id)
            .exists()
        )


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = ((DISLIKE, "Не нравится"), (LIKE, "Нравится"))

    vote = models.SmallIntegerField(verbose_name="Оценка", choices=VOTES)
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )

    content_type = models.ForeignKey(
        ContentType, verbose_name="Тип контента", on_delete=models.CASCADE
    )
    object_id = models.UUIDField(verbose_name="Идентификатор объекта")
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()

    def __str__(self):
        return f"{self.user} - {self.content_object} - {self.get_vote_display()}"

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        unique_together = ("user", "content_type", "object_id")
