from django.urls import path, include

from users.views import UserProfileView, edit_profile

app_name = "users"
# TODO: Сделать эндпоинт по pk
urlpatterns = [
    path("accounts/profile/", UserProfileView.as_view(), name="profile"),
    path("accounts/profile/edit", edit_profile, name="edit_profile"),
]
