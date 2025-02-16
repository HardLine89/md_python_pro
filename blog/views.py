from django.core.paginator import Paginator
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import ListView

from blog.models import Article, Category
from comments.models import Comment


class ArticleListView(ListView):
    model = Article
    template_name = "blog/index.html"
    context_object_name = "articles"
    lookup_field = "slug"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        p = Paginator(
            Article.objects.select_related("category").prefetch_related("tags"),
            self.paginate_by,
        )
        context["articles"] = p.page(context["page_obj"].number)
        context["categories"] = Category.objects.all()
        context["comments"] = Comment.objects.all().order_by("-created_at")[:3]
        context["popular_week"] = (
            Article.objects.all()
            .filter(
                created_at__range=[
                    timezone.now() - timezone.timedelta(days=7),
                    timezone.now(),
                ]
            )
            .annotate(sum_views=Sum("views"), sum_votes=Sum("votes"))
            .order_by("-sum_views", "sum_votes")[:3]
        )

        return context
