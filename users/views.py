from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import DetailView, TemplateView

from users.forms import ProfileForm


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProfileForm(instance=self.request.user.profile)
        context["user"] = self.request.user  # Передаем текущего пользователя
        return context


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён.")
            return redirect("users:profile")
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, "profile/user_profile.html", {"form": form})
