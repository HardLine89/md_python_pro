import random

from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import ListView
from faker import Faker

from blog.models import Article, Category
from comments.models import Comment


class ArticleListView(ListView):
    model = Article
    template_name = "blog/index.html"
    context_object_name = "articles"
    lookup_field = "slug"
    paginate_by = 10

    def get_template_names(self, *args, **kwargs):
        if self.request.htmx:
            return "blog/includes/article_list_card.html"
        else:
            return self.template_name

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


def fake_blog(request):
    fake: Faker = Faker()
    # Create 10 categories
    for _ in range(10):
        Category.objects.create(title=fake.word(), slug=fake.slug())
    categories = Category.objects.all()

    # create 100 articles
    for _ in range(30):
        Article.objects.create(
            title=fake.sentence(),
            content=fake.text(),
            author_id=1,
            category_id=random.choice(categories).id,
            slug=fake.slug(),
        )
    return HttpResponse("Fake data generated successfully")
