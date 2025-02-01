from django.contrib import admin

from blog.models import Article, Category


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at", "updated_at")
    list_filter = ("category",)
    search_fields = ("title", "content")
    list_per_page = 10
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    fieldsets = [
        (None, {"fields": ["title", "slug", "category", "content", "tags", "cover"]}),
        ("Даты", {"fields": ["created_at", "updated_at"]}),
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title",)
    list_per_page = 10
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    fieldsets = [
        (None, {"fields": ["title", "slug"]}),
        ("Даты", {"fields": ["created_at", "updated_at"]}),
    ]
