from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from users.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Профиль"
    fk_name = "user"


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


# Отменяем стандартную регистрацию модели User
admin.site.unregister(User)

# Регистрируем модель User с кастомным UserAdmin
admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "avatar", "about")
    list_display_links = ("user",)
    list_filter = ("user",)
    search_fields = ("user__username", "user__email")
    list_per_page = 10
    list_max_show_all = 100
    ordering = ("user",)
    readonly_fields = ("user",)
