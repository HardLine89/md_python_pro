from django.urls import path

from blog.views import ArticleListView, ArticleDetailView, fake_blog

app_name = "blog"

urlpatterns = [
    path("", ArticleListView.as_view(), name="index"),
    path("articles/<str:slug>/", ArticleDetailView.as_view(), name="article_detail"),
    path("fake/", fake_blog, name="fake"),
]
