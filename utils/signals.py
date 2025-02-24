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
    - Генерирует уникальный username на основе имени и фамилии.
    - Привязывает email из allauth.
    """
    if sociallogin:
        extra_data = sociallogin.account.extra_data  # Данные из Google
        first_name = extra_data.get("given_name", "")
        last_name = extra_data.get("family_name", "")
        email = extra_data.get("email", "")

        # Если username пустой, создаем на основе имени и фамилии
        if not user.username:
            base_username = unidecode.unidecode(f"{first_name}{last_name}").lower()
            user.username = generate_unique_username(base_username)

        # Заполняем имя и фамилию
        user.first_name = first_name
        user.last_name = last_name

        # Убеждаемся, что email привязан
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
