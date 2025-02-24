from django.urls import path, include

from users.views import UserProfileView

app_name = "users"

urlpatterns = [
    path("accounts/profile/", UserProfileView.as_view(), name="profile")
]
