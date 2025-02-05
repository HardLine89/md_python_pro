from django.contrib import admin

from users.models import Profile


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
