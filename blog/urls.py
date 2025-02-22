from django.urls import path

from blog.views import ArticleListView, ArticleDetailView, fake_blog, SearchListView, ArticleByCategoryView, \
    ArticleByTagView

app_name = "blog"

urlpatterns = [
    path("", ArticleListView.as_view(), name="index"),
    path("search/", SearchListView.as_view(), name="search"),
    path("category/<slug:slug>/", ArticleByCategoryView.as_view(), name="category_articles"),
    path("tag/<str:tag>/", ArticleByTagView.as_view(), name="tag_articles"),
    path("articles/<slug:slug>/", ArticleDetailView.as_view(), name="article_detail"),
    path("fake/", fake_blog, name="fake"),
]
