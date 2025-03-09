from django.db.models import Count
from taggit.models import Tag

from blog.models import Category
from comments.models import Comment


def common_context(request):
    return {
        "categories": Category.objects.all(),
        "latest_comments": Comment.objects.filter(parent=None).order_by("-created_at")[:3],
        "popular_week": None,
        "recent_articles": None,
        "popular_tags": Tag.objects.annotate(
            num_times=Count("taggit_taggeditem_items")
        ).order_by("-num_times")[:20],
    }
