from django.urls import path

from comments.views import add_comment

app_name = "comments"
urlpatterns = [
    path("article/<uuid:article_id>/comment/", add_comment, name="add_comment"),
]
