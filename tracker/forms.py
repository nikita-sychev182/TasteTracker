from django import forms

from tracker.models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ("category", "title", "description", "image", "rating", "status")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Bootstrap-классы для нормального вида на страницах CRUD.
        for name, field in self.fields.items():
            if name in {"category", "rating", "status"}:
                field.widget.attrs.update({"class": "form-select"})
            elif name in {"title", "image"}:
                field.widget.attrs.update({"class": "form-control"})
            elif name == "description":
                field.widget.attrs.update({"class": "form-control", "rows": 4})
            else:
                field.widget.attrs.update({"class": "form-control"})
