from django.views.generic import DetailView, ListView

from tracker.models import Item


class ItemListView(ListView):
    model = Item
    template_name = "tracker/item_list.html"
    context_object_name = "items"

    def get_queryset(self):
        queryset = (
            Item.objects.select_related("user", "category")
            .order_by("-created_at")
        )
        if self.request.user.is_authenticated:
            return queryset.filter(user=self.request.user)
        return queryset


class ItemDetailView(DetailView):
    model = Item
    template_name = "tracker/item_detail.html"
    context_object_name = "item"

