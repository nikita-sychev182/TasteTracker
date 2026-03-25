from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from tracker.forms import ItemForm
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
            queryset = queryset.filter(user=self.request.user)
        status = self.request.GET.get("status")
        if status in {"want", "done", "favorite"}:
            queryset = queryset.filter(status=status)
        return queryset


class ItemDetailView(DetailView):
    model = Item
    template_name = "tracker/item_detail.html"
    context_object_name = "item"

    def get_queryset(self):
        queryset = Item.objects.select_related("user", "category")
        if self.request.user.is_authenticated:
            return queryset.filter(user=self.request.user)
        return queryset


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = "tracker/item_form.html"
    success_url = reverse_lazy("tracker:item_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = "tracker/item_form.html"
    success_url = reverse_lazy("tracker:item_list")

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = "tracker/item_confirm_delete.html"
    success_url = reverse_lazy("tracker:item_list")

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)


@login_required
@require_POST
def item_rate_view(request, pk: int):
    item = get_object_or_404(Item, pk=pk, user=request.user)
    rating_raw = request.POST.get("rating")
    try:
        rating = int(rating_raw)
    except (TypeError, ValueError):
        return JsonResponse({"error": "invalid_rating"}, status=400)

    if rating < 1 or rating > 5:
        return JsonResponse({"error": "invalid_rating"}, status=400)

    item.rating = rating
    item.save(update_fields=["rating"])
    return JsonResponse({"rating": item.rating})

