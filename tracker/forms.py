from django import forms
from django.utils.safestring import mark_safe

from tracker.models import Item, Category


class CategorySelectWidget(forms.Select):
    """Виджет для выбора категории с иконками"""
    
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        # Добавляем иконку в начало label, если она есть
        if value and isinstance(label, str):
            parts = label.split(' ', 1)
            if len(parts) > 1 and parts[0].startswith(''):
                option['label'] = mark_safe(f'<span class="category-icon">{parts[0]}</span> {parts[1]}')
        return option


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ("category", "title", "description", "image", "rating", "status", "is_public")
        widgets = {
            "category": CategorySelectWidget(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Bootstrap-классы для нормального вида на страницах CRUD.
        for name, field in self.fields.items():
            if name in {"rating", "status"}:
                field.widget.attrs.update({"class": "form-select"})
            elif name in {"title", "image"}:
                field.widget.attrs.update({"class": "form-control"})
            elif name == "description":
                field.widget.attrs.update({"class": "form-control", "rows": 4})
            elif name == "is_public":
                field.widget.attrs.update({"class": "form-check-input"})
        
        # Устанавливаем queryset для категории (только существующие)
        self.fields["category"].queryset = Category.objects.all().order_by("name")
