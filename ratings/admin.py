from django.contrib import admin
from unfold.admin import ModelAdmin
from ratings.models import LikeDislike


@admin.register(LikeDislike)
class LikeDislikeAdmin(ModelAdmin):
    list_display = ("user", "content_object", "vote")
    list_filter = ("vote", "content_type")
    search_fields = ("user__username", "content_object__title")
    list_per_page = 10
