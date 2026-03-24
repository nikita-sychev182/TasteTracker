from django import forms

from tracker.models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ("category", "title", "description", "image", "rating", "status")
