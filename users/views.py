from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserProfileEditForm, UserRegisterForm

User = get_user_model()


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")


class UserLoginView(LoginView):
    template_name = "users/login.html"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("users:login")


def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    return render(
        request,
        "users/profile.html",
        {"profile_user": profile_user},
    )


@login_required
def profile_edit_view(request):
    if request.method == "POST":
        form = UserProfileEditForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )
        if form.is_valid():
            form.save()
            return redirect("users:profile", username=request.user.username)
    else:
        form = UserProfileEditForm(instance=request.user)

    return render(
        request,
        "users/profile_edit.html",
        {"form": form},
    )

