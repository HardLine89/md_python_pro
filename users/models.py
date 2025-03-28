from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
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
        default="users/avatars/default.jpg",
    )
    about = models.TextField(
        blank=True,
        null=True,
        max_length=200,
        verbose_name="О пользователе",
    )

    def __str__(self):
        return str(_(f"Профиль пользователя {self.user}"))

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
