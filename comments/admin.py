from django.contrib import admin

from comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "created_at", "updated_at")
    list_filter = ("author", "created_at", "updated_at")
    search_fields = ("author", "text")
    list_per_page = 10
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
