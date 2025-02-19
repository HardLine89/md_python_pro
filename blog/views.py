import random

from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Sum, Count, Q, F
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import ListView, DetailView
from faker import Faker
from taggit.models import Tag

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
        context["recent_articles"] = None
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
        # Получаем 20 самых популярных тегов
        context["popular_tags"] = Tag.objects.annotate(
            num_times=Count("taggit_taggeditem_items")
        ).order_by("-num_times")[:20]

        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/article_detail.html"
    lookup_field = "slug"
    context_object_name = "article"

    def get_object(self, queryset=None):
        article = super().get_object(queryset)
        # Увеличиваем количество просмотров
        Article.objects.filter(pk=article.pk).update(views=F("views") + 1)
        return article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        article_content_type = ContentType.objects.get_for_model(article)
        context["comments"] = Comment.objects.filter(
            content_type=article_content_type,
            object_id=article.id  # UUID объекта
        )
        context["popular_week"] = None
        context["recent_articles"] = (
            Article.objects.filter(
                Q(category=article.category)  # Статьи из той же категории
                | Q(tags__in=article.tags.all())  # Статьи с похожими тегами
            )
            .exclude(id=article.id)  # Исключаем текущую статью
            .distinct()  # Убираем дубликаты
            .annotate(
                common_tags=Count("tags", filter=Q(tags__in=article.tags.all()))
            )  # Количество общих тегов
            .order_by("-common_tags", "-created_at")[:5]  # Сортируем по количеству общих тегов и дате
        )
        context["popular_tags"] = Tag.objects.annotate(
            num_times=Count("taggit_taggeditem_items")
        ).order_by("-num_times")[:20]
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
