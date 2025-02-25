from django.urls import path, include

from users.views import UserProfileView

app_name = "users"
# TODO: Сделать эндпоинт по pk
urlpatterns = [
    path("accounts/profile/", UserProfileView.as_view(), name="profile")
]
