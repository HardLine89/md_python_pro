from django.urls import path

from blog.views import ArticleListView, fake_blog

app_name = "blog"

urlpatterns = [
    path("", ArticleListView.as_view(), name="index"),
    path("fake/", fake_blog, name="fake"),
]
