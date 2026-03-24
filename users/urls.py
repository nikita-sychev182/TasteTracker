from django.urls import path

from users.views import (
    UserLoginView,
    UserLogoutView,
    UserRegisterView,
    profile_edit_view,
    profile_view,
)

app_name = "users"

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/edit/", profile_edit_view, name="profile_edit"),
    path("profile/<str:username>/", profile_view, name="profile"),
]

