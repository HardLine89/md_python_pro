import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import localtime
from django.utils.formats import date_format
from django.views.decorators.csrf import csrf_exempt

from blog.models import Article
from .models import Comment


@login_required
@csrf_exempt
def add_comment(request, article_id):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text")

        if not text.strip():
            return JsonResponse(
                {"error": "Комментарий не может быть пустым"}, status=400
            )

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return JsonResponse({"error": "Статья не найдена"}, status=404)

        comment = Comment.objects.create(
            author=request.user, text=text, content_object=article
        )

        # Форматируем дату для ответа
        formatted_date = date_format(localtime(comment.created_at), "d M Y H:i")

        # Проверка, есть ли у пользователя аватар
        avatar_url = (
            comment.author.profile.avatar.url
            if comment.author.profile.avatar
            else f"https://via.placeholder.com/50?text={comment.author.username[0].upper()}"
        )

        return JsonResponse(
            {
                "success": True,
                "author": comment.author.username,
                "text": comment.text,
                "created_at": formatted_date,
                "avatar_url": avatar_url,
            }
        )

    return JsonResponse({"error": "Неверный запрос"}, status=400)
