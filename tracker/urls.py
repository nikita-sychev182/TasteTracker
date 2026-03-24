from django.urls import path

from tracker.views import home

app_name = "tracker"

urlpatterns = [
    path("", home, name="home"),
]

