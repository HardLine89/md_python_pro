from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import DetailView, TemplateView


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user  # Передаем текущего пользователя
        return context
