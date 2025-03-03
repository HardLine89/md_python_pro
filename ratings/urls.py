from django.urls import path
from .views import vote_article, vote_comment

app_name = "ratings"

urlpatterns = [
    path("article/<uuid:article_id>/vote/", vote_article, name="vote_article"),
    path("vote-comment/<int:comment_id>/", vote_comment, name="vote_comment"),
]
