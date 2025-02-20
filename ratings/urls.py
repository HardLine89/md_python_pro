from django.urls import path
from .views import vote_article

app_name = "ratings"

urlpatterns = [
    path("article/<uuid:article_id>/vote/", vote_article, name="vote_article"),
]
