from django.core.paginator import Paginator
from django.db.models import Sum, Count, Q
from django.utils import timezone
from taggit.models import Tag

from blog.models import Category, Article
from comments.models import Comment


class CommonContextMixin:
    """Миксин для добавления популярных статей, категорий, тегов и комментариев"""

    def get_common_context(self):

        return {
            "categories": Category.objects.all(),
            "comments": Comment.objects.order_by("-created_at")[:3],
            "popular_week": None,
            "recent_articles": None,
            "popular_tags": Tag.objects.annotate(
                num_times=Count("taggit_taggeditem_items")
            ).order_by("-num_times")[:20],
        }

    def get_context_data(self, **kwargs):
        """Добавляем общий контекст в каждый шаблон"""
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context())
        return context
