from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.db import models
from django.db.models import Q
from urllib.parse import unquote

from tracker.forms import ItemForm
from tracker.models import Item


class ItemListView(ListView):
    model = Item
    template_name = "tracker/item_list.html"
    context_object_name = "items"
    paginate_by = 9
    paginate_orphans = 0

    def get_queryset(self):
        queryset = (
            Item.objects.select_related("user", "category")
            .order_by("-created_at")
        )

        # Проверка режима "Мои впечатления"
        if self.request.GET.get("my") and self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        elif self.request.user.is_authenticated:
            # Показываем публичные элементы ИЛИ элементы текущего пользователя
            queryset = queryset.filter(
                models.Q(is_public=True) | models.Q(user=self.request.user)
            )
        else:
            # Анонимным пользователям показываем только публичные элементы
            queryset = queryset.filter(is_public=True)

        # Фильтр по категории (только на главной, не в "Мои впечатления")
        category = self.request.GET.get("category")
        if category and not self.request.GET.get("my"):
            queryset = queryset.filter(category__name=category)

        # Фильтр по статусу (только в "Мои впечатления")
        if self.request.GET.get("my"):
            status = self.request.GET.get("status")
            if status in {"want", "done", "favorite"}:
                queryset = queryset.filter(status=status)

        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем категории только для главной страницы (не "Мои впечатления")
        if not self.request.GET.get("my"):
            from tracker.models import Category
            context["categories"] = Category.objects.all().order_by("name")
        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = "tracker/item_detail.html"
    context_object_name = "item"

    def get_queryset(self):
        queryset = Item.objects.select_related("user", "category")
        if self.request.user.is_authenticated:
            # Показываем публичные элементы ИЛИ элементы текущего пользователя
            return queryset.filter(
                models.Q(is_public=True) | models.Q(user=self.request.user)
            )
        return queryset.filter(is_public=True)


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


def load_more_items(request):
   """AJAX-эндпоинт для загрузки дополнительных элементов"""
   page = int(request.GET.get('page', 1))
   offset = (page - 1) * 9  # 9 элементов на страницу

   # Получаем базовый queryset из ItemListView
   queryset = (
       Item.objects.select_related("user", "category")
       .order_by("-created_at")
   )

   # Проверка режима "Мои впечатления"
   if request.GET.get("my") and request.user.is_authenticated:
       queryset = queryset.filter(user=request.user)
   elif request.user.is_authenticated:
       # Показываем публичные элементы ИЛИ элементы текущего пользователя
       queryset = queryset.filter(
           models.Q(is_public=True) | models.Q(user=request.user)
       )
   else:
       # Анонимным пользователям показываем только публичные элементы
       queryset = queryset.filter(is_public=True)

   # Фильтр по категории (только на главной, не в "Мои впечатления")
   category = request.GET.get("category")
   if category and not request.GET.get("my"):
       queryset = queryset.filter(category__name=category)

   # Фильтр по статусу (только в "Мои впечатления")
   if request.GET.get("my"):
       status = request.GET.get("status")
       if status in {"want", "done", "favorite"}:
           queryset = queryset.filter(status=status)

   search_query = request.GET.get("search")
   if search_query:
       # URL-decode the search query
       search_query = unquote(search_query)
       queryset = queryset.filter(title__icontains=search_query)

   # Получаем 9 дополнительных элементов начиная с offset
   items = queryset[offset:offset + 9]

   items_data = []
   for item in items:
       items_data.append({
           'id': item.id,
           'title': item.title,
           'status': item.get_status_display(),
           'rating': item.rating,
           'category': item.category.name if item.category else None,
           'category_icon': item.category.name.split(' ')[0] if item.category and ' ' in item.category.name else None,
           'image': item.image.url if item.image else None,
           'url': f"/tracker/{item.pk}/",
           'update_url': f"/tracker/{item.pk}/edit/",
           'delete_url': f"/tracker/{item.pk}/delete/",
           'is_owner': request.user.is_authenticated and request.user == item.user,
       })

   # Определяем, есть ли еще элементы для загрузки
   has_next = queryset.count() > offset + 9

   return JsonResponse({
       'items': items_data,
       'has_next': has_next,
       'next_page': page + 1 if has_next else None
   })

