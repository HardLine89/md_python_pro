from django.db.models.signals import post_save
import random
import unidecode
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from users.models import Profile


@receiver(user_signed_up)
def populate_profile_on_signup(request, user, sociallogin=None, **kwargs):
    """
    Срабатывает при регистрации нового пользователя через соцсети.
    - Заполняет username (если его нет).
    - Если нет имени и фамилии, берет email до знака @ в качестве username.
    - Привязывает email из allauth.
    """
    if sociallogin:
        extra_data = sociallogin.account.extra_data  # Данные из Google
        first_name = extra_data.get("given_name", "").strip()
        last_name = extra_data.get("family_name", "").strip()
        email = extra_data.get("email", "").strip()

        # Если нет имени и фамилии, берем часть email до "@"
        if not first_name and not last_name and email:
            base_username = email.split("@")[0]
        else:
            base_username = unidecode.unidecode(f"{first_name}{last_name}").lower()

        # Генерируем уникальный username
        user.username = generate_unique_username(base_username)

        if first_name and last_name:
            # Заполняем имя и фамилию
            user.first_name = first_name
            user.last_name = last_name

        # Привязываем email
        if email and not user.email:
            user.email = email

        user.save()


def generate_unique_username(base_username):
    """Генерирует уникальный username, добавляя случайное число, если нужно."""
    username = base_username
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{random.randint(1000, 9999)}"
    return username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()  # Безопасно сохраняем профиль
