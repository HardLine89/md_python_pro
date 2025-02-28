from django.urls import path

from comments.views import add_comment, get_notifications, mark_notification_as_read, mark_all_notifications_as_read

app_name = "comments"
urlpatterns = [
    path("article/<uuid:article_id>/comment/", add_comment, name="add_comment"),
path("notifications/", get_notifications, name="get_notifications"),
    path("notifications/read/<int:notification_id>/", mark_notification_as_read, name="mark_notification_as_read"),
    path("notifications/read-all/", mark_all_notifications_as_read, name="mark_all_notifications_as_read"),
]
