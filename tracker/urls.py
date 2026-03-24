from django.urls import path

from tracker.views import (
    ItemCreateView,
    ItemDeleteView,
    ItemDetailView,
    ItemListView,
    ItemUpdateView,
)

app_name = "tracker"

urlpatterns = [
    path("", ItemListView.as_view(), name="home"),
    path("items/", ItemListView.as_view(), name="item_list"),
    path("items/create/", ItemCreateView.as_view(), name="item_create"),
    path("items/<int:pk>/", ItemDetailView.as_view(), name="item_detail"),
    path("items/<int:pk>/edit/", ItemUpdateView.as_view(), name="item_update"),
    path("items/<int:pk>/delete/", ItemDeleteView.as_view(), name="item_delete"),
]

