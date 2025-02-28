import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import localtime
from django.utils.formats import date_format
from django.views.decorators.csrf import csrf_exempt

from blog.models import Article
from .models import Comment, Notification


@login_required
def add_comment(request, article_id):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text")
        parent_id = data.get("parent_id")

        # Проверка на пустой текст комментария
        if not text.strip():
            return JsonResponse(
                {"error": "Комментарий не может быть пустым"}, status=400
            )

        # Проверка существования статьи
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return JsonResponse({"error": "Статья не найдена"}, status=404)

        # Создание нового комментария
        comment = Comment.objects.create(
            author=request.user, text=text, content_object=article
        )

        # Если комментарий является ответом на другой комментарий, устанавливаем родителя
        if parent_id:
            try:
                parent_comment = Comment.objects.get(id=parent_id)
                comment.parent = parent_comment  # Устанавливаем родительский комментарий
                comment.save()

                # Создание уведомления для автора родительского комментария
                Notification.objects.create(
                    user=parent_comment.author,  # Автор родительского комментария
                    sender=request.user,  # Кто оставил ответ
                    comment=comment  # Сам комментарий
                )
            except Comment.DoesNotExist:
                return JsonResponse(
                    {"error": "Родительский комментарий не найден"}, status=404
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


@login_required
def get_notifications(request):
    """
    Возвращает список непрочитанных уведомлений.
    """
    notifications = Notification.objects.filter(
        user=request.user, is_read=False
    ).order_by("-created_at")

    data = [
        {
            "id": n.id,
            "text": f"{n.sender.username} ответил на ваш комментарий",
            "url": f"/articles/{n.comment.content_object.slug}#comment-{n.comment.id}",
        }
        for n in notifications
    ]

    return JsonResponse({"notifications": data})


@login_required
def mark_notification_as_read(request, notification_id):
    """
    Помечает одно уведомление как прочитанное.
    """
    notification = get_object_or_404(
        Notification, id=notification_id, user=request.user
    )
    notification.is_read = True
    notification.save()
    return JsonResponse({"success": True})


@login_required
def mark_all_notifications_as_read(request):
    """
    Помечает все уведомления как прочитанные.
    """
    request.user.notifications.update(is_read=True)
    return JsonResponse({"success": True})
