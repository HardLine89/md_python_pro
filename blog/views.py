from django.views.generic import ListView

from blog.models import Article


class ArticleListView(ListView):
    model = Article
    template_name = "blog/index.html"
    context_object_name = "articles"
    lookup_field = "slug"
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.select_related("category").prefetch_related("tags")
