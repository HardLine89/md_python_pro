import random

from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.core.paginator import Paginator
from django.db.models import Sum, Count, Q, F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView
from faker import Faker
from taggit.models import Tag

from blog.models import Article, Category
from comments.models import Comment
from utils.view_mixins import CommonContextMixin


class SearchListView(CommonContextMixin, ListView):
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
        query = self.request.GET.get("q")
        articles = (
            Article.objects.select_related("category")
            .prefetch_related("tags")
            .annotate(
                search=SearchVector("title", weight="A")
                + SearchVector("content", weight="B"),
                rank=SearchRank(SearchVector("title", "content"), query),
            )
            .filter(search=query)
            .order_by("-rank")
        )

        # Пагинация
        p = Paginator(articles, self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = p.get_page(page_number)

        # Добавляем статьи в контекст
        context["articles"] = page_obj
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


class ArticleListView(CommonContextMixin, ListView):
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

        articles = Article.objects.select_related("category").prefetch_related("tags")
        # Пагинация
        p = Paginator(articles, self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = p.get_page(page_number)

        # Добавляем статьи в контекст
        context["articles"] = page_obj
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


class ArticleDetailView(CommonContextMixin, DetailView):
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
        user_vote = None
        if self.request.user.is_authenticated:
            user_vote = article.votes.user_vote(self.request.user, article)
        context["user_vote"] = user_vote
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
            .order_by("-common_tags", "-created_at")[
                :5
            ]  # Сортируем по количеству общих тегов и дате
        )
        return context


class ArticleByCategoryView(CommonContextMixin, ListView):
    """Вывод всех статей по выбранной категории"""

    model = Article
    template_name = "blog/index.html"  # Используем тот же шаблон
    context_object_name = "articles"
    paginate_by = 10

    def get_template_names(self, *args, **kwargs):
        if self.request.htmx:
            return "blog/includes/article_list_card.html"
        else:
            return self.template_name

    def get_queryset(self):
        """Фильтруем статьи по категории"""
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return (
            Article.objects.filter(category=self.category)
            .select_related("category")
            .prefetch_related("tags")
        )

    def get_context_data(self, **kwargs):
        """Добавляем категории и пагинацию в контекст"""
        context = super().get_context_data(**kwargs)

        # Пагинация
        articles = self.get_queryset()
        p = Paginator(articles, self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = p.get_page(page_number)

        # Добавляем статьи и текущую категорию в контекст
        context["articles"] = page_obj
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
        context["current_category"] = self.category.slug
        return context


class ArticleByTagView(CommonContextMixin, ListView):
    """Вывод всех статей по выбранной категории"""

    model = Article
    template_name = "blog/index.html"  # Используем тот же шаблон
    context_object_name = "articles"
    paginate_by = 10

    def get_template_names(self, *args, **kwargs):
        if self.request.htmx:
            return "blog/includes/article_list_card.html"
        else:
            return self.template_name

    def get_queryset(self):
        """Фильтруем статьи по тегу"""
        self.tag = get_object_or_404(Tag, slug=self.kwargs["tag"])
        return (
            Article.objects.filter(tags=self.tag)
            .select_related("category")
            .prefetch_related("tags")
        )

    def get_context_data(self, **kwargs):
        """Добавляем категории и пагинацию в контекст"""
        context = super().get_context_data(**kwargs)

        # Пагинация
        articles = self.get_queryset()
        p = Paginator(articles, self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = p.get_page(page_number)

        # Добавляем статьи и текущую категорию в контекст
        context["articles"] = page_obj
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
        context["current_tag"] = self.tag
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
