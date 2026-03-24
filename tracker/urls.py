from django.urls import path

from tracker.views import ItemDetailView, ItemListView

app_name = "tracker"

urlpatterns = [
    path("", ItemListView.as_view(), name="home"),
    path("items/", ItemListView.as_view(), name="item_list"),
    path("items/<int:pk>/", ItemDetailView.as_view(), name="item_detail"),
]

