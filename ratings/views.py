import json

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from blog.models import Article
from comments.models import Comment
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
        user_vote = None
        if request.user.is_authenticated:
            user_vote = article.votes.user_vote(request.user, article)
        return JsonResponse(
            {
                "success": True,
                "user_vote": user_vote,
                "likes": LikeDislike.objects.likes()
                .filter(content_type=content_type, object_id=article.id)
                .count(),
                "dislikes": LikeDislike.objects.dislikes()
                .filter(content_type=content_type, object_id=article.id)
                .count(),
            }
        )

    return JsonResponse({"error": "Неверный запрос"}, status=400)


@login_required
@csrf_exempt
def vote_comment(request, comment_id):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")  # action может быть "like" или "dislike"

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return JsonResponse({"error": "Комментарий не найден"}, status=404)

        content_type = ContentType.objects.get_for_model(Comment)
        vote, created = LikeDislike.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=comment.id,
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

        # Получаем количество лайков и дизлайков для комментария
        user_vote = None
        if request.user.is_authenticated:
            user_vote = comment.votes.user_vote(request.user, comment)

        return JsonResponse(
            {
                "success": True,
                "user_vote": user_vote,
                "likes": LikeDislike.objects.likes()
                .filter(content_type=content_type, object_id=comment.id)
                .count(),
                "dislikes": LikeDislike.objects.dislikes()
                .filter(content_type=content_type, object_id=comment.id)
                .count(),
            }
        )

    return JsonResponse({"error": "Неверный запрос"}, status=400)
