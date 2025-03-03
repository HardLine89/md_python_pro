from django.urls import path, include

from users.views import UserProfileView, edit_profile, UserProfileDetailView

app_name = "users"
# TODO: Сделать эндпоинт по pk
urlpatterns = [
    path("accounts/profile/", UserProfileView.as_view(), name="profile"),
    path("accounts/profile/<int:pk>", UserProfileDetailView.as_view(), name="profile_by_id"),
    path("accounts/profile/edit", edit_profile, name="edit_profile"),
]
