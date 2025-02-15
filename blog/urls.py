from django.urls import path

from blog.views import ArticleListView

app_name = "blog"

urlpatterns = [
    path("", ArticleListView.as_view(), name="index"),
]
