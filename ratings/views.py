import json

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from blog.models import Article
from ratings.models import LikeDislike


@login_required
@csrf_exempt
def vote_article(request, article_id):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return JsonResponse({"error": "Статья не найдена"}, status=404)

        content_type = ContentType.objects.get_for_model(article)
        vote, created = LikeDislike.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=article.id,
            defaults={"vote": 1 if action == "like" else -1},
        )

        if not created:
            if (vote.vote == 1 and action == "like") or (
                vote.vote == -1 and action == "dislike"
            ):
                vote.delete()  # Убираем голос
            else:
                vote.vote = 1 if action == "like" else -1
                vote.save()  # Меняем голос

        return JsonResponse(
            {
                "success": True,
                "likes": LikeDislike.objects.likes()
                .filter(content_type=content_type, object_id=article.id)
                .count(),
                "dislikes": LikeDislike.objects.dislikes()
                .filter(content_type=content_type, object_id=article.id)
                .count(),
            }
        )

    return JsonResponse({"error": "Неверный запрос"}, status=400)
