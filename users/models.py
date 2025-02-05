from django.contrib.auth.models import User
from django.db import models

from utils.path_helpers import profile_avatar_path


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь",
    )
    avatar = models.ImageField(
        upload_to=profile_avatar_path,
        blank=True,
        null=True,
        verbose_name="Аватар",
    )
    about = models.TextField(
        blank=True,
        null=True,
        max_length=500,
        verbose_name="О пользователе",
    )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
